import pygame, sys
from pygame.locals import *




class Controls:

    def __init__(self, parent, rect):
        self._area = parent.subsurface(rect)
        print(rect, parent)
        self._width = self._area.get_width()
        self._height = self._area.get_height()
        button_w_h = (self._width/4, self._height)
        self._area.fill((0x22, 0x44, 0x66, 0xFF))
        self._menu = Button(self._area, Rect((0,0,)+button_w_h), "Menu") 
        self._roll = Button(self._area, Rect((self._width/4,0,)+button_w_h), "Roll")
        self._trade = Button(self._area, Rect((self._width*2/4,0)+button_w_h), "Trade")
        self._help = Button(self._area, Rect((self._width*3/4,0)+button_w_h), "Help") 
    


class Button:

    def __init__(self, parent, rect, label = ""):

        self._area = parent.subsurface(rect)
        self._font = pygame.font.Font( None, 30)
        self._width = self._area.get_width()
        self._height = self._area.get_height()
        
        self._textarea = self._font.render( label, 1, (0,0,0),(0x22, 0x44, 0x66, 0xFF) )
        self._area.blit(self._textarea,((self._width-self._textarea.get_width())/2,
                                        (self._height - self._textarea.get_height())/2))
        pygame.draw.rect(self._area,(0,0,0), (0,0, self._area.get_width(),
                                              self._area.get_height()), 5)
        #print(rect, parent)
       
        
        
        







