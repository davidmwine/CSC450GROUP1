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
        '''self.rect = pygame.Rect((int(self.buildings[self.position].getRect().right - self.scale*50),\
                         int(self.buildings[self.position].getRect().bottom - self.scale*50)),\
                         (self.size, self.size))
        self.token = pygame.draw.rect(self.board, self.color, self.rect)'''

    def moveToken(self, spaces):
        redrawRect = self.buildings[self.position].getRect()
        pygame.draw.rect(self.board, Colors.BLACK, redrawRect, 2)
        redrawImage = pygame.transform.scale(self.buildings[self.position].getImage(),
                                         (int(redrawRect.width - 3), int(redrawRect.height - 3)))
        self.board.blit(redrawImage, (redrawRect.left + 2, redrawRect.top + 2))
        self.prevX = self.rect.left
        self.prevY = self.rect.top
        self.position += spaces     
        numBuildings = Buildings().getNumBuildings()
        self.position %= numBuildings
        
        self.displayToken()

    def displayToken(self):
        if 9 <= self.position <= 15:
            self.rect = pygame.Rect((int(self.buildings[self.position].getRect().right - self.scale*50),\
                             int(self.buildings[self.position].getRect().top + self.scale*8)),\
                             (self.size, self.size))
        elif self.position == 0 or self.position == 24:
            self.rect = pygame.Rect((int(self.buildings[self.position].getRect().left + self.scale*10),\
                             int(self.buildings[self.position].getRect().bottom - self.scale*50)),\
                             (self.size, self.size))
        elif 25 <= self.position <= 31:
            self.rect = pygame.Rect((int(self.buildings[self.position].getRect().left + self.scale*10),\
                             int(self.buildings[self.position].getRect().top + self.scale*8)),\
                             (self.size, self.size))    
        else:
            self.rect = pygame.Rect((int(self.buildings[self.position].getRect().right - self.scale*50),\
                             int(self.buildings[self.position].getRect().bottom - self.scale*50)),\
                             (self.size, self.size)) 
        self.token = pygame.draw.rect(self.board, self.color, self.rect)

    def clearToken(self):
        redrawRect = self.buildings[self.position].getRect()
        pygame.draw.rect(self.board, Colors.BLACK, redrawRect, 2)
        redrawImage = pygame.transform.scale(self.buildings[self.position].getImage(),
                                         (int(redrawRect.width - 3), int(redrawRect.height - 3)))
        self.board.blit(redrawImage, (redrawRect.left + 2, redrawRect.top + 2))
        

    def drawWheel(self, percentage, location):
        angle = percentage*360 #Size of angle
        startAng = angle*location #Where the angle starts on the wheel
        stopAng = startAng + angle #Where angle ends on the wheel
        if self.position == 0 or self.position == 24 or 9 <= self.position <= 15:
            wheelRect = pygame.Rect((int(self.buildings[self.position].getRect().right - self.scale*50),\
                                 int(self.buildings[self.position].getRect().bottom - self.scale*45)),\
                                 (self.size, self.size))
        else:
            wheelRect = pygame.Rect((int(self.buildings[self.position].getRect().left + self.scale*10),\
                             int(self.buildings[self.position].getRect().bottom - self.scale*45)),\
                             (self.size, self.size))
        
        pygame.draw.arc(self.board, self.color, wheelRect, startAng*math.pi/180, stopAng*math.pi/180, self.size//2)
        '''for d in range(int(startAng), int(stopAng)):
            pygame.draw.line(self.board, self.color, (self.buildings[self.position].getRect().left + 30*self.scale, \
                                                      self.buildings[self.position].getRect().bottom - 30*self.scale),\
                             (self.buildings[self.position].getRect().left + 30*self.scale + 20*self.scale*math.cos(d*math.pi/180),\
                              self.buildings[self.position].getRect().bottom - 30*self.scale + 20*self.scale*math.sin(d*math.pi/180)), 1)'''
        
        
