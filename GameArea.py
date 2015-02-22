import pygame, sys
from pygame.locals import *
from player import Player
from building import Building
from globals import Globals
from playersDisplay import PlayersDisplay
from board import GameBoard
from Controls import Controls
from ChatBox import chatBox


class gameArea():


<<<<<<< HEAD
    def __init__(self, scale=1, ischild=False):
        '''Inits a Game area object optional paramaters: float sclale and bool isChild'''
=======
    def __init__(self, parent=False, scale=1):
>>>>>>> origin/development

        self.width = int(scale*1920)
        self.height = int(scale*1080)
        self.scale = scale

        if ischild:
            self.area = pygame.Surface((self.width, self.height))
        else:
            pygame.init()
            self.area = pygame.display.set_mode((self.width, self.height))

        # Game Board
        rect = pygame.Rect((0, 0), (1440*self.scale, 1020*self.scale))
        self.boardArea = self.area.subsurface(rect)
        self.boardArea.fill(Globals.maroon) 

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
<<<<<<< HEAD
        rect = pygame.Rect((1080*self.scale,0), (840*self.scale, 810*self.scale))
        self.area.blit(self.playerDis.getPD(), rect)
        size_rect = pygame.Rect((0*self.scale, 0*self.scale), (360*self.scale,1080*self.scale))
        while 1:
            
            self.board.fill((255,0,0))
            pygame.display.flip()   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:           
=======
        game_exit = False
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
        
        while not game_exit:
            for event in pygame.event.get():
                if event.type == KEYDOWN: #TEMPORARY, will later replace with proper game exit
                    if event.key == K_ESCAPE:
                        game_exit = True
                        break
                elif event.type == pygame.QUIT:
>>>>>>> origin/development
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
<<<<<<< HEAD
        screen = gameArea(.5)
        screen.play()
=======
    screen = GameArea(False, 2/3)
    screen.play()
>>>>>>> origin/development



if __name__ == "__main__":
    main()








        
        
            
