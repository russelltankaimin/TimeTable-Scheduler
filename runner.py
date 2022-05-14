from NUSModule import NUSModule
from NUSClass import *
from timetableZ3 import TimeTableSchedulerZ3


f = open("tests/smaller.in","r")
print("Input File exists ! \nReading File now ...")

semesterMods = dict()
modList = []
i = -1
for line in f:
    line = line.strip("\n").split(" ")
    if (line[0] == "M") :
        i = i + 1
        modList.append(NUSModule(line[1]))
    elif (line[0] == "T") :
        t = modList[-1]
        t.addTutorials(Tutorial(line[1], int(line[2]), int(line[3]), int(line[4]), t.modCode))
    elif (line[0] == "R") :
        t = modList[-1]
        t.addRecitations(Recitation(line[1], int(line[2]), int(line[3]), int(line[4]), t.modCode))
    elif (line[0] == "L") :
        t = modList[-1]
        t.addLectures(Lecture(line[1], int(line[2]), int(line[3]), int(line[4]), t.modCode))
    else:
        continue

for mod in modList :
    semesterMods[mod.modCode] = mod

print("Below are the Semester Mods that are successfully logged !")
print(semesterMods)

#Initialise Timetable
timetable = TimeTableSchedulerZ3(semesterMods)
timetable.optimiseTimetable()
    