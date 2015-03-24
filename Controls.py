import pygame, sys
from pygame.locals import *
import Colors

class Controls:

    def __init__(self, parent, rect):
        self.area = parent.subsurface(rect)
        #print(rect, parent)
        self.width = self.area.get_width()
        self.height = self.area.get_height()
        buttonwh = (self.width/4, self.height)##button width and height
        self.area.fill((0x22, 0x44, 0x66, 0xFF))
        self.menu = Button(self.area, Rect((0,0,) + buttonwh), "Menu") 
        self.roll = Button(self.area, Rect((self.width/4,0,) + buttonwh), "Roll")
        self.trade = Button(self.area, Rect((self.width*2/4,0) + buttonwh), "Trade")
        self.help = Button(self.area, Rect((self.width*3/4,0) + buttonwh), "Help") 

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height   


class Button:

    def __init__(self, parent, rect, label = "", bgcolor=Colors.LIGHTGRAY, fontcolor=(0, 0, 0)):

        self.area = parent.subsurface(rect)
        self.font = pygame.font.Font( None, 30)
        self.width = self.area.get_width()
        self.height = self.area.get_height()
        

        pygame.draw.rect(self.area, bgcolor, (0,0, self.area.get_width(),
                                              self.area.get_height()))
        self.textarea = self.font.render( label, 1, fontcolor)
        self.area.blit(self.textarea,((self.width-self.textarea.get_width())/2,
                                        (self.height - self.textarea.get_height())/2))
        pygame.draw.rect(self.area,(0,0,0), (0,0, self.area.get_width(),
                                              self.area.get_height()), 5)
        #print(rect, parent)
       
        
        
        







