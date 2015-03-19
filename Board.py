# Drawing the basic board layout

import pygame
from pygame.locals import *
import sys
import math
import Building
import Colors 

class GameBoard(object):

    def __init__(self, scale, buildings, isSubscreen=False):

        # Width and height of each grid location
        self.scale = scale
        size = [int(self.scale*1400), int(self.scale*980)]  # set the overall size
        margin = 2                                          # sets the margin between each cell
        padding = 3                                         # sets the padding for text
        polysize = 20
        
        width  = (math.floor(size[0]/10)-margin)            # set the Width of each cell
        height = (math.floor(size[1]/10)-margin)            # set the Height of each cell

        padWidth = (size[0] - (width * 10)) / 2
        padHeight = (size[1] - (height * 10)) / 2
        
        self.buildings = buildings

        if isSubscreen == False:
            pygame.init()
            self.board = pygame.display.set_mode(size)
            pygame.display.set_caption("Mastering MSU")              #Name of title
        else:
            self.board = pygame.Surface(size)
            
        self.boardfont = pygame.font.Font(None, 16)

        x_pos = 0 + padWidth
        y_pos = 0 + padHeight
        angle = -90.0
        
        for building in range(len(buildings)):
            seq = buildings[building].getSequence()
            cellColor = buildings[building].getColor()
            cellName = buildings[building].getName()
            
            print(seq, cellColor, cellName)
                
            # Side 1 (Top of screen)
            if seq / 8.0 < 1:
                side = 1
                if seq % 8 == 0:
                    cellWidth = width * 1.5
                    cellHeight = height * 1.5
                else:
                    cellWidth = width
                    cellHeight = height * 1.5
                    pointList = (x_pos, y_pos + cellHeight),(x_pos + polysize, y_pos + cellHeight + polysize), (x_pos + cellWidth - polysize, y_pos + cellHeight + polysize), (x_pos + cellWidth, y_pos + cellHeight)
                    poly = pygame.draw.polygon(self.board, cellColor, pointList)
                    poly = pygame.draw.polygon(self.board, Colors.BLACK, pointList, 1)
                    # Store pointList in building object
                    buildings[building].setPointList(pointList)
                    
                rect = pygame.draw.rect(self.board, cellColor, (x_pos, y_pos, cellWidth, cellHeight))
                rect = pygame.draw.rect(self.board, Colors.BLACK, (x_pos, y_pos, cellWidth, cellHeight),margin)
                # Store rect in building object
                buildings[building].setRect(rect)
                x_pos += cellWidth
                        
            # Side 2 (Right of screen)
            elif seq / 8.0 >= 1 and seq / 8.0 < 2:
                side = 2
                if seq % 8 == 0:
                    cellWidth = width * 1.5
                    cellHeight = height * 1.5
                else:
                    cellWidth = width * 1.5
                    cellHeight = height
                    pointList = (x_pos, y_pos),(x_pos - polysize, y_pos + polysize), (x_pos - polysize, y_pos + cellHeight - polysize), (x_pos, y_pos + cellHeight)
                    poly = pygame.draw.polygon(self.board, cellColor, pointList)
                    poly = pygame.draw.polygon(self.board, Colors.BLACK, pointList, 1)
                    # Store pointList in building object
                    buildings[building].setPointList(pointList)
                    
                rect = pygame.draw.rect(self.board, cellColor, (x_pos, y_pos, cellWidth, cellHeight))
                rect = pygame.draw.rect(self.board, Colors.BLACK, (x_pos, y_pos, cellWidth, cellHeight),margin)
                # Store rect in building object
                buildings[building].setRect(rect)
                y_pos += cellHeight
                            
            # Side 3 (Bottom of screen)
            elif seq / 8.0 >= 2 and seq / 8.0 < 3:
                side = 3
                if seq % 8 == 0:
                    cellWidth = width * 1.5
                    cellHeight = height * 1.5
                else:
                    cellWidth = width
                    cellHeight = height * 1.5
                    x_pos -= cellWidth
                    pointList = (x_pos, y_pos),(x_pos + polysize, y_pos - polysize), (x_pos + cellWidth - polysize, y_pos - polysize), (x_pos + cellWidth, y_pos)
                    poly = pygame.draw.polygon(self.board, cellColor, pointList)
                    poly = pygame.draw.polygon(self.board, Colors.BLACK, pointList, 1)
                    # Store pointList in building object
                    buildings[building].setPointList(pointList)
                    
                rect = pygame.draw.rect(self.board, cellColor, (x_pos, y_pos, cellWidth, cellHeight))
                rect = pygame.draw.rect(self.board, Colors.BLACK, (x_pos, y_pos, cellWidth, cellHeight),margin)
                # Store rect in building object
                buildings[building].setRect(rect)
                                
            # Side 4 (Left of screen)
            elif seq / 8.0 >= 3:
                x_pos = 0 + padWidth
                side = 4
                if seq % 8 == 0:
                    cellWidth = width * 1.5
                    cellHeight = height * 1.5
                else:
                    cellWidth = width * 1.5
                    cellHeight = height
                    y_pos -= cellHeight
                    pointList = (x_pos + cellWidth, y_pos),(x_pos + cellWidth + polysize, y_pos + polysize), (x_pos + cellWidth + polysize, y_pos - polysize + cellHeight), (x_pos + cellWidth, y_pos + cellHeight)
                    poly = pygame.draw.polygon(self.board, cellColor, pointList)
                    poly = pygame.draw.polygon(self.board, Colors.BLACK, pointList, 1)
                    # Store pointList in building object
                    buildings[building].setPointList(pointList)
                    
                rect = pygame.draw.rect(self.board, cellColor, (x_pos, y_pos, cellWidth, cellHeight))
                rect = pygame.draw.rect(self.board, Colors.BLACK, (x_pos, y_pos, cellWidth, cellHeight),margin)
                # Store rect in building object
                buildings[building].setRect(rect)
                

    def getGB(self):
            return self.board

    def colorBuilding(self, building):
        color = building.getColor()
        rect = building.getRect()
        name = building.getName()
        pointList = building.getPointList()
        #pygame.draw.rect(self.board, color, rect)
        pygame.draw.polygon(self.board, color, pointList)
        pygame.draw.polygon(self.board, color, pointList, 1)
        self.board.blit(self.boardfont.render(name, True, Colors.BLACK), rect)


def main():
    
    buildingsFromBuildings = Building.Buildings().getBuildingList()
    
    gb = GameBoard(0.65, buildingsFromBuildings)
    
    pygame.display.flip()                           #Updates the screen
    
    '''
    gameActive = True
    while gameActive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameActive = False
    pygame.quit()
    sys.exit()
    '''


if __name__ == '__main__':
    main()
