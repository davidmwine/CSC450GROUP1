
import pygame
from pygame.locals import *
import sys
import os

from Player import Player
import Colors


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
        self.scale = c
        self.width = int(c*480)
        self.height = int(c*810)
        self.playerHeight = int(c*135)
        
        # If this isn't called by another screen, make this the main screen.
        if parent == False:
            pygame.init()
            self.screen = pygame.display.set_mode((self.width, self.height))

        # The main Surface for the PlayersDisplay, which we'll keep adding to
        self.playersDisplay = pygame.Surface((self.width, self.height))
        self.playersDisplay = self.playersDisplay.convert()
        self.playersDisplay.fill(Colors.MAROON)

        # Add black background so it looks better when players go bankrupt
        totalPlayersHeight = self.playerHeight * len(players)
        pygame.draw.rect(self.playersDisplay, Color('black'),
                         (0, 0, self.width, totalPlayersHeight), 0)

        # Create separate a separate surface for each player so we can
        # use set_alpha on it when a player goes bankrupt.
        self.pd = []
        for i in range(len(self.players)):
            self.pd.append(pygame.Surface((self.width, self.playerHeight)))
            self.pd[i].fill(Colors.LIGHTGRAY)            
            pygame.draw.rect(self.pd[i], Colors.MEDGRAY,
                         (0, 0, self.width, 45*c), 0)
            pygame.draw.lines(self.pd[i], Colors.MAROON, False,
                              [(0, 0), (self.width, 0)], 2)

            # Add text.
            self.printText(c, i)

            # Darken the sections of bankrupt players.
            if self.players[i].isBankrupt:
                self.pd[i].set_alpha(100)
                
            # Blit the player surfaces onto the main surface.
            rect = (0, i*self.playerHeight, self.width, self.playerHeight)
            self.playersDisplay.blit(self.pd[i], rect)        
                  

    def printText(self, c, i):
        """Prints the appropriate text in the i^th player's section."""
        
        font = pygame.font.Font(None, int(40*c))

        # Player name  
        text = font.render(self.players[i].getName(),
                           True, Color('black'))
        self.pd[i].blit(text, (4, 4))

        # College name
        college = self.players[i].getCollege()
        
        # For the colleges with light colors, create a black outline.
        if college == 'Natural and Applied Sciences' \
           or college == 'Health and Human Services' \
           or college == 'Education' or college == 'Business':
            textOutline = font.render(Colors.COLLEGEABBR[college],
                           True, Color('black'))
            self.pd[i].blit(textOutline, (220*c - 1, 5))
            self.pd[i].blit(textOutline, (220*c - 1, 3))
            self.pd[i].blit(textOutline, (220*c + 1, 5))
            self.pd[i].blit(textOutline, (220*c + 1, 3))
        
        text = font.render(Colors.COLLEGEABBR[college],
                           True, Colors.COLLEGECOLORS[college])
        self.pd[i].blit(text, (220*c, 4))

        # Points
        points = self.players[i].getPoints()
        if points == 1:
            text = font.render(str(points) + ' point', True, Color('black'))
        else:
            text = font.render(str(points) + ' points', True, Color('black'))
        self.pd[i].blit(text, (20*c, 50*c))
        
        # Points per round
        points = self.players[i].getPointsPerRound()
        if points == 1:
            text = font.render(str(points) + ' point / round', True, Color('black'))
        else:
            text = font.render(str(points) + ' points / round', True, Color('black'))
        self.pd[i].blit(text, (250*c, 50*c))

        # Dollars
        text = font.render('${:,.0f}'.format(self.players[i].getDollars()),
                           True, Color('black'))
        self.pd[i].blit(text, (20*c, 90*c))


    def selectPlayer(self, playerIndex):
        """
        Uses light maroon to highlight a player's section
        (for indicating it's his/her turn).
        """
        self.pd[playerIndex].fill((238, 180, 180))
        pygame.draw.rect(self.pd[playerIndex], (205, 155, 155),
            (0, 2, self.width, 45*self.scale), 0)
        pygame.draw.lines(self.pd[playerIndex], Colors.MAROON, False,
                              [(0, 0), (self.width, 0)], 2)
        self.printText(self.scale, playerIndex)
        rect = (0, playerIndex*self.playerHeight, self.width, self.playerHeight)
        self.playersDisplay.blit(self.pd[playerIndex], rect)


    def updatePlayer(self, playerIndex):
        """
        Updates a player's displayed information to reflect current data.
        Also used to return a player's section to gray after it has been selected.
        """
        self.pd[playerIndex].fill(Colors.LIGHTGRAY)
        pygame.draw.rect(self.pd[playerIndex], Colors.MEDGRAY,
            (0, 2, self.width, 45*self.scale), 0)
        pygame.draw.lines(self.pd[playerIndex], Colors.MAROON, False,
                              [(0, 0), (self.width, 0)], 2)
        self.printText(self.scale, playerIndex)
        rect = (0, playerIndex*self.playerHeight, self.width, self.playerHeight)
        self.playersDisplay.blit(self.pd[playerIndex], rect)
        
              
    def getPD(self):
        return self.playersDisplay
    
    

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

    pd.selectPlayer(0)
    pd.unselectPlayer(0)
    pd.selectPlayer(1)

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
