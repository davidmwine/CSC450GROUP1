import pygame, sys
from pygame.locals import *
from playersDisplay import PlayersDisplay
from player import Player
from building import Building
from boardJB import GameBoard
from Controls import Controls
from ChatBox import chatBox


class gameArea():


    def __init__(self, parent=False, scale=1):

        self.width = int(scale*1920)
        self.height = int(scale*1080)
        self.scale = scale
        self.parent = parent

        if self.parent:
            self.area = pygame.Surface((self.width, self.height))
        else:
            pygame.init()
            self.area = pygame.display.set_mode((self.width, self.height))

        # Game Board
        rect = pygame.Rect((0, 0), (1440*self.scale, 1020*self.scale))
        self.boardArea = self.area.subsurface(rect)
        self.boardArea.fill((80, 0, 0))

        self.gameBoard = GameBoard(self.scale, True)
            
        # Players Display
        self.playerDis = PlayersDisplay(testplayers(), self.scale, True)

        # Chat Box
        rect = pygame.Rect((1440*self.scale, 810*self.scale),
                           (480*self.scale, 270*self.scale))
        self.chatbox = chatBox(1,self.area, rect)
        
        # Controls
        rect = pygame.Rect((0, 1020*self.scale),
                           (1440*self.scale, 60*self.scale))
        self.controls = Controls(self.area, rect)


    def get_area(self):
        return self.area


    def play(self):

        # Insert Players Display
        rect = pygame.Rect((1440*self.scale, 0),
                           (480*self.scale, 810*self.scale))
        self.area.blit(self.playerDis.getPD(), rect)

        # Insert Game Board
        rect = pygame.Rect((20*self.scale, 20*self.scale),
                           (1400*self.scale, 980*self.scale))
        self.area.blit(self.gameBoard.getGB(), rect)

        if self.parent:
            self.parent.blit(self.area, (0,0))
        
        while 1:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
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
    screen = gameArea(False, 2/3)
    screen.play()



if __name__ == "__main__":
    main()








        
        
            
