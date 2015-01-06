class die(object):
    def __init__(self, name, sides, parity, num_success=[0], num_boon=[0]):
        self.name = name
        self.sides = sides
        self.parity = parity
        self.num_success = num_success

    def chance_of_success(self):
        failure = [(0, float(self.sides - sum(self.num_success))/self.sides)]
        num_success_and_side = zip(range(1, len(self.num_success)+1), self.num_success)
        success = [(x, float(y)/self.sides) for (x, y) in num_success_and_side]
        return failure + success

    def __repr__(self):
        return self.name

    def pool(self, num):
        return [die(self.name, self.sides, self.parity, self.num_success) for num in range(num)]

succ = lambda x, y: x+y
fail = lambda x, y: x-y

def build_tree(parent_node, pool):
    if(len(pool)==0): return parent_node
    head, tail = pool[0], pool[1:]

    result = []
    for perc in head.chance_of_success():
        apply = (head.parity(parent_node[0], perc[0]), parent_node[1]*perc[1])
        if tail:
            result.extend(build_tree(apply, tail))
        else:
            result.append(build_tree(apply, tail))

    return result

def success(pool):
    return sum([x[1] for x in pool if x[0] > 0])

char = die('characteristic', 8, succ, [4])
cons = die('conservative', 10, succ, [7])
reck = die('reckless', 10, succ, [3, 2])
fort = die('fortune', 6, succ, [2])
spec = die('specialization', 6, succ, [3])
chal = die('challenge', 8, fail, [2, 2])
misf = die('misfortune', 6, fail, [2])

pool = char.pool(8) + cons.pool(0) + reck.pool(0) + fort.pool(0) + spec.pool(0) + \
       chal.pool(1) + misf.pool(3)

begin = (0, 1)
probs = build_tree(begin, pool)
print "Success for pool %s is: %.2f%%" % (str(pool), success(probs)*100)