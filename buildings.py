
import pygame
from pygame.locals import *
import sys
import math
from building import Building

class Buildings(object):
    """ This class contains a definitive list of the buildings """

    def __init__(self):

        self.buildings = []
        
        self.buildings.append( Building('Carrington Hall',
                                        len(self.buildings), 'special') )
        
        self.buildings.append( Building('Siceluff Hall',
                                        len(self.buildings), 'academic') )
        
        self.buildings.append( Building('Cheek Hall',
                                        len(self.buildings), 'academic') )
        
        self.buildings.append( Building('Wells House',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( Building('University Bookstore',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( Building('Hammons Field',
                                        len(self.buildings), 'sports') )
        
        self.buildings.append( Building('Greenwood Lab School',
                                        len(self.buildings), 'academic') )
        
        self.buildings.append( Building('Blair-Shannon House',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( Building('Foster Recreation Center',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( Building('Bear Park North',
                                        len(self.buildings), 'special') )
        
        self.buildings.append( Building('Pummill Hall',
                                        len(self.buildings), 'academic') )
        
        self.buildings.append( Building('Juanita K Hammons',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( Building('Hill Hall',
                                        len(self.buildings), 'academic') )
        
        self.buildings.append( Building('JQH Arena',
                                        len(self.buildings), 'sports') )
        
        self.buildings.append( Building('Ellis Hall',
                                        len(self.buildings), 'academic') )
        
        self.buildings.append( Building('Hammons Student Center',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( Building('Craig Hall',
                                        len(self.buildings), 'academic') )
        
        self.buildings.append( Building('Allison South Stadium',
                                        len(self.buildings), 'sports') )
        
        self.buildings.append( Building('Art Annex',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( Building('Brick City',
                                        len(self.buildings), 'academic') )
        
        self.buildings.append( Building('Karls Hall',
                                        len(self.buildings), 'academic') )
        
        self.buildings.append( Building('Kings St Annex',
                                        len(self.buildings), 'academic') )
        
        self.buildings.append( Building('Meyer Library',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( Building('Forsythe Athletics Center',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( Building('Power House',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( Building('Freudenberger House',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( Building('Bear Park South',
                                        len(self.buildings), 'special') )
        
        self.buildings.append( Building('Plaster Sports Complex',
                                        len(self.buildings), 'sports') )
        
        self.buildings.append( Building('Central Stores & Maintenance',
                                        len(self.buildings), 'support') )
        
        self.buildings.append( Building('Temple Hall',
                                        len(self.buildings), 'academic') )
        
        self.buildings.append( Building('Kemper Hall',
                                        len(self.buildings), 'academic') )
        
        self.buildings.append( Building('Strong Hall',
                                        len(self.buildings), 'academic') )
        
        self.buildings.append( Building('Glass Hall',
                                        len(self.buildings), 'academic') )
        
        self.buildings.append( Building('McDonald Arena',
                                        len(self.buildings), 'academic') )
        
        self.buildings.append( Building('Plaster Student Union',
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
