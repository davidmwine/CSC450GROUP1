from globals import Globals
from building import Building


class Player(object):

    def __init__(self, name, college):
        self.name = name
        self.college = college
        self.dollars = 1500000
        self.points = 0
        self.pointsPerRound = 0
        self.buildings = []

    def getName(self):
        return self.name

    def getCollege(self):
        return self.college

    def getCollegeAbbr(self):
        return Globals.collegeAbbr.get(self.college, "")    # look up in dictionary

    def getDollars(self):
        return self.dollars

    def getPoints(self):
        return self.points

    def getPointsPerRound(self):
        return self.pointsPerRound

    def getBuildings(self):
        return self.buildings

    def addDollars(self, dollarsToAdd):
        self.dollars += dollarsToAdd

    def subtractDollars(self, dollarsToSubtract):
        self.dollars -= dollarsToSubtract

    def addPoints(self, pointsToAdd):
        self.points += pointsToAdd

    def subtractPoints(self, pointsToSubtract):
        self.points += pointsToSubtract   

    def addPointsPerRound(self, pointsToAdd):
        self.pointsPerRound += pointsToAdd

        
    def addBuilding(self, building):
        
        if building in self.buildings:
            return -1   # I'm not sure what we actually want to do here...

        # Insert the building in the correct position in the list
        # using one iteration of insertion sort.
        i = len(self.buildings)
        self.buildings.append(building)
        while i>0 and building.getPosition() < self.buildings[i-1].getPosition():
            self.buildings[i] = self.buildings[i-1]
            i -= 1
        self.buildings[i] = building    
            

    def removeBuilding(self, building):
        if building in self.buildings:
            self.buildings.remove(building)
        else:
            return -1   # or whatever we want to do here...    




    
