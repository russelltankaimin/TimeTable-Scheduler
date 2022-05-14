from z3 import *
from itertools import combinations
solver = Solver()
p = Bool('p')
q = Bool('q')
r = Bool('r')
s = Bool('s')

solver = Solver()


def chooseExactlyOneLiteral(literalList) :
        #self.s.add(AtMost(*literalList, 1))
        #self.s.add(AtLeast(*literalList, 1))
        
        if (len(literalList) == 0) :
            return
        elif (len(literalList) == 1) :
            solver.add(literalList[0] == True)
        else : 
            solver.add(Or(literalList))
            for pair in list(combinations(literalList,2)):
                solver.add(Not(And(pair)))

def chooseAtLeastOne(literalList) :
    if (len(literalList) == 0) :
        solver.add(False)
    else :
        solver.add(AtLeast(*literalList,1))

def chooseAtMostOne(literalList) :
    solver.add(AtMost(*literalList,1))



chooseAtMostOne([p,q,r,s])
chooseAtLeastOne([p,q,r,s])
solver.add(q == True)
solver.add(r == True)
print(solver.check())
print(solver.model())