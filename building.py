import Colors

import pygame
from pygame.locals import *
import sys

class Building(object):

    def __init__(self, name, sequence, purpose):
        self.name = name            # Name of Building
        self.sequence = sequence    # Sequence number of space
        self.purpose = purpose      # Purpose of building (academic, sports, support, special)
        self.rect = None            # Rect object where its space is located on the board

        if purpose == 'academic':
            self.color = Colors.LIGHTGRAY 
        elif purpose == 'special':
            self.color = Colors.BLUE
        elif purpose == 'sports':
            self.color = Colors.GREEN 
        elif purpose == 'support':
            self.color = Colors.WHITE 

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
        

class OwnableBuilding(Building):    
    def __init__(self, name, sequence, purpose, price=200000):
        Building.__init__(self, name, sequence, purpose)
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

    def __init__(self, name, sequence, purpose, price=200000):
        OwnableBuilding.__init__(self, name, sequence, purpose)
        self.costNonAcademic = 10000     # Cost to other deans for non-academic building fees

    def getFeeAmount(self):
        return self.costNonAcademic

    
class AcademicBuilding(OwnableBuilding):

    def __init__(self, name, sequence, price=200000):
        OwnableBuilding.__init__(self, name, sequence, 'academic')
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
                                        len(self.buildings), 'special') )
        
        self.buildings.append( AcademicBuilding('Siceluff Hall',
                                        len(self.buildings)) )
        
        self.buildings.append( AcademicBuilding('Cheek Hall',
                                        len(self.buildings)) )
        
        self.buildings.append( NonAcademicBuilding('University Bookstore',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( NonAcademicBuilding('Hammons Field',
                                        len(self.buildings), 'sports') )
        
        self.buildings.append( AcademicBuilding('Greenwood Lab School',
                                        len(self.buildings)) )
        
        self.buildings.append( NonAcademicBuilding('Foster Recreation Center',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( NonAcademicBuilding('Juanita K Hammons',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( Building('Bear Park North',
                                        len(self.buildings), 'special') )
        
        self.buildings.append( NonAcademicBuilding('Hammons Student Center',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( AcademicBuilding('Brick City',
                                        len(self.buildings)) )
        
        self.buildings.append( AcademicBuilding('Kings St Annex',
                                        len(self.buildings)) )
        
        self.buildings.append( NonAcademicBuilding('JQH Arena',
                                        len(self.buildings), 'sports') )
        
        self.buildings.append( NonAcademicBuilding('Forsythe Athletics Center',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( AcademicBuilding('McDonald Arena',
                                        len(self.buildings)) )
        
        self.buildings.append( NonAcademicBuilding('Plaster Student Union',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( Building('Bear Park South',
                                        len(self.buildings), 'special') )
        
        self.buildings.append( NonAcademicBuilding('Meyer Library',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( AcademicBuilding('Glass Hall',
                                        len(self.buildings)) )
        
        self.buildings.append( AcademicBuilding('Strong Hall',
                                        len(self.buildings)) )
        
        self.buildings.append( NonAcademicBuilding('Allison South Stadium',
                                        len(self.buildings), 'sports') )
        
        self.buildings.append( AcademicBuilding('Kemper Hall',
                                        len(self.buildings)) )
        
        self.buildings.append( AcademicBuilding('Temple Hall',
                                        len(self.buildings)) )
        
        self.buildings.append( NonAcademicBuilding('Central Stores & Maintenance',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( Building('Accreditation Review',
                                        len(self.buildings), 'special') )

        self.buildings.append( NonAcademicBuilding('Power House',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( AcademicBuilding('Karls Hall',
                                        len(self.buildings)) )
        
        self.buildings.append( AcademicBuilding('Craig Hall',
                                        len(self.buildings)) )
        
        self.buildings.append( NonAcademicBuilding('Plaster Sports Complex',
                                        len(self.buildings), 'sports') )
        
        self.buildings.append( AcademicBuilding('Ellis Hall',
                                        len(self.buildings)) )
        
        self.buildings.append( AcademicBuilding('Hill Hall',
                                        len(self.buildings)) )

        self.buildings.append( AcademicBuilding('Pummill Hall',
                                        len(self.buildings)) )


    def getBuildingList(self):
        return self.buildings

    def getNumBuildings(self):
        return len(self.buildings)


def main():
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


if __name__ == '__main__':
    main()        
