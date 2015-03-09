# Drawing the basic board layout

import pygame
from pygame.locals import *
import sys
import math
from globals import Globals
 

class GameBoard(object):

    def __init__(self, scale, buildings, isSubscreen=False):

        # Width and height of each grid location
        self.scale = scale
        size = [int(self.scale*1400), int(self.scale*980)]  # set the overall size
        margin = 2                                          # sets the margin between each cell
        padding = 3                                         # sets the padding for text
        width  = (math.floor(size[0]/10)-margin)            # set the Width of each cell
        height = (math.floor(size[1]/10)-margin)            # set the Height of each cell

        self.buildings = buildings

        if isSubscreen == False:
            pygame.init()
            self.board = pygame.display.set_mode(size)
            pygame.display.set_caption("Mastering MSU")              #Name of title
        else:
            self.board = pygame.Surface(size)
            
        self.boardfont = pygame.font.Font(None, 16)

        boardSpace = 0
        # Create a 2 dimensional array/list of lists.
        # Each element grid[row][column] either references a building or contains ''.
        # The outer ( or rows ) dimension
        grid = []
        for row in range(10):
            # The inner ( or columns ) dimension
            grid.append([])
            for column in range(10):
                if row == 0 or row == 9 or column == 0 or column == 9:
                    grid[row].append(self.buildings[boardSpace])
                    mine = grid[row][column]
                    grid[row][column].setPosition([row, column])
                    color = grid[row][column].getColor()
                else:
                    grid[row].append('')
                    color = Globals.maroon
                rect = pygame.Rect((margin+width)*column+margin, (margin+height)*row+margin, width, height)    
                pygame.draw.rect(self.board, color, rect)
                # Put names on the rectangles which represent buildings, store a Rect in each building object
                if color != Globals.maroon:
                    self.buildings[boardSpace].setRect(rect)
                    self.board.blit(self.boardfont.render(mine.getName(), True, Color('black')),
                                    [(margin+width)*column+margin,((margin+height)+1)*row+margin, width,height])
                    boardSpace += 1


    def getGB(self):
        return self.board


    def colorBuilding(self, building):
        color = building.getColor()
        rect = building.getRect()
        name = building.getName()
        pygame.draw.rect(self.board, color, rect)
        self.board.blit(self.boardfont.render(name, True, Color('black')), rect)
        


def main():
    
    gb = GameBoard(0.65)
    
    pygame.display.flip()                           #Updates the screen
    
    gameActive = True
    while gameActive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameActive = False

    pygame.quit()
    sys.exit()



if __name__ == '__main__':
    main()
