
import pygame
from pygame.locals import *

from player import Player
from globals import Globals



class PlayersDisplay(object):

    def __init__(self, players):

        self.players = players
        
        pygame.init()
        
        self.screen = pygame.display.set_mode((200, 510))

        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(Globals.maroon)

        totalHeight = 85 * len(players)
        pygame.draw.rect(self.background, Globals.lightGray, (0, 0, 200, totalHeight), 0)
        for i in range(1, len(players)):
            pygame.draw.lines(self.background, Globals.maroon, False, [(0,85*i), (200,85*i)], 1)

        if pygame.font:
            for i in range(len(players)):
                self.printText(i)
                  

    def printText(self, i):
        font = pygame.font.Font(None, 20)
        
        text = font.render(self.players[i].getName(),
                           True, Color('black'))
        self.background.blit(text, (0, 85*i))
        
        text = font.render(self.players[i].getCollegeAbbr(),
                           True, Color('black'))
        self.background.blit(text, (75, 85*i))
        #pygame.draw.circle(self.background, black, (125, 5), 5)  # Do we want an icon?

        text = font.render('$' + str(self.players[i].getDollars()),
                           True, Color('black'))
        self.background.blit(text, (125, 85*i))
        
        text = font.render(str(self.players[i].getPoints()) + ' pts',
                           True, Color('black'))
        self.background.blit(text, (20, 20+85*i))

        text = font.render(str(self.players[i].getPointsPerRound()) + ' pts/round',
                           True, Color('black'))
        self.background.blit(text, (110, 20+85*i))
        

    def insert(self, x, y):
        """Inserts this display into another window at the specified point."""
        self.screen.blit(self.background, (x, y))
        pygame.display.flip() 



def main():

    p1 = Player("player1", "Business")
    p2 = Player("player2", "Arts and Letters")
    p3 = Player("player3", "Natural and Applied Sciences")

    players = [p1, p2, p3]

    pd = PlayersDisplay(players)
    pd.insert(0, 0)
    
    gameActive = True
    while gameActive:
        for event in pygame.event.get():
            if event.type == QUIT:
                gameActive = False

    pygame.quit()



if __name__ == '__main__':
    main()
