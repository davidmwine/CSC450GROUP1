import Colors
from Token import Token
from Board import GameBoard


class Player(object):

    def __init__(self, name, college, board, bldgs, scale = 1):
        """
        'bldgs' should be a Buildings object, with attributes of buildings
        initialized from the creation of the game board.
        """
        self.scale = scale
        self.board = board
        self.allBldgs = bldgs
        self.name = name
        self.college = college
        self.dollars = 1500000
        self.points = 0
        self.pointsPerRound = 0
        self.buildings = []     # buildings that the player owns
        self.position = 0
        self.playerToken = Token(self.getColor(), self.position, self.board,
                                 self.allBldgs.getBuildingList(), self.scale)

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


    def getPossibleUpgrades(self):
        """
        Returns a tuple containing three lists:
        [0]: the names of buildings the player can upgrade to bachelors level
        [1]: the names of buildings the player can upgrade to masters level
        [2]: the names of buildings the player can upgrade to doctorate level
        """
        allAcadBuildings = self.allBldgs.getAcademicBuildings()
        acad = []   # will contain indices of the player's academic buildings
        for building in self.buildings:
            if building.getPurpose() == 'academic':
                acad.append(allAcadBuildings.index(building.getName()))

        twoInARow = []      # for keeping track of consecutive buildings
        threeOrMore = []

        if len(acad) == 0:
            return ([], [], [])

        startOfRun = acad[0]
        previous = acad[0]
        for x in acad:
            # We might need to add buildings to the lists if we've reached
            # the end of a run or if we've reached the end of the list.
            if x != previous + 1:
                endOfRun = previous
                runLength = acad.index(x) - acad.index(startOfRun)
            elif acad.index(x) == len(acad) - 1 and x == previous + 1:
                endOfRun = x
                runLength = acad.index(x) - acad.index(startOfRun) + 1

            # If the runs were long enough, add buildings to the lists.
            if runLength > 2:
                for i in range(acad.index(startOfRun), acad.index(endOfRun) + 1):
                    threeOrMore.append(acad[i])
                    twoInARow.append(acad[i])
            elif runLength == 2:
                twoInARow.append(startOfRun)
                twoInARow.append(endOfRun)

            # If runLength was set to be >0, that means we reached the end of a
            # run, so we need to start over.
            if runLength > 0:    
                startOfRun = x
                runLength = 0
                
            previous = x        

        # From the lists of eligible buildings compiled above, remove the ones
        # which have already been upgraded.  Then convert the indices to names.
        bachelors = []
        if len(acad) >= 2:
            for i in range(len(acad)):
                building = self.allBldgs.getBuilding( allAcadBuildings[acad[i]] )
                if building.getDegreeLvl() == "Associate":
                    bachelors.append( building.getName() )

        masters = []    
        for i in range(len(twoInARow)):
            building = self.allBldgs.getBuilding( allAcadBuildings[twoInARow[i]] )
            if building.getDegreeLvl() == "Associate" or building.getDegreeLvl() == "Bachelor":
                masters.append( building.getName() )

        doctorates = []    
        for i in range(len(threeOrMore)):
            building = self.allBldgs.getBuilding( allAcadBuildings[threeOrMore[i]] )
            if building.getDegreeLvl() != "Doctorate":
                doctorates.append( building.getName() )

        return (bachelors, masters, doctorates)


    def increasePosition(self, spaces):
        self.position += spaces
        numBuildings = self.allBldgs.getNumBuildings()
        if self.position > numBuildings:    # if we've passed Carrington
            self.points += self.pointsPerRound
            self.dollars += 200000
        self.position %= numBuildings
        self.playerToken.moveToken(spaces)


    def createToken(self, board, scale):
        """Used for re-creating the tokens after the screen has been resized."""
        self.playerToken = Token(self.getColor(), self.position, board,
                                 self.allBldgs.getBuildingList(), scale)

    def startToken(self):
        self.playerToken.displayToken()

    def removeToken(self):
        self.playerToken.clearToken()

    def displayWheel(self, percentage, location):
        self.playerToken.drawWheel(percentage, location)


            
