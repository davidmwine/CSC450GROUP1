import pygame, sys, os
from pygame.locals import *
from textWrap import *


class EntryBox():

    def __init__(self, parent, length, position , font_op ,start_text = ''):
        self.parent = parent
        self.len = length
        self.font_op = font_op
        self.width, self.height = font_op(10, 'berlin').size("W"*length)
        self.text = start_text
        self.x_start = position[0]
        self.y_start = position[1]
        self.area = parent.subsurface(positon)
        self.focus = False


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


    def __init__(self):
        self.entryBoxes = dict()
        focused = None

    def createNew(self,parent, length, position , font_op , name = '',start_text = ''):
        if name == '':
            name = str(len(entryBoxes))
        self.entryBoxes[name] = EntryBox(parent, length, position , font_op, start_text)

    def isClicked(mousex,mousey):
        for i in entryBoxes:
            if i.isClicked():
                i.giveFocus()
                if not focused is None:
                    focused.takeFocus
                return i
    





