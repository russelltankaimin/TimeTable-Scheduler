from z3 import *
from itertools import combinations
#solver = Solver()
#p = Bool('p')
#q = Bool('q')
#r = Bool('r')
#s = Bool('s')

#solver = Solver()


#def chooseExactlyOneLiteral(literalList) :
#        #self.s.add(AtMost(*literalList, 1))
#        #self.s.add(AtLeast(*literalList, 1))
#        
#        if (len(literalList) == 0) :
#            return
#        elif (len(literalList) == 1) :
#            solver.add(literalList[0] == True)
#       else : 
#            solver.add(Or(literalList))
#            for pair in list(combinations(literalList,2)):
#                solver.add(Not(And(pair)))

#def chooseAtLeastOne(literalList) :
#    if (len(literalList) == 0) :
#        solver.add(False)
#    else :
#        solver.add(AtLeast(*literalList,1))

#def chooseAtMostOne(literalList) :
#    solver.add(AtMost(*literalList,1))



#chooseAtMostOne([p,q,r,s])
#chooseAtLeastOne([p,q,r,s])
#solver.add(q == True)
#solver.add(r == True)
#print(solver.check())
#print(solver.model())
w = Bool('w')
x = Bool('x')
y = Bool('y')
z = Bool('z')

s = Solver()
soln = 0
hashMap = {'x' : x, 'y' : y, 'z' : z}
s.add(Or(x,y,z, w))
print(s.check())
print(s.model())
'''
def block_model(model) :
    m = model.model()
    model.add(Or([f() != m[f] for f in m.decls() if f.arity() == 0 ]))
'''
def block_model1(sp, terms):
    m = sp.model()
    sp.add(Or([t != m.eval(t, model_completion=True) for t in terms]))

block_model1(s, [x,y,z])
print(s.check())
print(s.model())
block_model1(s, [x,y,z])
print(s.check())
print(s.model())

block_model1(s, [x,y,z])
print(s.check())
print(s.model())
block_model1(s, [x,y,z])
print(s.check())
print(s.model())

block_model1(s, [x,y,z])
print(s.check())
print(s.model())
block_model1(s, [x,y,z])
print(s.check())
print(s.model())

block_model1(s, [x,y,z])
print(s.check())
print(s.model())