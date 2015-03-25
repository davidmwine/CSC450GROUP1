import pygame, sys, os
from pygame.locals import *
from TextWrap import *


class EntryBox():

    def __init__(self, parent, length, position ,font_op, scale ,start_text = ''):
        self.parent = parent
        self.len = length
        self.font_op = font_op
        self.width, self.height = self.font_op(10, 'berlin').size(" " + "W"*length)
        if self.width > position[2]:
            position = (position[0], position[1], self.width, position[3])
        self.text = start_text
        self.x_start = position[0]
        self.y_start = position[1]
        self.area = parent.subsurface(position)
        self.focus = False
        self.scale = scale

    def draw(self):
        self.area.fill((255,255,255))
        boxText = self.font_op(20*self.scale, 'berlin').render(" " +self.text,1,(0,0,0))
   
        pygame.draw.rect(self.area,(0,0,0), (0,0, self.area.get_width(),
                                              self.area.get_height()), 2)
        self.area.blit(boxText, (0,0))

    def hasFocus(self):
        return self.focus

    def giveFocus(self):
        self.focus = True

    def takeFocus(self):    
        self.focus = False

    def isClicked(self, mousex, mousey):
        if(self.x_start< mousex< self.x_start+self.width) and (self.y_start< mousey< self.y_start+self.height):
           return True
        else:
           return False


class EntryBoxSet():


    def __init__(self, scale):
        self.entryBoxes = dict()
        self.scale = scale
        focused = None

    def createNew(self,parent, length, position , font_op ,start_text = '', name = ''):
        if name == '':
            name = str(len(self.entryBoxes))
        self.entryBoxes[name] = EntryBox(parent, length, position , font_op, self.scale  ,start_text)
        return self.entryBoxes[name]

    def isClicked(mousex,mousey):
        for i in entryBoxes:
            if i.isClicked():
                i.giveFocus()
                if not focused is None:
                    focused.takeFocus
                return i
            
    def getBoxes(self):
        return self.entryBoxes

    def draw(self):
        for i in self.entryBoxes:
            self.entryBoxes.get(i).draw()
    





