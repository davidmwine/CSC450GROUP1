import pygame, sys, os
from pygame.locals import *
from TextWrap import *


class EntryBox():

    def __init__(self, parent, length, position ,font_op, scale , offset, start_text = ''):
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
        self.offset = offset #For isClick to know proper location
        self.maxChar = -1

    def draw(self):
        self.area.fill((255,255,255))
        boxText = self.font_op(20*self.scale, 'berlin').render(" " +self.text,1,(0,0,0))
   
        pygame.draw.rect(self.area,(0,0,0), (0,0, self.area.get_width(),
                                              self.area.get_height()), 2)
        self.area.blit(boxText, (0,0))

    def setMaxChar(self, num):
        self.maxChar = num

    def getMaxChar(self):
        return self.maxChar

    def getText(self):
        return self.text

    def setText(self, entry = ""):
        self.text = entry

    def deleteText(self):
        self.text = self.text[:-1]

    def hasFocus(self):
        return self.focus

    def giveFocus(self):
        self.focus = True

    def takeFocus(self):    
        self.focus = False

    def isClicked(self, mousex, mousey):
        if(self.x_start< mousex-self.offset[0]< self.x_start+self.area.get_width()) and (self.y_start< mousey-self.offset[1]< self.y_start+self.area.get_height()):
           return True
        else:
           return False


class EntryBoxSet():


    def __init__(self, scale):
        self.entryBoxes = dict()
        self.scale = scale
        self.focused = None

    def createNew(self,parent, length, position , font_op , offset,start_text = '', name = ''):
        if name == '':
            name = str(len(self.entryBoxes))
        self.entryBoxes[name] = EntryBox(parent, length, position , font_op, self.scale, offset ,start_text)
        return self.entryBoxes[name]

    def isClicked(self, mousex, mousey):
        result = False
        for i in self.entryBoxes.keys():
            if self.entryBoxes[i].isClicked(mousex, mousey):
                result = True
                self.entryBoxes[i].giveFocus()
                if not self.focused is None:
                    self.focused.takeFocus()
                self.focused = self.entryBoxes[i]
        return result
            
    def getBoxes(self):
        return self.entryBoxes

    def getBox(self, name):
        return self.entryBoxes[name]

    def getFocused(self):
        return self.focused

    def draw(self, val = -1):
        if val > -1: #KEYS MUST BE STRINGS OF INTEGERS IN ORDER OF BEING CREATED TO WORK
            for i in range(val):
                self.entryBoxes.get(str(i)).draw()
        else:
            for i in self.entryBoxes:
                self.entryBoxes.get(i).draw()
    





