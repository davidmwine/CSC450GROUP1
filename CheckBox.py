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
        pygame.draw.rect(self.screen, (255, 255, 255), Rect((self.x, self.y), (self.w, self.w)), 0)
        if self.checked:
            pygame.draw.line(self.screen, (0, 0, 0), (self.x, self.y), (self.x + self.w, self.y + self.w))
            pygame.draw.line(self.screen, (0, 0, 0), (self.x, self.y + self.w), (self.x + self.w, self.y))

    def setChecked(self, x, y):
        '''setChecked(x, y) takes an x and y location of a clicked mouse, and
        if there is a checkbox in that location, the checkbox is set to checked'''
        if x > self.x and y > self.y and x < self.x + self.w and y < self.y + self.w:
            self.checked = not self.checked
            return True
        return False

    def getChecked(self):
        '''getChecked() returns the value of self.checked'''
        return self.checked
