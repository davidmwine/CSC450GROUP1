import pygame, sys
from pygame.locals import *
from playersDisplay import PlayersDisplay



class gameArea():


    def __init__(self, scale, ischild=False):

        self.width = int(scale*1980)
        self.height = int(scale*1080)

        if ischild:
            self.area = pygame.Surface((self.width, self.height))
        else:
            pygame.init()
            self.screen = pygame.display.set_mode((self.width, self.height))
            

        self.playersDisplay = PlayersDisplay(players, scale, 1)
        size_rect = pygame.Rect((0, 900), (1400,180))
        self.chatbox = self.area.subscreen(size_rect)
        
        #self.controls
        #self.board

        
        



    def get_area(self):
        return self.area


    def play(self):
       while 1:
        self.chatbox.fill((255,255,255))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0 
        


    
def main():
    screen = gameArea(1)
    screen.play()



if __name__ == "__main__":
    main()








        
        
            
