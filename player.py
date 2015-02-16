from globals import Globals

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
        if building not in self.buildings:
            self.buildings.append(building)

    def removeBuilding(self, building):
        if building in self.buildings:
            self.buildings.remove(building)




    
