
import pygame
from pygame.locals import *

from player import Player
from globals import Globals



class PlayersDisplay(object):

    def __init__(self, players, parent=None):

        self.players = players

        if parent == None:
            pygame.init()
            self.screen = pygame.display.set_mode((200, 510))

        self.pd = pygame.Surface((200, 510))
        self.pd = self.pd.convert()
        self.pd.fill(Globals.maroon)

        totalHeight = 85 * len(players)
        pygame.draw.rect(self.pd, Globals.lightGray, (0, 0, 200, totalHeight), 0)
        for i in range(1, len(players)):
            pygame.draw.lines(self.pd, Globals.maroon, False, [(0,85*i), (200,85*i)], 1)

        if pygame.font:
            for i in range(len(players)):
                self.printText(i)
                  

    def printText(self, i):
        font = pygame.font.Font(None, 20)
        
        text = font.render(self.players[i].getName(),
                           True, Color('black'))
        self.pd.blit(text, (0, 85*i))

        college = self.players[i].getCollege()

        # For the colleges with light colors, create a black outline.
        if college == 'Natural and Applied Sciences' \
           or college == 'Health and Human Services' \
           or college == 'Education' or college == 'Business':
            textOutline = font.render(Globals.collegeAbbr[college],
                           True, Color('black'))
            self.pd.blit(textOutline, (74, 85*i - 1))
            self.pd.blit(textOutline, (74, 85*i + 1))
            self.pd.blit(textOutline, (76, 85*i - 1))
            self.pd.blit(textOutline, (76, 85*i + 1))
            
        text = font.render(Globals.collegeAbbr[college],
                           True, Globals.collegeColors[college])
        self.pd.blit(text, (75, 85*i))

        text = font.render('$' + str(self.players[i].getDollars()),
                           True, Color('black'))
        self.pd.blit(text, (125, 85*i))
        
        text = font.render(str(self.players[i].getPoints()) + ' pts',
                           True, Color('black'))
        self.pd.blit(text, (20, 18+85*i))

        text = font.render(str(self.players[i].getPointsPerRound()) + ' pts/round',
                           True, Color('black'))
        self.pd.blit(text, (110, 18+85*i))

        x = 0   # x position to place text of each building
        y = 36  # y position to place text (within player's section)
        for building in self.players[i].getBuildings():
            text = font.render(Globals.buildingAbbr[building], True, Color('black'))
            self.pd.blit(text, (x, y+85*i))
            x += 50
            if x >= 200:
                x = 0
                y += 16

    def getPD(self):
        return self.pd
    

def main():

    p1 = Player("player1", "Agriculture")
    p2 = Player("player2", "Arts and Letters")
    p3 = Player("player3", "Natural and Applied Sciences")
    p4 = Player("player4", "Health and Human Services")
    p5 = Player("player5", "Humanities and Public Affairs")
    p6 = Player("player6", "Education")
    
    p1.addBuilding('Siceluff')
    p1.addBuilding('Cheek')
    p1.addBuilding('Plaster Student Union')
    p1.addBuilding('Kemper')
    p1.addBuilding('Glass')
    p1.addBuilding('Strong')
    p1.addBuilding('Karls')
    p1.addBuilding('Ellis')
    p1.addBuilding('JQH Arena')
    p2.addBuilding('Temple')
    
    players = [p1, p2, p3, p4, p5, p6]
    
    pd = PlayersDisplay(players)

    pd.screen.blit(pd.getPD(), (0, 0))
    pygame.display.flip()
    
    gameActive = True
    while gameActive:
        for event in pygame.event.get():
            if event.type == QUIT:
                gameActive = False

    pygame.quit()



if __name__ == '__main__':
    main()
