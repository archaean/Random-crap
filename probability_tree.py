class die(object):
    def __init__(self, name, side, succ, perc):
        self.name = name
        self.side = side
        self.succ = succ
        self.perc = perc

    def percentages(self):
        return [(x, float(y)/self.side) for (x, y) in self.perc]

    def __repr__(self):
        return self.name

succ = lambda x, y: x+y
fail = lambda x, y: x-y

char = die('char', 8, succ, [(0, 4), (1, 4)])
cons = die('conserv', 10, succ, [(0, 3), (1, 7)])
reck = die('reckless', 10, succ, [(0, 5), (1, 3), (2, 2)])
fort = die('fortune', 6, succ, [(0, 4), (1, 2)])
spec = die('special', 6, succ, [(0, 3), (1, 3)])
chal = die('challenge', 8, fail, [(0, 4), (1, 2), (2, 2)])
misf = die('misfortune', 6, fail, [(0, 4), (1, 2)])

pool = [reck, char, char, char, chal, misf]

class node(object):
    def __init__(self, value):
        self.value = value
        self.children = []

    def __repr__(self, level=0):
        ret = "\t"*level+repr(self.value)+"\n"
        for child in self.children:
            ret += child.__repr__(level+1)
        return ret

def build_tree(parent_node, pool):
    if(len(pool)==0): return parent_node.value
    head, tail = pool[0], pool[1:]

    result = []
    for perc in head.percentages():
        apply = (head.succ(parent_node.value[0], perc[0]), parent_node.value[1]*perc[1])
        child_node = node(apply)
        parent_node.children.extend([child_node])
        if tail:
            result.extend(build_tree(child_node, tail))
        else:
            result.append(build_tree(child_node, tail))

    return result

def success(pool):
    return sum([x[1] for x in probs if x[0] > 0])

def gen_pool(nchar=0, ncons=0, nreck=0, nfort=0, nspec=0, nchal=0, nmisf=0):
    pass

begin = node((0, 1))
probs = build_tree(begin, pool)
print "Success for pool "+str(pool)+" is:", success(probs)


