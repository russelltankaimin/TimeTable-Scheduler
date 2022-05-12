import requests
import json
from NUSClass import *
from NUSModule import NUSModule

#r = requests.get('https://api.nusmods.com/v2/2021-2022/modules/CS2040S.json')
#MODULE = ["ST2334, CS2030S", "MA2001"]
#a = r.content
#b = json.loads(a.decode('utf-8'))
#print(b['semesterData'][1]['timetable'])

WEEKDAYS = {
    'Monday' : 1,
    'Tuesday' : 2,
    'Wednesday' : 3,
    'Thursday' : 4,
    'Friday' : 5
}

class Scrapper :

    URL_FRONT = 'https://api.nusmods.com/v2/'
    URL_MIDDLE = '/modules/'
    URL_END = '.json'

    def __init__(self, modList, AY, semester) :
        self.modList = modList
        self.AY = AY
        self.semester = semester
        self.semesterProcessed = {}

    def scrape(self) :
        for mod in self.modList :
            URL = Scrapper.URL_FRONT + self.AY + Scrapper.URL_MIDDLE + mod + Scrapper.URL_END
            req = json.loads(requests.get(URL).content.decode('utf-8'))
            print(req)

            nusMod = NUSModule(mod)
            print(self.semester)
            print(nusMod)
            nusClasses = req['semesterData'][self.semester - 1]['timetable']
            for someClass in nusClasses :
                slot = someClass['classNo']
                day = WEEKDAYS[someClass['day']]
                start = int(someClass['startTime'])
                end = int(someClass['endTime'])
                if (someClass['lessonType'] == 'Tutorial') :
                    nusMod.addTutorials(Tutorial(slot, day, start, end, mod))
                elif (someClass['lessonType'] == 'Laboratory') :
                    nusMod.addLabs(Lab(slot, day, start, end, mod))
                elif (someClass['lessonType'] == 'Recitation') :
                    nusMod.addRecitations(Recitation(slot, day, start, end, mod))
                elif (someClass['lessonType'] == 'Lecture') :
                    nusMod.addLectures(Lecture(slot, day, start, end, mod))
                else :
                    print("Unknown Class Type Detected!")
                    continue
            self.semesterProcessed[mod] = nusMod
        print("Scrapping Successful")

