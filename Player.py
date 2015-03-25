import Colors
from Building import *
from Token import Token
from Board import GameBoard


class Player(object):

    def __init__(self, name, college, board, bldgs, scale = 1):
        self.scale = scale
        self.board = board
        self.bldgs = bldgs
        self.name = name
        self.college = college
        self.dollars = 1500000
        self.points = 0
        self.pointsPerRound = 0
        self.buildings = []     # buildings that the player owns
        self.buildingList = Buildings().getBuildingList()
        self.position = 0
        self.playerToken = Token(self.getColor(), self.position, self.board, self.bldgs, self.scale)

    def getName(self):
        return self.name

    def getCollege(self):
        return self.college

    def getCollegeAbbr(self):
        return Colors.COLLEGEABBR.get(self.college, "")    # look up in dictionary

    def getColor(self):
        return Colors.COLLEGECOLORS.get(self.college, "")

    def getDollars(self):
        return self.dollars

    def getPoints(self):
        return self.points

    def getPointsPerRound(self):
        return self.pointsPerRound

    def getBuildings(self):
        return self.buildings

    def getBuildingNames(self):
        return [building.getName() for building in self.buildings]

    def getPosition(self):
        return self.position

    def addDollars(self, dollarsToAdd):
        self.dollars += dollarsToAdd

    def subtractDollars(self, dollarsToSubtract):
        self.dollars -= dollarsToSubtract

    def addPoints(self, pointsToAdd):
        self.points += pointsToAdd

    def subtractPoints(self, pointsToSubtract):
        self.points -= pointsToSubtract   

    def addPointsPerRound(self, pointsToAdd):
        self.pointsPerRound += pointsToAdd

        
    def addBuilding(self, building):
        
        if building in self.buildings:
            return -1   # I'm not sure what we actually want to do here...

        # Insert the building in the correct position in the list
        # using one iteration of insertion sort.
        i = len(self.buildings)
        self.buildings.append(building)
        while i>0 and building.getSequence() < self.buildings[i-1].getSequence():
            self.buildings[i] = self.buildings[i-1]
            i -= 1
        self.buildings[i] = building    
            

    def removeBuilding(self, building):
        if building in self.buildings:
            self.buildings.remove(building)
        else:
            return -1   # or whatever we want to do here...

    def increasePosition(self, spaces):
        self.position += spaces
        numBuildings = Buildings().getNumBuildings()
        if self.position > numBuildings:    # if we've passed Carrington
            self.points += self.pointsPerRound
            self.dollars += 200000
        self.position %= numBuildings
        self.playerToken.moveToken(spaces)


    def displayWheel(self, percentage, location):
        self.playerToken.drawWheel(percentage, location)


