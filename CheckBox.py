import pygame
from pygame.locals import *
import os
import sys

class CheckBox(object):

    def __init__(self, screen, x, y, w):
        self.screen = screen
        self.x = x #X and Y are the top left corner of square
        self.y = y
        self.w = w #W is how wide and tall the square is
        self.checked = False

    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 255), Rect((self.x, self.y), (self.w, self.w)), 0)
        if self.checked:
            pygame.draw.line(self.screen, (0, 0, 0), (self.x, self.y), (self.x + self.w, self.y + self.w))
            pygame.draw.line(self.screen, (0, 0, 0), (self.x, self.y + self.w), (self.x + self.w, self.y))

    def setChecked(self, x, y):
        if x > self.x and y > self.y and x < self.x + self.w and y < self.y + self.w:
            self.checked = not self.checked
            return True
        return False

    def getChecked(self):
        return self.checked
