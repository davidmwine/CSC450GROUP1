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
            self.color = Colors.LIGHTGRAY
            self.buildingColor = Colors.LIGHTGRAY
        elif purpose == 'special':
            self.color = Colors.BLUE
            self.buildingColor = Colors.BLUE
        elif purpose == 'sports':
            self.color = Colors.GREEN
            self.buildingColor = Colors.GREEN
        elif purpose == 'support':
            self.color = Colors.WHITE
            self.buildingColor = Colors.WHITE

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

    def getRect(self): 
        return self.rect
        
    def setRect(self, rect):
        self.rect = rect   

    def getColor(self):
        return self.color
    
    def setColor(self, color):
        self.color = color

    def getBuildingColor(self):
        return self.buildingColor
        

class OwnableBuilding(Building):    
    def __init__(self, name, sequence, purpose, image, price=200000):
        Building.__init__(self, name, sequence, purpose, image)
        self.owner = None           # Which dean 'owns' building
        self.price = price          # Inital purchase price
        self.renovation = False     # Under Renovation (similar to mortgage)

    def getPrice(self): 
        return self.price

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
        

class NonAcademicBuilding(OwnableBuilding):

    def __init__(self, name, sequence, purpose, image, price=200000):
        OwnableBuilding.__init__(self, name, sequence, purpose, image)
        self.costNonAcademic = 10000     # Cost to other deans for non-academic building fees

    def getFeeAmount(self):
        return self.costNonAcademic

    
class AcademicBuilding(OwnableBuilding):

    def __init__(self, name, sequence, image, price=200000):
        OwnableBuilding.__init__(self, name, sequence, 'academic', image)
        self.degreeLvl = 'Associate'
        self.baseGrads = 10             # Base number of grad points earned
        self.costAssociate = 10000      # Cost to other deans for associate lvl classes
        self.costBachelor = 20000       # Cost to other deans for bachelor lvl classes
        self.costMaster = 30000         # Cost to other deans for master lvl classes
        self.costDoctorate = 40000      # Cost to other deans for doctorate lvl classes

    def getDegreeLvl(self):
        return self.degreeLvl
        
    def setDegreeLvl(self, degLvl):
        self.degreeLvl = degLvl

    def getFeeAmount(self):
        if self.degreeLvl == 'Associate':
            return self.costAssociate
        elif self.degreeLvl == 'Bachelor':
            return self.costBachelor
        elif self.degreeLvl == 'Master':
            return self.costMaster
        elif self.degreeLvl == 'Doctorate':
            return self.costDoctorate


class Buildings(object):
    """ This class contains a definitive list of the buildings """
    # These have been reordered to reflect the new board layout.

    def __init__(self):

        self.buildings = []
        
        self.buildings.append( Building('Carrington Hall',
                                        len(self.buildings), 'special',
                                        "CarringtonHall.png") )
        
        self.buildings.append( AcademicBuilding('Siceluff Hall',
                                        len(self.buildings), "SiceluffHall.png") )
        
        self.buildings.append( AcademicBuilding('Cheek Hall',
                                        len(self.buildings), "CheekHall.png") )
        
        self.buildings.append( NonAcademicBuilding('University Bookstore',
                                        len(self.buildings), 'support',
                                        "UniversityBookstore.png") )
        
        self.buildings.append( NonAcademicBuilding('Hammons Field',
                                        len(self.buildings), 'sports',
                                        "HammonsField.png") )
        
        self.buildings.append( AcademicBuilding('Greenwood Lab School',
                                        len(self.buildings), "GreenwoodLabSchool.png") )
        
        self.buildings.append( NonAcademicBuilding('Foster Recreation Center',
                                        len(self.buildings), 'support',
                                        "FosterRecreationCenter.png") )
        
        self.buildings.append( NonAcademicBuilding('Juanita K Hammons',
                                        len(self.buildings), 'support',
                                        "JuanitaKHammons.png") )
        
        self.buildings.append( Building('Bear Park North',
                                        len(self.buildings), 'special',
                                        "BearParkNorth.png") )
        
        self.buildings.append( NonAcademicBuilding('Hammons Student Center',
                                        len(self.buildings), 'support',
                                        "HammonsStudentCenter.png") )
        
        self.buildings.append( AcademicBuilding('Brick City',
                                        len(self.buildings), "BrickCity.png") )
        
        self.buildings.append( AcademicBuilding('Kings St Annex',
                                        len(self.buildings), "KingsStreetAnnex.png") )
        
        self.buildings.append( NonAcademicBuilding('JQH Arena',
                                        len(self.buildings), 'sports',
                                        "JQHArena.png") )
        
        self.buildings.append( NonAcademicBuilding('Forsythe Athletics Center',
                                        len(self.buildings), 'support',
                                        "ForsytheAthleticsCenter.png") )
        
        self.buildings.append( AcademicBuilding('McDonald Arena',
                                        len(self.buildings), "McDonaldArena.png") )
        
        self.buildings.append( NonAcademicBuilding('Plaster Student Union',
                                        len(self.buildings), 'support',
                                        "PlasterStudentUnion.png") )
        
        self.buildings.append( Building('Bear Park South',
                                        len(self.buildings), 'special',
                                        "BearParkSouth.png") )
        
        self.buildings.append( NonAcademicBuilding('Meyer Library',
                                        len(self.buildings), 'support',
                                        "MeyerLibrary.png") )
        
        self.buildings.append( AcademicBuilding('Glass Hall',
                                        len(self.buildings), "GlassHall.png") )
        
        self.buildings.append( AcademicBuilding('Strong Hall',
                                        len(self.buildings), "StrongHall.png") )
        
        self.buildings.append( NonAcademicBuilding('Allison South Stadium',
                                        len(self.buildings), 'sports',
                                        "AllisonSouthStadium.png") )
        
        self.buildings.append( AcademicBuilding('Kemper Hall',
                                        len(self.buildings), "KemperHall.png") )
        
        self.buildings.append( AcademicBuilding('Temple Hall',
                                        len(self.buildings), "TempleHall.png") )
        
        self.buildings.append( NonAcademicBuilding('Central Stores & Maintenance',
                                        len(self.buildings), 'support',
                                        "CentralMaintenance.png") )
        
        self.buildings.append( Building('Accreditation Review',
                                        len(self.buildings), 'special',
                                        "AccreditationReview.png") )

        self.buildings.append( NonAcademicBuilding('Power House',
                                        len(self.buildings), 'support',
                                        "PowerHouse.png") )
        
        self.buildings.append( AcademicBuilding('Karls Hall',
                                        len(self.buildings), "KarlsHall.png") )
        
        self.buildings.append( AcademicBuilding('Craig Hall',
                                        len(self.buildings), "CraigHall.png") )
        
        self.buildings.append( NonAcademicBuilding('Plaster Sports Complex',
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
