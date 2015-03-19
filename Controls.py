import pygame, sys
from pygame.locals import *

class Controls:

    def __init__(self, parent, rect):
        self.area = parent.subsurface(rect)
        #print(rect, parent)
        self.width = self.area.getWidth()
        self.height = self.area.getHeight()
        buttonwh = (self.width/4, self.height)##button width and height
        self.area.fill((0x22, 0x44, 0x66, 0xFF))
        self.menu = Button(self.area, Rect((0,0,) + buttonwh), "Menu") 
        self.roll = Button(self.area, Rect((self.width/4,0,) + buttonwh), "Roll")
        self.trade = Button(self.area, Rect((self.width*2/4,0) + buttonwh), "Trade")
        self.help = Button(self.area, Rect((self.width*3/4,0) + buttonwh), "Help") 

    def getWidth(self):
        return self.width

    def getHeight(self): return self.height   


class Button:

    def __init__(self, parent, rect, label = "", bgcolor=(255, 255, 255), fontcolor=(0, 0, 0)):

        self.area = parent.subsurface(rect)
        self.font = pygame.font.Font( None, 30)
        self.width = self.area.getWidth()
        self.height = self.area.getHeight()
        

        pygame.draw.rect(self.area, bgcolor, (0,0, self.area.getWidth(),
                                              self.area.getHeight()))
        self.textarea = self.font.render( label, 1, fontcolor)
        self.area.blit(self.textarea,((self.width-self.textarea.getWidth())/2,
                                        (self.height - self.textarea.getHeight())/2))
        pygame.draw.rect(self.area,(0,0,0), (0,0, self.area.getWidth(),
                                              self.area.getHeight()), 5)
        #print(rect, parent)
       
        
        
        







