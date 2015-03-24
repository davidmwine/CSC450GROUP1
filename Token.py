import pygame
from pygame.locals import *
from Building import Buildings
import Colors
import math

class Token(object):
    '''Token(playerColor, position, scale = 1) takes a player color,
    a position, a gameboard, a list of buildings, and a scale factor with a default
    value of 1. Then creates a token that will display on the board.'''
    def __init__(self, playerColor, position, board, buildings, scale = 1):
        self.color = playerColor
        self.position = position
        self.board = board
        self.buildings = buildings
        self.scale = scale
        self.size = int(self.scale*40)
        self.rect = pygame.Rect((int(self.buildings[self.position].getRect().right - self.scale*50),\
                         int(self.buildings[self.position].getRect().bottom - self.scale*50)),\
                         (self.size, self.size))
        self.token = pygame.draw.rect(self.board, self.color, self.rect)

    def moveToken(self, spaces):
        redrawRect = self.buildings[self.position].getRect()
        pygame.draw.rect(self.board, self.buildings[self.position].getBuildingColor(), redrawRect)
        pygame.draw.rect(self.board, Colors.BLACK, redrawRect, 2)
        self.prevX = self.rect.left
        self.prevY = self.rect.top
        self.position += spaces
        numBuildings = Buildings().getNumBuildings()
        self.position %= numBuildings
        self.rect = self.rect.move(int(self.buildings[self.position].getRect().right - self.scale*50 - self.prevX),\
                         int(self.buildings[self.position].getRect().bottom - self.scale*50 - self.prevY))
        self.token = pygame.draw.rect(self.board, self.color, self.rect)

    def drawWheel(self, percentage, location):
        angle = percentage*360 #Size of angle
        startAng = angle*location #Where the angle starts on the wheel
        stopAng = startAng + angle #Where angle ends on the wheel
        wheelRect = pygame.Rect((int(self.buildings[self.position].getRect().left + self.scale*10),\
                         int(self.buildings[self.position].getRect().bottom - self.scale*50)),\
                         (self.size, self.size))
        
        pygame.draw.arc(self.board, self.color, wheelRect, startAng*math.pi/180, stopAng*math.pi/180, self.size//2)
        
        