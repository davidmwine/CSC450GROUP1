import pygame
from pygame.locals import *
import os
import sys

class RadioButton(object):
    def __init__(self, screen, x, y, r):
        '''RadioButton(screen, x, y, r) takes a screen to be
        displayed on, an x and y for the center of the radio button,
        and a radius for the radio button.'''
        self.screen = screen
        self.x = int(x) #X and Y represent center of button
        self.y = int(y)
        self.r = r #R is the radius of the button
        #pygame.draw.circle(self.screen, (255, 255, 255), (self.x, self.y), self.r, 0)

    def getX(self):
        '''getX() returns the x value of the center of the button'''
        return self.x

    def getY(self):
        '''getY() returns the y value of the center of the button'''
        return self.y

    def getR(self):
        '''getR() returns the radius of the button'''
        return self.r

    def set(self):
        '''set() sets the radio button to selected'''
        pygame.draw.circle(self.screen, (0, 255, 0), (self.x, self.y), self.r, 0)

    def unSet(self):
        '''unSet() sets the radio button to false'''
        pygame.draw.circle(self.screen, (255, 255, 255), (self.x, self.y), self.r, 0)

class RadioGroup(object):
    def __init__(self, screen):
        '''RadioGroup(screen) takes a screen and can be used to create
        a group of radio buttons on that screen'''
        self.screen = screen
        self.buttons = []
        self.current = 0

    def newButton(self, x, y, r):
        '''newButton(x, y, r) creates a new radio button with
        a given x and y center, and a given radius r.'''
        self.buttons.append(RadioButton(self.screen, x, y, r))

    def draw(self):
        '''draw() makes sure the currently selected button
        is the only one highlighted'''
        for i in range(len(self.buttons)):
            if self.current == i:
                self.buttons[i].set()
            else:
                self.buttons[i].unSet()

    def getCurrent(self):
        '''getCurrent() returns the currently selected button'''
        return self.current

    def setCurrent(self, i):
        '''setCurrent(i) sets the ith button to be the current button'''
        if len(self.buttons)-1 >= i:
            self.current = i
            self.buttons[self.current].set()

    def inArea(self, b, x, y):
        '''inArea(b, x, y) takes a button b, and checks if the given
        x, y coordinate is within its area'''
        if ((x-b.getX())**2 + (y-b.getY())**2)**(0.5) < b.getR():
            return True
        return False

    def checkButton(self, x, y):
        '''checkButton(x, y) takes and x, y coordinate and if
        the coordinate is within the area of one of the buttons
        that button is set to current'''
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
            return True
        return False
