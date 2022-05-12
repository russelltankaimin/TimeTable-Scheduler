from socket import timeout
from z3 import *
from NUSModule import *
from NUSClass import *
from itertools import combinations
set_option(timeout = 10000)

class TimeTableSchedulerZ3 :

    WEEKDAYS = {1 : "Monday",
                2 : "Tuesday",
                3 : "Wednesday",
                4 : "Thursday",
                5 : "Friday"}

    def __init__(self, dict) :
        self.semesterMods = dict
        self.s = Solver()
        self.lessonsByDay = [[], [], [], [], []]
        self.lecs = []
        self.tuts = []
        self.recs = []
        self.labs = []
        self.hashMap = {}
        self.IDToLiteralHashMap = {}
        self.StringToBoolLiteralHashMap = {}
        self.LiteralToObject = {}
        self.finalTimetable = [[], [], [], [], []]

    def initVariables(self) :
        for [key, value] in self.semesterMods.items() :
            print("In " + str(value) + " there are")
            print(str(len(value.lectures)) + " lectures")
            print(str(len(value.tutorials)) + " tutorials")
            print(str(len(value.recitations)) + " recitations")
            print(str(len(value.labs)) + " labs\n")
            for l in value.lectures :
                self.lessonsByDay[l.day - 1].append(l)
                self.lecs.append(l)
            for t in value.tutorials :
                self.lessonsByDay[t.day - 1].append(t)
                self.tuts.append(t)
            for r in value.recitations :
                self.lessonsByDay[r.day - 1].append(r)
                self.recs.append(r)
            for l in value.labs :
                self.lessonsByDay[l.day - 1].append(l)
                self.labs.append(l)

        id = 0
        for day in self.lessonsByDay:
            for nus_class in day:
                self.hashMap[nus_class] = id
                self.IDToLiteralHashMap[id] = Bool(str(nus_class))
                self.LiteralToObject[self.IDToLiteralHashMap[id]] = nus_class
                self.StringToBoolLiteralHashMap[str(nus_class)] = self.IDToLiteralHashMap[id]
                id = id + 1
        # print(self.StringToBoolLiteralHashMap)
    def chooseExactlyOne(self, lst) :
        if (len(lst) == 0) :
            return
        elif (len(lst) == 1) :
            self.s.add(self.StringToBoolLiteralHashMap[str(lst[0])])
            return
        AndList = []
        for c in lst :
            candidates = list(filter(lambda t : t is not c, lst))
            shortlist = list(map(lambda x : Not(self.StringToBoolLiteralHashMap[str(x)]), candidates))
            AndList.append(And([self.StringToBoolLiteralHashMap[str(c)]] + shortlist))
        self.s.add(Or(AndList))

    def chooseExactlyOneWithPairs(self, lst) :
        if (len(lst) == 0) : return
        elif (len(lst) == 1) :
            self.s.add(self.StringToBoolLiteralHashMap[str(lst[0])] == True)
            return
        else :
            s = set()
            literalList = []
            for item in lst :
                candidates = list(filter(lambda x : x.slot == item.slot, lst))
                converts = frozenset(map(lambda x : self.StringToBoolLiteralHashMap[str(x)] , candidates))
                s.add(converts)
            for pair in s :
                if len(pair) == 1 :
                    literalList.append(list(pair)[0])
                else :
                    literalList.append(And(list(pair)))
            self.chooseExactlyOneLiteral(literalList)

    def chooseExactlyOneLiteral(self, literalList) :
        self.s.add(AtMost(*literalList, 1))
        self.s.add(AtLeast(*literalList, 1))

    def chooseAtMostOneLiteral(self, literalList) :
        self.s.add(AtMost(*literalList, 1))

    def addConstraintTT(self) :
        # for each module
        #   for each tut/rec : pick exactly 1 that cannot clash
        #   for each lecture : pick that one set with the same slot
        # for all lessons on the same day : if got clash, negate the boolean variables
        # e.g a = lecture at 6pm - 8pm, b = Rec at 5pm - 7pm, then (a and !b) or (b and !a)
        for [modCode, module] in self.semesterMods.items() :
            self.chooseExactlyOne(module.tutorials)
            self.chooseExactlyOne(module.recitations)
            self.chooseExactlyOne(module.labs)
            self.chooseExactlyOneWithPairs(module.lectures)
        '''
        for day in self.lessonsByDay :
            for NUSCLASS in day :
                candidates =  list(filter(lambda x : x.willClash(NUSCLASS), day))
                #print(NUSCLASS)
                #print(candidates)
                convert = list(map(lambda x : self.StringToBoolLiteralHashMap[str(x)], candidates))
                if (len(convert) != 1) :
                   self.chooseAtMostOneLiteral(convert)
        '''

    def addOtherConstraints(self, fn) :
        raise NotImplementedError

    def fixPreferred(self, lst) :
        for item in lst :
            self.s.add(self.StringToBoolLiteralHashMap[str(item)])

    def optimiseTimetable(self) :
        #self.s.set("produce-proofs", True)
        self.initVariables()
        self.addConstraintTT()
        #print(len(self.s.assertions()))
        
        if (self.s.check() == sat) :
            print("SAT")
            self.printTimeTable()
        elif (self.s.check() == unsat) :
            print("UNSAT")
            print("No feasible timetable")

    def printTimeTable(self) :
        self.finalTimetable = [[], [], [], [], []]
        for item in self.s.model() :
            if (self.s.model()[item]) :
                pp = self.StringToBoolLiteralHashMap[str(item)]
                l = self.LiteralToObject[pp]
                self.finalTimetable[l.day - 1].append(l)
        for i in range(5) :
            self.finalTimetable[i] = sorted(self.finalTimetable[i], key=lambda x : x.start)
            print("On " + TimeTableSchedulerZ3.WEEKDAYS[i + 1])
            if (len(self.finalTimetable[i]) == 0) :
                print(" Hooray! You CAN Have No Classes On that Day!")
                continue
            for classes in self.finalTimetable[i] :
                print(" " + str(classes))