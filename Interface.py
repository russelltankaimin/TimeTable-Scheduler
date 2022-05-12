from scrapper import Scrapper
from timetableZ3 import *

mods = ["CM1102", "MA2104", "CS2030S", "CS2040S"]
test1 = ["CS2030S", "CS1231S", "MA2001", "MA1521", "IS1103"]
scrapper = Scrapper(mods, '2021-2022', 2)
scrapper.scrape()
print(scrapper.semesterProcessed)
timetable = TimeTableSchedulerZ3(scrapper.semesterProcessed)
timetable.optimiseTimetable()