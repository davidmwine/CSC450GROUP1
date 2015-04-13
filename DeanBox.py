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
        self.area.fill((54, 27, 123))
        pygame.draw.rect(self.area, (0, 0, 0), (0, 0, self.area.get_width(), self.area.get_height()), 2)

class DeanBoxes(object):
    def __init__(self, parent, font_op, scale, offset, width, height):
        self.parent = parent
        self.font_op = font_op
        self.scale = scale
        self.offset = offset
        self.width = width
        self.height = height
        self.boxes = []

    def newBox(self, rect):
        self.boxes.append(DeanBox(self.parent, rect, self.font_op, self.scale, self.offset))

    def drawBoxes(self, val):
        if val >=2 and val <= 6:
            for i in range(val):
                self.boxes[i].draw()

