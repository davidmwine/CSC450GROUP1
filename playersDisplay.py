
import pygame
from pygame.locals import *
import sys
import os

from player import Player
from globals import Globals



class PlayersDisplay(object):
    """
    Used for displaying the section of the user interface which contains
    player information.

    In the constructor, 'players' should be a list of Player objects;
    'c' is a scale factor indicating the size the panel should be displayed at
    as a fraction of its maximum size, 480 x 810px (when the whole window
    is 1920 x 1080px);
    'parent' is a boolean value indicating whether this panel has a parent,
    i.e., whether it's being displayed as part of a larger screen.

    Example usage:
    c = 1
    pd = PlayersDisplay(players, c, True)
    rect = pygame.Rect((0,0), (c*480, c*810))
    screen.blit(pd.getPD(), rect)
    """

    def __init__(self, players, c, parent=False):

        self.players = players
        self.width = int(c*480)
        self.height = int(c*810)
        self.playerHeight = int(c*135)

        if parent == False:
            pygame.init()
            self.screen = pygame.display.set_mode((self.width, self.height))

        # The main Surface for the PlayersDisplay, which we'll keep adding to
        self.pd = pygame.Surface((self.width, self.height))
        self.pd = self.pd.convert()
        self.pd.fill(Globals.maroon)

        totalPlayersHeight = self.playerHeight * len(players)
        pygame.draw.rect(self.pd, Globals.lightGray,
                         (0, 0, self.width, totalPlayersHeight), 0)
        for i in range(1, len(players)):
            pygame.draw.lines(self.pd, Globals.maroon, False,
                              [(0, self.playerHeight*i),
                               (self.width, self.playerHeight*i)], 1)
    
        if pygame.font:
            for i in range(len(players)):
                self.printText(c, i)
                  

    def printText(self, c, i):
        if c >= 0.9:
            font = pygame.font.Font(None, 30)
            buildingFont = pygame.font.Font(None, 24)
        elif c >= 0.75:    
            font = pygame.font.Font(None, 24)
            buildingFont = pygame.font.Font(None, 20)
        elif c >= 0.6:
            font = pygame.font.Font(None, 20)
            buildingFont = pygame.font.Font(None, 16)
        else:
            font = pygame.font.Font(None, 16)
            buildingFont = pygame.font.Font(None, 14)
            
                
        text = font.render(self.players[i].getName(),
                           True, Color('black'))
        self.pd.blit(text, (2, self.playerHeight*i + 2))

        college = self.players[i].getCollege()
        
        # For the colleges with light colors, create a black outline.
        if college == 'Natural and Applied Sciences' \
           or college == 'Health and Human Services' \
           or college == 'Education' or college == 'Business':
            textOutline = font.render(Globals.collegeAbbr[college],
                           True, Color('black'))
            self.pd.blit(textOutline, (140*c - 1, self.playerHeight*i + 1))
            self.pd.blit(textOutline, (140*c - 1, self.playerHeight*i + 3))
            self.pd.blit(textOutline, (140*c + 1, self.playerHeight*i + 1))
            self.pd.blit(textOutline, (140*c + 1, self.playerHeight*i + 3))
        
        text = font.render(Globals.collegeAbbr[college],
                           True, Globals.collegeColors[college])
        self.pd.blit(text, (140*c, self.playerHeight*i + 2))
        
        text = font.render('${:,d}'.format(self.players[i].getDollars()),
                           True, Color('black'))
        self.pd.blit(text, (350*c, self.playerHeight*i + 2))
        
        text = font.render(str(self.players[i].getPoints()) + ' pts',
                           True, Color('black'))
        self.pd.blit(text, (20*c, self.playerHeight*i + 30*c))

        text = font.render(str(self.players[i].getPointsPerRound()) + ' pts/round',
                           True, Color('black'))
        self.pd.blit(text, (250*c, self.playerHeight*i + 30*c))
        
        x = 2   # x position to place text of each building
        y = 60*c  # y position to place text (within player's section)
        for building in self.players[i].getBuildings():
            text = buildingFont.render(Globals.buildingAbbr[building], True, Color('black'))
            self.pd.blit(text, (x, y + self.playerHeight*i))
            x += 75*c
            if x >= self.width - 60*c:
                x = 2
                y += 20*c
         

    def getPD(self):
        return self.pd
    
    

def main():

    p1 = Player("player1", "Agriculture")
    p2 = Player("player2", "Arts and Letters")
    p3 = Player("player3", "Natural and Applied Sciences")
    p4 = Player("player4", "Education")
    p5 = Player("player5", "Health and Human Services")
    p6 = Player("player6", "Humanities and Public Affairs")
    
    p1.addBuilding('Siceluff')
    p1.addBuilding('Cheek')
    p1.addBuilding('Plaster Student Union')
    p1.addBuilding('Kemper')
    p1.addBuilding('Strong')
    p1.addBuilding('Karls')
    p1.addBuilding('Glass')
    p1.addBuilding('Ellis')
    p1.addBuilding('JQH Arena')
    p1.addBuilding('McDonald Arena')
    p1.addBuilding('Meyer Library')
    p1.addBuilding('Foster Recreation Center')
    p1.addBuilding('Juanita K Hammons')
    p1.addBuilding('Pummil')
    p1.addBuilding('Plaster Stadium')
    p1.addBuilding('Temple')
    p2.addBuilding('Craig')
    p2.addBuilding('Ellis')

    p2.addDollars(30000000)
    
    players = [p1, p2, p3, p4, p5, p6]
    
    pd = PlayersDisplay(players, 1)

    pd.screen.blit(pd.getPD(), (0, 0))
    pygame.display.flip()
    
    gameActive = True
    while gameActive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameActive = False

    pygame.quit()
    sys.exit()



if __name__ == '__main__':
    main()
