import pygame
from pygame.locals import *
import os
import sys

class RadioButton(object):
    def __init__(self, screen, x, y, r):
        self.screen = screen
        self.x = int(x) #X and Y represent center of button
        self.y = int(y)
        self.r = r #R is the radius of the button
        #pygame.draw.circle(self.screen, (255, 255, 255), (self.x, self.y), self.r, 0)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getR(self):
        return self.r

    def set(self):
        pygame.draw.circle(self.screen, (0, 255, 0), (self.x, self.y), self.r, 0)

    def unSet(self):
        pygame.draw.circle(self.screen, (255, 255, 255), (self.x, self.y), self.r, 0)

class RadioGroup(object):
    def __init__(self, screen):
        self.screen = screen
        self.buttons = []
        self.current = 0

    def newButton(self, x, y, r):
        self.buttons.append(RadioButton(self.screen, x, y, r))

    def draw(self):
        for i in range(len(self.buttons)):
            if self.current == i:
                self.buttons[i].set()
            else:
                self.buttons[i].unSet()

    def getCurrent(self):
        return self.current

    def setCurrent(self, i):
        if len(self.buttons)-1 > i:
            self.current = i
            self.buttons[self.current].set()

    def inArea(self, b, x, y):
        if ((x-b.getX())**2 + (y-b.getY())**2)**(0.5) < b.getR():
            return True
        return False

    def checkButton(self, x, y):
        temp = self.current
        for i in range(len(self.buttons)):
            if self.inArea(self.buttons[i], x, y):
                if self.current != i:
                    self.current = i
                    self.buttons[i].set()
        if temp != self.current:
            for i in range(len(self.buttons)):
                if i != self.current:
                    self.buttons[i].unSet()
