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
        self.help = Button(self.area, Rect((self.width*3/4,0) + buttonwh), "Upgrade") 

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height   


class SignInControls:
    
    def __init__(self, parent, rect):
        self.area = parent.subsurface(rect)
        #print(rect, parent)
        self.width = self.area.get_width()
        self.height = self.area.get_height()
        buttonwh = (self.width/4, self.height)##button width and height
        self.area.fill((0x22, 0x44, 0x66, 0xFF))
        self.menu = Button(self.area, Rect((0,0,) + buttonwh), "Local Game",textSize = 20) 
        self.roll = Button(self.area, Rect((self.width/4,0,) + buttonwh), "Host Game",textSize = 20)
        self.trade = Button(self.area, Rect((self.width*2/4,0) + buttonwh), "Join Game",textSize = 20)
        self.help = Button(self.area, Rect((self.width*3/4,0) + buttonwh), "Delete User", textSize = 20)
        self.buttons = [self.menu,self.roll,self.trade,self.help]
        

    def wasClicked(self,mousex, mousey):
        for i in range(len(self.buttons)):
            if self.buttons[i].wasClicked(mousex, mousey):
                return i+1
        return 0

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def redraw(self):
        for i in self.buttons:
            i.redraw()



class Button:

    def __init__(self, parent, rect, label = "",bgcolor=Colors.LIGHTGRAY, fontcolor=(0, 0, 0), textSize = 30):
        self.area = parent.subsurface(rect)
        self.font = pygame.font.Font( None, textSize)
        self.width = self.area.get_width()
        self.height = self.area.get_height()
        self.left = rect[0]
        self.top = rect[1]
        self.right = rect[2]
        self.bottom = rect[3]
        self.bgcolor = bgcolor
        self.fontcolor = fontcolor
        self.text = label
        

        pygame.draw.rect(self.area, bgcolor, (0,0, self.area.get_width(),
                                              self.area.get_height()))
        self.textarea = self.font.render( self.text, 1, fontcolor)
        self.area.blit(self.textarea,((self.width-self.textarea.get_width())/2,
                                        (self.height - self.textarea.get_height())/2))
        pygame.draw.rect(self.area,(0,0,0), (0,0, self.area.get_width(),
                                              self.area.get_height()), 5)
        #print(rect, parent)
       
    def redraw(self):
        pygame.draw.rect(self.area, self.bgcolor, (0,0, self.area.get_width(),
                                              self.area.get_height()))
        self.textarea = self.font.render( self.text, 1, self.fontcolor)
        self.area.blit(self.textarea,((self.width-self.textarea.get_width())/2,
                                        (self.height - self.textarea.get_height())/2))
        pygame.draw.rect(self.area,(0,0,0), (0,0, self.area.get_width(),
                                              self.area.get_height()), 5)
    def wasClicked(self, mouseX, mouseY):
        xoffset, yoffset = self.area.get_abs_offset()
        return xoffset < mouseX<self.area.get_width() +xoffset \
               and yoffset <mouseY <self.area.get_height() + yoffset
        #return (self.left < mouseX < self.left + self.width) and\
        #        (self.top < mouseY < self.top + self.height)
        
        







