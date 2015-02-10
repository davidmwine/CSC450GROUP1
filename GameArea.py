import pygame, sys
from pygame.locals import *
from playersDisplay import PlayersDisplay
from player import Player


class gameArea():


    def __init__(self, scale=.75, ischild=False):

        self.width = int(scale*1920)
        self.height = int(scale*1080)
        self.scale = scale

        if ischild:
            self.area = pygame.Surface((self.width, self.height))
        else:
            pygame.init()
            self.area = pygame.display.set_mode((self.width, self.height))
            

        self.playerDis = PlayersDisplay(testplayers(), scale, 1)
        
        size_rect = pygame.Rect((0*scale, 900*self.scale), (1400*self.scale,180*self.scale))
        self.chatbox = self.area.subsurface(size_rect)
        
        #self.controls
        #self.board

        
        



    def get_area(self):
        return self.area


    def play(self):
        rect = pygame.Rect((1440*self.scale,0), (480*self.scale, 810*self.scale))
        self.area.blit(self.playerDis.getPD(), rect)
        while 1:
            self.chatbox.fill((255,255,255))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return 0 
        

def testplayers():
    p1 = Player("player1", "Agriculture")
    p2 = Player("player2", "Arts and Letters")
    p3 = Player("player3", "Natural and Applied Sciences")
    p4 = Player("player4", "Education")
    p5 = Player("player5", "Health and Human Services")
    p6 = Player("player6", "Humanities and Public Affairs")
    
    p1.addBuilding('Siceluff')
    p1.addBuilding('Cheek')
    p1.addBuilding('Plaster Student Union')
    p1.addBuilding('Kemper')
    p1.addBuilding('Strong')
    p1.addBuilding('Karls')
    p1.addBuilding('Glass')
    p1.addBuilding('Ellis')
    p1.addBuilding('JQH Arena')
    p1.addBuilding('McDonald Arena')
    p1.addBuilding('Meyer Library')
    p1.addBuilding('Foster Recreation Center')
    p1.addBuilding('Juanita K Hammons')
    p1.addBuilding('Pummil')
    p1.addBuilding('Plaster Stadium')
    p1.addBuilding('Temple')
    p2.addBuilding('Craig')
    p2.addBuilding('Ellis')

    p2.addDollars(30000000)
    
    return [p1, p2, p3, p4, p5, p6]



    
def main():
    screen = gameArea(.5)
    screen.play()



if __name__ == "__main__":
    main()








        
        
            
