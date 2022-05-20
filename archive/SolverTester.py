from timetableZ3 import *

class SolverTester :

    def __init__(self, solver) :
        self.solver = solver

    def enumerateClauses(self) :
        a = self.solver.assertions()
        for clause in a :
            print(clause)