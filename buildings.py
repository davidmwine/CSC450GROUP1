
import pygame
from pygame.locals import *
import sys
from building import *

class Buildings(object):
    """ This class contains a definitive list of the buildings """
    # These still need to be reordered to reflect the new board layout.

    def __init__(self):

        self.buildings = []
        
        self.buildings.append( Building('Carrington Hall',
                                        len(self.buildings), 'special') )
        
        self.buildings.append( AcademicBuilding('Siceluff Hall',
                                        len(self.buildings)) )
        
        self.buildings.append( AcademicBuilding('Cheek Hall',
                                        len(self.buildings)) )
        
        self.buildings.append( NonAcademicBuilding('Wells House',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( NonAcademicBuilding('University Bookstore',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( NonAcademicBuilding('Hammons Field',
                                        len(self.buildings), 'sports') )
        
        self.buildings.append( AcademicBuilding('Greenwood Lab School',
                                        len(self.buildings)) )
        
        self.buildings.append( NonAcademicBuilding('Blair-Shannon House',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( NonAcademicBuilding('Foster Recreation Center',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( Building('Bear Park North',
                                        len(self.buildings), 'special') )
        
        self.buildings.append( AcademicBuilding('Pummill Hall',
                                        len(self.buildings)) )
        
        self.buildings.append( NonAcademicBuilding('Juanita K Hammons',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( AcademicBuilding('Hill Hall',
                                        len(self.buildings)) )
        
        self.buildings.append( NonAcademicBuilding('JQH Arena',
                                        len(self.buildings), 'sports') )
        
        self.buildings.append( AcademicBuilding('Ellis Hall',
                                        len(self.buildings)) )
        
        self.buildings.append( NonAcademicBuilding('Hammons Student Center',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( AcademicBuilding('Craig Hall',
                                        len(self.buildings)) )
        
        self.buildings.append( NonAcademicBuilding('Allison South Stadium',
                                        len(self.buildings), 'sports') )
        
        self.buildings.append( NonAcademicBuilding('Art Annex',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( AcademicBuilding('Brick City',
                                        len(self.buildings)) )
        
        self.buildings.append( AcademicBuilding('Karls Hall',
                                        len(self.buildings)) )
        
        self.buildings.append( AcademicBuilding('Kings St Annex',
                                        len(self.buildings)) )
        
        self.buildings.append( NonAcademicBuilding('Meyer Library',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( NonAcademicBuilding('Forsythe Athletics Center',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( NonAcademicBuilding('Power House',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( NonAcademicBuilding('Freudenberger House',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( Building('Bear Park South',
                                        len(self.buildings), 'special') )
        
        self.buildings.append( NonAcademicBuilding('Plaster Sports Complex',
                                        len(self.buildings), 'sports') )
        
        self.buildings.append( NonAcademicBuilding('Central Stores & Maintenance',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( AcademicBuilding('Temple Hall',
                                        len(self.buildings)) )
        
        self.buildings.append( AcademicBuilding('Kemper Hall',
                                        len(self.buildings)) )
        
        self.buildings.append( AcademicBuilding('Strong Hall',
                                        len(self.buildings)) )
        
        self.buildings.append( AcademicBuilding('Glass Hall',
                                        len(self.buildings)) )
        
        self.buildings.append( AcademicBuilding('McDonald Arena',
                                        len(self.buildings)) )
        
        self.buildings.append( NonAcademicBuilding('Plaster Student Union',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( Building('Accreditation Review',
                                        len(self.buildings), 'special') )



    def getBuildingList(self):
        return self.buildings

    def getNumBuildings(self):
        return len(self.buildings)




def main():
    # Testing
    buildings = Buildings().getBuildingList()
    print(buildings[2].getName())
    print(Buildings().getNumBuildings())



if __name__ == '__main__':
    main()        
