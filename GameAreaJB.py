import pygame, sys
from pygame.locals import *
from playersDisplay import PlayersDisplay
from player import Player
from building import Building
from boardJB import GameBoard


class GameArea():


    def __init__(self, scale=1, ischild=False):

        self.width = int(scale*1920)
        self.height = int(scale*1080)
        self.scale = scale

        if ischild:
            self.area = pygame.Surface((self.width, self.height))
        else:
            pygame.init()
            self.area = pygame.display.set_mode((self.width, self.height))
            

        self.playerDis = PlayersDisplay(testplayers(), scale, True)
        self.gameBoard = GameBoard(True)

        size_rect = pygame.Rect((1440*scale, 810*self.scale), (480*self.scale, 270*self.scale))
        self.chatbox = self.area.subsurface(size_rect)
        
        size_rect = pygame.Rect((0*scale, 0*self.scale), (1440*self.scale, 1080*self.scale))
        self.board   = self.area.subsurface(size_rect)


    def get_area(self):
        return self.area


    def play(self):

        # Insert Players Display
        rect = pygame.Rect((1440*self.scale, 0), (480*self.scale, 810*self.scale))
        self.area.blit(self.playerDis.getPD(), rect)

        # Insert Game Board
        rect = pygame.Rect((32, 24), (800, 600))
        self.area.blit(self.gameBoard.getGB(), rect)
        
        while 1:
            self.chatbox.fill((255,255,255))
            #self.board.fill((0,0,0))
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
        
    p2.addDollars(120000000)
    
    return [p1, p2, p3, p4, p5, p6]



    
def main():
    screen = GameArea(0.6)
    screen.play()



if __name__ == "__main__":
    main()








        
        
            
