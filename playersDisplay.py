
import pygame
from pygame.locals import *
import sys
import os

from player import Player
from globals import Globals
from building import Building



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

        # Colors
        maroon = (80, 0, 0)
        lightGray = (200, 200, 200)
        medGray = (180, 180, 180)
        
        # If this isn't called by another screen, make this the main screen.
        if parent == False:
            pygame.init()
            self.screen = pygame.display.set_mode((self.width, self.height))

        # The main Surface for the PlayersDisplay, which we'll keep adding to
        self.pd = pygame.Surface((self.width, self.height))
        self.pd = self.pd.convert()
        self.pd.fill(maroon)

        # Add gray background for player data & separate with lines.
        totalPlayersHeight = self.playerHeight * len(players)
        pygame.draw.rect(self.pd, lightGray,
                         (0, 0, self.width, totalPlayersHeight), 0)
        for i in range(0, len(players)):
            pygame.draw.rect(self.pd, medGray,
                         (0, i*self.playerHeight, self.width, 45*c), 0)
            pygame.draw.lines(self.pd, maroon, False,
                              [(0, self.playerHeight*i),
                               (self.width, self.playerHeight*i)], 2)

        # Add text.
        if pygame.font:
            for i in range(len(players)):
                self.printText(c, i)
                  

    def printText(self, c, i):

        font = pygame.font.Font(None, int(40*c))

        # Player name  
        text = font.render(self.players[i].getName(),
                           True, Color('black'))
        self.pd.blit(text, (2, self.playerHeight*i + 4))

        # College name
        college = self.players[i].getCollege()
        
        # For the colleges with light colors, create a black outline.
        if college == 'Natural and Applied Sciences' \
           or college == 'Health and Human Services' \
           or college == 'Education' or college == 'Business':
            textOutline = font.render(Globals.collegeAbbr[college],
                           True, Color('black'))
            self.pd.blit(textOutline, (220*c - 1, self.playerHeight*i + 5))
            self.pd.blit(textOutline, (220*c - 1, self.playerHeight*i + 3))
            self.pd.blit(textOutline, (220*c + 1, self.playerHeight*i + 5))
            self.pd.blit(textOutline, (220*c + 1, self.playerHeight*i + 3))
        
        text = font.render(Globals.collegeAbbr[college],
                           True, Globals.collegeColors[college])
        self.pd.blit(text, (220*c, self.playerHeight*i + 4))

        # Points
        text = font.render(str(self.players[i].getPoints()) + ' pts',
                           True, Color('black'))
        self.pd.blit(text, (20*c, self.playerHeight*i + 50*c))
        
        # Points per round
        text = font.render(str(self.players[i].getPointsPerRound()) + ' pts/round',
                           True, Color('black'))
        self.pd.blit(text, (250*c, self.playerHeight*i + 50*c))

        # Dollars
        text = font.render('${:,d}'.format(self.players[i].getDollars()),
                           True, Color('black'))
        self.pd.blit(text, (20*c, self.playerHeight*i + 90*c))

              
    def getPD(self):
        return self.pd
    
    

def main():

    p1 = Player("player1", "Agriculture")
    p2 = Player("player2", "Arts and Letters")
    p3 = Player("player3", "Natural and Applied Sciences")
    p4 = Player("player4", "Education")
    p5 = Player("player5", "Health and Human Services")
    p6 = Player("player6", "Humanities and Public Affairs")
    
    p2.addDollars(120000000)
    
    players = [p1, p2, p3, p4, p5, p6]
    
    pd = PlayersDisplay(players, 0.7)

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
