import pygame, sys, os
from pygame.locals import *


class DeanBox(object):
    def __init__(self, parent, rect, font_op, scale, offset):
        self.parent = parent
        self.maxLength = 8 #Max length of the string for player name
        self.font_op = font_op
        self.area = parent.subsurface(rect)
        self.scale = scale
        self.offset = offset #Determine click location

    def draw(self):
        self.area.fill((255, 255, 255))
        pygame.draw.rect(self.area, (0, 0, 0), (0, 0, self.area.get_width(), self.area.get_height()), 2)

class DeanBoxes(object):
    def __init__(self, parent, font_op, scale, offset):
        self.parent = parent
        self.font_op = font_op
        self.scale = scale
        self.offset = offset
        self.currPosition = [self.parent.get_width()/4 - self.parent.get_width()/8, self.parent.get_height()/2 - self.parent.get_height()/8]
        self.width = self.parent.get_width()/4 - self.parent.get_width()/16
        self.height = self.parent.get_height()/4
        self.boxes = []

    def newBox(self):
        if len(self.boxes) < 3:
            rect = Rect(self.currPosition[0], self.currPosition[1], self.width, self.height)
            self.boxes.append(DeanBox(self.parent, rect, self.font_op, self.scale, self.offset))
            self.currPosition[0] += self.parent.get_width()/4
        elif len(self.boxes) == 3:
            self.currPosition[0] = self.parent.get_width()/4 - self.parent.get_width()/8
            self.currPosition[1] += self.parent.get_height()/2 - self.parent.get_height()/6
            rect = Rect(self.currPosition[0], self.currPosition[1], self.width, self.height)
            self.boxes.append(DeanBox(self.parent, rect, self.font_op, self.scale, self.offset))
            self.currPosition[0] += self.parent.get_width()/4
        elif len(self.boxes) < 6:
            rect = Rect(self.currPosition[0], self.currPosition[1], self.width, self.height)
            self.boxes.append(DeanBox(self.parent, rect, self.font_op, self.scale, self.offset))
            self.currPosition[0] += self.parent.get_width()/4

    def drawBoxes(self):
        for i in self.boxes:
            i.draw()

