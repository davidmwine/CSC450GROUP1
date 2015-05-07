import pygame
from pygame.locals import *
import os
import sys

class CheckBox(object):

    def __init__(self, screen, x, y, w):
        '''CheckBox(screen, x, y, w) takes a screen to be displayed
        on, an x and y value for the top left corner of the checkbox, and
        width for the size of the checkbox'''
        self.screen = screen
        self.x = x #X and Y are the top left corner of square
        self.y = y
        self.w = w #W is how wide and tall the square is
        self.checked = False

    def draw(self):
        '''draw() draws the checkbox, and an x in the middle if the checkbox is checked'''
        pygame.draw.rect(self.screen, (200,200,200), Rect((self.x, self.y), (self.w, self.w)), 0)
        pygame.draw.rect(self.screen, (0, 0, 0), Rect((self.x, self.y), (self.w, self.w)), 1)
        if self.checked:
            pygame.draw.rect(self.screen, (0, 0, 0), Rect((self.x + self.w/10, self.y + self.w/10), \
                                                          (self.w - self.w/5, self.w - self.w/5)), 0)
            #pygame.draw.line(self.screen, (0, 0, 0), (self.x, self.y), (self.x + self.w, self.y + self.w), 2)
            #pygame.draw.line(self.screen, (0, 0, 0), (self.x, self.y + self.w), (self.x + self.w, self.y), 2)

    def setChecked(self, x, y):
        '''setChecked(x, y) takes an x and y location of a clicked mouse, and
        if there is a checkbox in that location, the checkbox is set to checked'''
        if x > self.x and y > self.y and x < self.x + self.w and y < self.y + self.w:
            self.checked = not self.checked
            return True
        return False

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self, val):
        self.x = val

    def setY(self, val):
        self.y = val

    def getChecked(self):
        '''getChecked() returns the value of self.checked'''
        return self.checked

    def undoChecked(self):
        self.checked = False

    def changePosition(self, x, y, w, screen):
        self.screen = screen
        self.x = x
        self.y = y
        self.w = w
        
