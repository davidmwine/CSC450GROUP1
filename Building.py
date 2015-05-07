import Colors

import pygame
from pygame.locals import *
import sys
import os

class Building(object):

    def __init__(self, name, sequence, purpose, image):
        self.name = name            # Name of Building
        self.sequence = sequence    # Sequence number of space
        self.purpose = purpose      # Purpose of building (academic, sports, support, special)
        self.rect = None            # Rect object where its space is located on the board
        self.image = pygame.image.load(os.path.join("img","buildings",image))

        if purpose == 'academic':
            self.initialColor = Colors.WHITE
            self.color = Colors.WHITE
        elif purpose == 'stealable':
            self.initialColor = Colors.BLUE
            self.color = Colors.BLUE
        elif purpose == 'sports':
            self.initialColor = Colors.GREEN
            self.color = Colors.GREEN
        elif purpose == 'card':
            self.initialColor = Colors.OFFBLACK
            self.color = Colors.OFFBLACK
        elif purpose == 'utility':
            self.initialColor = Colors.DARKGRAY
            self.color = Colors.DARKGRAY

    def getImage(self):
        return self.image

    def getName(self): 
        return self.name

    def getSequence(self):
        return self.sequence

    def getPurpose(self):
        return self.purpose

    def getPointList(self): 
        return self.pointList
        
    def setPointList(self, pointList):
        self.pointList = pointList

    def getInnerPointList(self): 
        return self.innerPointList
        
    def setInnerPointList(self, innerPointList):
        self.innerPointList = innerPointList    

    def getRect(self): 
        return self.rect
        
    def setRect(self, rect):
        self.rect = rect   

    def getColor(self):
        return self.color
    
    def setColor(self, color):
        self.color = color

    def getInitialColor(self):
        return self.initialColor    
        

class OwnableBuilding(Building):    
    def __init__(self, name, sequence, purpose, image):
        Building.__init__(self, name, sequence, purpose, image)
        self.owner = None           # Which dean 'owns' building
        self.renovation = False     # Under Renovation (similar to mortgage)

    def getOwner(self):
        return self.owner
    
    def setOwner(self, owner):
        self.owner = owner

    def getRenovation(self): 
        return self.renovation
        
    def setRenovation(self):            # Toggles value of renovation (True/False)
        if self.renovation == False:
            self.renovation = True
        elif self.renovation == True:
            self.renovation = False    
        
    
class AcademicBuilding(OwnableBuilding):

    def __init__(self, name, sequence, image):
        OwnableBuilding.__init__(self, name, sequence, 'academic', image)
        self.degreeLvl = 'Associate'
        
    @staticmethod
    def setFeePercentages():
        """
        The fees for landing on an academic building are a percentage of the
        current building cost.  They depend on the degree level of the building
        but are otherwise the same for all buildings.  This method sets those
        percentages.
        """
        AcademicBuilding.associateFeePercent = 0.2
        AcademicBuilding.bachelorFeePercent = 0.4
        AcademicBuilding.masterFeePercent = 0.6
        AcademicBuilding.doctorateFeePercent = 0.8

    def getDegreeLvl(self):
        return self.degreeLvl
        
    def setDegreeLvl(self, degLvl):
        self.degreeLvl = degLvl

    def getFeeAmount(self, buildingCost):
        """
        Returns the amount of the fees charged to a player for landing on
        an academic building, given the current building cost.
        """
        if self.degreeLvl == 'Associate':
            return buildingCost * AcademicBuilding.associateFeePercent
        elif self.degreeLvl == 'Bachelor':
            return buildingCost * AcademicBuilding.bachelorFeePercent
        elif self.degreeLvl == 'Master':
            return buildingCost * AcademicBuilding.masterFeePercent
        elif self.degreeLvl == 'Doctorate':
            return buildingCost * AcademicBuilding.doctorateFeePercent


class Buildings(object):
    """ This class contains a definitive list of the buildings """
    # These have been reordered to reflect the new board layout.

    def __init__(self):

        self.currentPrice = 200000  # current price of all ownable buildings
        self.priceIncreasePercentage = 0.2  # percentage the price increases by
                                            # when it increases every n rounds

        AcademicBuilding.setFeePercentages()

        self.buildings = []
        
        self.buildings.append( Building('Carrington Hall',
                                        len(self.buildings), 'special',
                                        "CarringtonHall.png") )
        
        self.buildings.append( AcademicBuilding('Siceluff Hall',
                                        len(self.buildings), "SiceluffHall.png") )
        
        self.buildings.append( AcademicBuilding('Cheek Hall',
                                        len(self.buildings), "CheekHall.png") )
        
        self.buildings.append( OwnableBuilding('University Bookstore',
                                        len(self.buildings), 'stealable',
                                        "UniversityBookstore.png") )
        
        self.buildings.append( OwnableBuilding('Hammons Field',
                                        len(self.buildings), 'sports',
                                        "HammonsField.png") )
        
        self.buildings.append( Building('Greenwood Lab School',
                                        len(self.buildings), 'card',
                                        "GreenwoodLabSchool.png") )

        self.buildings.append( Building('Power House',
                                        len(self.buildings), 'utility',
                                        "PowerHouse2.png") )
        
        self.buildings.append( AcademicBuilding('Juanita K Hammons',
                                        len(self.buildings), "JuanitaKHammons.png") )
        
        self.buildings.append( Building('Bear Park North',
                                        len(self.buildings), 'special',
                                        "BearParkNorth.png") )

        self.buildings.append( AcademicBuilding('Forsythe Athletics Center',
                                        len(self.buildings),
                                        "ForsytheAthleticsCenter.png") )
        
        self.buildings.append( AcademicBuilding('Brick City',
                                        len(self.buildings), "BrickCity.png") )
        
        self.buildings.append( AcademicBuilding('Kings St Annex',
                                        len(self.buildings), "KingsStreetAnnex.png") )
        
        self.buildings.append( OwnableBuilding('JQH Arena', len(self.buildings),
                                        'sports', "JQHArena.png") )

        self.buildings.append( Building('Hammons Student Center',
                                        len(self.buildings), 'card',
                                        "HammonsStudentCenter.png") )
        
        self.buildings.append( AcademicBuilding('McDonald Arena',
                                        len(self.buildings), "McDonaldArena.png") )
        
        self.buildings.append( OwnableBuilding('Plaster Student Union',
                                        len(self.buildings), 'stealable',
                                        "PlasterStudentUnion.png") )
        
        self.buildings.append( Building('Bear Park South',
                                        len(self.buildings), 'special',
                                        "BearParkSouth.png") )
        
        self.buildings.append( AcademicBuilding('Glass Hall',
                                        len(self.buildings), "GlassHall.png") )
        
        self.buildings.append( AcademicBuilding('Strong Hall',
                                        len(self.buildings), "StrongHall.png") )

        self.buildings.append( Building('Meyer Library',
                                        len(self.buildings), 'card',
                                        "MeyerLibrary.png") )
        
        self.buildings.append( OwnableBuilding('Allison South Stadium',
                                        len(self.buildings), 'sports',
                                        "AllisonSouthStadium.png") )
        
        self.buildings.append( AcademicBuilding('Kemper Hall',
                                        len(self.buildings), "KemperHall.png") )
        
        self.buildings.append( AcademicBuilding('Temple Hall',
                                        len(self.buildings), "TempleHall.png") )
        
        self.buildings.append( Building('Central Stores & Maintenance',
                                        len(self.buildings), 'utility',
                                        "CentralMaintenance.png") )
        
        self.buildings.append( Building('Accreditation Review',
                                        len(self.buildings), 'special',
                                        "AccreditationReview.png") )

        
        
        self.buildings.append( AcademicBuilding('Karls Hall',
                                        len(self.buildings), "KarlsHall.png") )
        
        self.buildings.append( AcademicBuilding('Craig Hall',
                                        len(self.buildings), "CraigHall.png") )

        self.buildings.append( Building('Foster Recreation Center',
                                        len(self.buildings), 'card',
                                        "FosterRecreationCenter2.png") )
        
        self.buildings.append( OwnableBuilding('Plaster Sports Complex',
                                        len(self.buildings), 'sports',
                                        "PlasterSportsComplex.png") )
        
        self.buildings.append( AcademicBuilding('Ellis Hall',
                                        len(self.buildings), "EllisHall.png") )
        
        self.buildings.append( AcademicBuilding('Hill Hall',
                                        len(self.buildings), "HillHall.png") )

        self.buildings.append( AcademicBuilding('Pummill Hall',
                                        len(self.buildings), "PummillHall.png") )


    def getBuildingList(self):
        return self.buildings

    def getBuildingNames(self):
        """Returns a list of the names of all buildings."""
        return [building.getName() for building in self.buildings]
        
    def getNumBuildings(self):
        return len(self.buildings)

    def getBuilding(self, name):
        """Given the name of a building, returns its Building object."""
        for building in self.buildings:
            if building.name == name:
                return building

    def getAcademicBuildings(self):
        """Returns a list of the names of all the academic buildings."""
        acadBuildings = []
        for building in self.buildings:
            if building.purpose == 'academic':
                acadBuildings.append(building.name)
        return acadBuildings

    def getCurrentPrice(self):
        """Gets the current price of all ownable buildings."""
        return self.currentPrice

    def increasePrice(self):
        """Increases the price of all ownable buildings by the set percentage."""
        self.currentPrice *= (1 + self.priceIncreasePercentage)


def main():
    '''
    # Testing
    buildings = Buildings().getBuildingList()
    
    print(Buildings().getNumBuildings())

    for building in range(len(buildings)):
        print(buildings[building].getName())
        print(buildings[building].getSequence(), "   /8: ", buildings[building].getSequence()/8, "   %8: ", buildings[building].getSequence()%8)
        #print(buildings[building].getPosition())
        print(buildings[building].getPurpose())
        print(buildings[building].getRect())
        print(buildings[building].getColor())
        print()
    '''
    print(Buildings().getAcademicBuildings())
    print(Buildings().getBuilding('Glass Hall').getSequence())
    

if __name__ == '__main__':
    main()        
