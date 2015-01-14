from enum import Enum
import operator as op

class Source(Enum):
    '''
    Enumeration for the different kind of sources that can be generated from
    a dice pool
    '''
    success = 1
    challenge = 2
    boon = 3
    bane = 4
    fatigue = 5
    delay = 6
    comet = 7
    star = 8
    success_plus = 9

class SourceRelation(object):
    '''
    Some Dice sources have a parity relationship (i.e. success <-> failure)
    in that when calculating the final probabilistic result the sources
    cancel each other out.
    '''
    parity = {Source.success: Source.challenge,
              Source.challenge: Source.success,
              Source.boon: Source.bane,
              Source.bane: Source.boon}

class Die(object):
    '''
    WFRPG 3rd Die representation
    '''
    def __init__(self, name, side_def):
        self.name = name
        self.side_def = side_def

    def __repr__(self):
        return self.name

    def num_sides(self):
        return len(self.side_def)

    def sides_with(self, source):
        return [side for side in self.side_def if source in side]

    def sides_with_only(self, source):
        return [[s for s in side if s == source] for side in self.side_def if source in side]

    @staticmethod
    def chance_of_no(percentages):
        return [(0, float(1) - sum(abs(per) for num, per in percentages))]

    def _chance_of(self, source, op):
        source_sides = self.sides_with_only(source)

        def summarize_side(summary, side):
            summary.update({len(side) : (summary.get(len(side), 0) + 1)})
            return summary

        summary_of_sides = reduce(summarize_side, source_sides, {})
        return [(op(0, x), float(y)/self.num_sides()) for x, y in summary_of_sides.items()]

    def chance_of(self, source):
        return self._chance_of(source, op.add)

    def chance_of_parity(self, source):
        parity = SourceRelation.parity.get(source, None)
        if not parity: return []
        return self._chance_of(parity, op.sub)

    def full_chance(self, source):
        chances = self.chance_of(source) + self.chance_of_parity(source)
        scratch = self.chance_of_no(chances)
        return scratch + chances

    def die_summary(self):
        summary = ['%s: %s' % (source.name,
                               [(val, '%.2f%%' % (occ*100))
                                for val, occ in self.full_chance(source)])
                   for source in Source if (0, 1.0) not in self.full_chance(source)]
        return '%s die has chances of \n%s' % (self.name, '\n'.join(summary))

    def pool(self, num):
        return [self.__class__(self.name, self.side_def) for num in range(num)]

class SpecDie(Die):
    '''
    Apx. Hack for the "exploding" mechanics of the specialization die
    '''
    def _chance_of(self, source, op):
        '''
        .5 + (1/6*.5) + (1/(6*6) *.5) + (1/(6*6*6) * .5) + (1/(6*6*6*6) * .5) ...
        approaches .6
        '''
        if (source is not Source.success):
            return super(SpecDie, self)._chance_of(source, op)
        else:
            return [(op(0, 1), 0.5),
                    (op(0, 2), 1.0/6 *.5),
                    (op(0, 3), 1.0/(6*6) * .5),
                    (op(0, 4), 1.0/(6*6*6) * .5),
                    (op(0, 5), 1.0/(6*6*6*6) * .5)]

characteristic_die = Die('Characteristic',
                           [[Source.success],
                            [Source.success],
                            [Source.success],
                            [Source.success],
                            [Source.boon],
                            [Source.boon],
                            [],
                            []])

challenge_die = Die('Challenge',
                      [[Source.challenge, Source.challenge],
                       [Source.challenge, Source.challenge],
                       [Source.challenge],
                       [Source.challenge],
                       [Source.bane],
                       [Source.bane],
                       [Source.star],
                       []])

conservative_die = Die('Conservative',
                         [[Source.success, Source.delay],
                          [Source.success, Source.delay],
                          [Source.success, Source.boon],
                          [Source.success],
                          [Source.success],
                          [Source.success],
                          [Source.success],
                          [Source.boon],
                          [Source.boon],
                          []])

reckless_die = Die('Reckless',
                     [[Source.success, Source.success],
                      [Source.success, Source.success],
                      [Source.success, Source.fatigue],
                      [Source.success, Source.fatigue],
                      [Source.success, Source.boon],
                      [Source.bane],
                      [Source.bane],
                      [Source.boon, Source.boon],
                      [], []])

fortune_die = Die('Fortune',
                    [[Source.success],
                     [Source.success],
                     [Source.boon],
                     [],[],[]])

misfortune_die = Die('Misfortune',
                       [[Source.challenge],
                        [Source.challenge],
                        [Source.bane],
                        [],[],[]])

specialization_die = SpecDie('Specialization',
                               [[Source.success],
                                [Source.success_plus],
                                [Source.boon],
                                [Source.comet],
                                [],[]])

all_dice = [characteristic_die, challenge_die, conservative_die, reckless_die,
            fortune_die, misfortune_die, specialization_die]

for die in all_dice:
    print die.die_summary(), '\n'

def build_probs(pool, source):
    '''
    Given a pool of dice and a target source, build and flatten the resulting
    probability tree.

    :param pool:
    :param source:
    :return:
    '''
    def _build_probs(parent_die, pool, source):
        if(len(pool)==0): return parent_die
        result = []
        head, tail = pool[0], pool[1:]
        hocc, hperc = parent_die
        for occ, perc in head.full_chance(source):
            apply = (occ+hocc, hperc*perc)
            if tail: result.extend(_build_probs(apply, tail, source))
            else:    result.append(_build_probs(apply, tail, source))
        return result

    return _build_probs((0, 1), pool, source)

def success_by(pool, needed):
    '''
    Given a flattened probability tree for a source, sum the chance of
    that the resulting source will meet or exceed a specified "needed" value.


    :param pool:
    :param needed:
    :return:
    '''
    return sum([x[1] for x in pool if x[0] >= needed])

pool = characteristic_die.pool(3) \
       + conservative_die.pool(2) \
       + reckless_die.pool(0) \
       + fortune_die.pool(1) \
       + specialization_die.pool(1) \
       + challenge_die.pool(1) \
       + misfortune_die.pool(3)

#print probs
print "Success for pool %s is: %.2f%%" % (str(pool), success_by(build_probs(pool, Source.success), 1)*100)
print "Boon for pool %s is: %.2f%%" % (str(pool), success_by(build_probs(pool, Source.boon), 2)*100)