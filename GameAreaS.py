import pygame, sys
from pygame.locals import *
from playersDisplayS import PlayersDisplay
from player import Player
from ChatBox import chatBox
from Controls import Controls


class gameArea():


    def __init__(self, scale=1, ischild=False):
        '''Inits a Game area object optional paramaters: float sclale and bool isChild'''

        self.width = int(scale*1920)
        self.height = int(scale*1080)
        self.scale = scale

        if ischild:
            self.area = pygame.Surface((self.width, self.height))
        else:
            pygame.init()
            self.area = pygame.display.set_mode((self.width, self.height))
            

        self.playerDis = PlayersDisplay(testplayers(), scale, 1)
        
        size_rect = pygame.Rect((1080*scale, 810*self.scale), (840*self.scale,270*self.scale))
        self.chatbox = chatBox(1,self.area, size_rect)
        
        size_rect = pygame.Rect((0*scale, 0*self.scale), (1080*self.scale,1020*self.scale))
        self.board   = self.area.subsurface(size_rect)
        size_rect = pygame.Rect((0*scale, 1020*self.scale), (1080*self.scale,60*self.scale))
        self.controls = Controls(self.area, size_rect)

        
        



    def get_area(self):
        return self.area


    def play(self):
        rect = pygame.Rect((1080*self.scale,0), (840*self.scale, 810*self.scale))
        self.area.blit(self.playerDis.getPD(), rect)
        size_rect = pygame.Rect((0*self.scale, 0*self.scale), (360*self.scale,1080*self.scale))
        while 1:
            
            self.board.fill((255,0,0))
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
        screen = gameArea(.65)
        screen.play()



if __name__ == "__main__":
        main()








        
        
            
