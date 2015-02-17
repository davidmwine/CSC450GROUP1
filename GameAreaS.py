import pygame, sys
from pygame.locals import *
from playersDisplayS import PlayersDisplay
from player import Player
from ChatBox import chatBox
from Controls import Controls
from boardS import GameBoard


class GameArea(object):


    def __init__(self, parent=False, scale=1):
        '''Inits a Game area object optional paramaters: float sclale and bool isChild'''

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
        rect = pygame.Rect((0, 0), (1080*self.scale, 1020*self.scale))
        self.boardArea = self.area.subsurface(rect)
        self.boardArea.fill((80,0,0))

        self.gameBoard = GameBoard(self.scale, True)

        # Players Display
        self.playerDis = PlayersDisplay(testplayers(), self.scale, True)

        # Chat Box
        rect = pygame.Rect((1080*scale, 810*self.scale), (840*self.scale,270*self.scale))
        self.chatbox = chatBox(1,self.area, rect)
        
        # Controls
        rect = pygame.Rect((0, 1020*self.scale), (1080*self.scale,60*self.scale))
        self.controls = Controls(self.area, rect)


    def get_area(self):
        return self.area


    def play(self):
        game_exit = False

        # Insert Players Display
        rect = pygame.Rect((1080*self.scale,0), (840*self.scale, 810*self.scale))
        self.area.blit(self.playerDis.getPD(), rect)
        
        # Insert Game Board
        rect = pygame.Rect((0, 0),
                           (1080*self.scale, 1020*self.scale))
        self.area.blit(self.gameBoard.getGB(), rect)
        
        if self.parent:
            self.parent.blit(self.area, (0,0))
        
        while not game_exit: 
            for event in pygame.event.get():
                if event.type == KEYDOWN: #TEMPORARY, will later replace with proper game exit
                    if event.key == K_ESCAPE:
                        game_exit = True
                        break
                elif event.type == pygame.QUIT:           
                    pygame.quit()
                    sys.exit()
                    return 0 
            pygame.display.update()
        return "start"

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
    screen = gameArea(False, 0.65)
    screen.play()



if __name__ == "__main__":
    main()








        
        
            
