"""
Drawing the basic board layout
Graduation cap icon from http://www.flaticon.com
"""

import pygame
from pygame.locals import *
import sys
import os
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
        polyMargin = 5
        
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

        self.board.fill(Colors.MAROON)    
            
        self.boardfont = pygame.font.Font(None, 30)

        self.gradIcon = pygame.image.load(os.path.join("img", "graduate34.png")).convert_alpha()

        x_pos = 0 + padWidth
        y_pos = 0 + padHeight
        angle = -90.0
        
        for building in range(len(buildings)):
            seq = buildings[building].getSequence()
            cellName = buildings[building].getName()
            cellImage = buildings[building].getImage()
            if buildings[building].getPurpose() == 'academic':
                cellColor = buildings[building].getColor()
            elif buildings[building].getPurpose() != 'special':
                cellColor = buildings[building].getInitialColor()
                            
            # Side 1 (Top of screen)
            if seq / 8.0 < 1:
                side = 1
                if seq % 8 == 0:
                    cellWidth = width * 1.5
                    cellHeight = height * 1.5
                else:
                    cellWidth = width
                    cellHeight = height * 1.5
                    pointList = ((x_pos, y_pos + cellHeight),
                                (x_pos + polysize, y_pos + cellHeight + polysize),
                                (x_pos + cellWidth - polysize, y_pos + cellHeight + polysize),
                                (x_pos + cellWidth, y_pos + cellHeight))
                    innerPointList = ((x_pos, y_pos + cellHeight),
                                (x_pos + polysize + polyMargin, y_pos + cellHeight + polysize - polyMargin),
                                (x_pos + cellWidth - polysize - polyMargin, y_pos + cellHeight + polysize - polyMargin),
                                (x_pos + cellWidth, y_pos + cellHeight))
                    poly = pygame.draw.polygon(self.board, cellColor, pointList)
                    poly = pygame.draw.polygon(self.board, Colors.BLACK, pointList, 1)
                    # Store pointList in building object
                    buildings[building].setPointList(pointList)
                    buildings[building].setInnerPointList(innerPointList)
                    
                    if buildings[building].getPurpose() == 'card':
                        '''
                        # This stripe is another option for the card spaces, to match the actual cards.
                        stripePointList = ((x_pos + polysize/3, y_pos + cellHeight + polysize/3),
                                (x_pos + 2*polysize/3, y_pos + cellHeight + 2*polysize/3),
                                (x_pos + cellWidth - 2*polysize/3, y_pos + cellHeight + 2*polysize/3),
                                (x_pos + cellWidth - polysize/3, y_pos + cellHeight + polysize/3))
                        poly = pygame.draw.polygon(self.board, Colors.MAROON, stripePointList)
                        '''
                        self.board.blit(self.boardfont.render('?', True, Colors.WHITE),
                                        (x_pos + cellWidth/2 - self.boardfont.size('?')[0]/2, y_pos + cellHeight))
                    if buildings[building].getPurpose() in ['card', 'utility']:
                        pygame.draw.polygon(self.board, Colors.WHITE, pointList, 1)
                        
                    
                rect = pygame.draw.rect(self.board, Colors.BLACK, (x_pos, y_pos, cellWidth, cellHeight),margin)

                # Load cell image
                cellImage = pygame.transform.scale(cellImage, (int(cellWidth - margin), int(cellHeight - margin)))
                self.board.blit(cellImage, (x_pos + margin, y_pos + margin))

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
                    pointList = ((x_pos, y_pos),
                                 (x_pos - polysize, y_pos + polysize),
                                 (x_pos - polysize, y_pos + cellHeight - polysize),
                                 (x_pos, y_pos + cellHeight))
                    innerPointList = ((x_pos, y_pos),
                                 (x_pos - polysize + polyMargin, y_pos + polysize + polyMargin),
                                 (x_pos - polysize + polyMargin, y_pos + cellHeight - polysize - polyMargin),
                                 (x_pos, y_pos + cellHeight))
                    poly = pygame.draw.polygon(self.board, cellColor, pointList)
                    poly = pygame.draw.polygon(self.board, Colors.BLACK, pointList, 1)
                    # Store pointList in building object
                    buildings[building].setPointList(pointList)
                    buildings[building].setInnerPointList(innerPointList)

                    if buildings[building].getPurpose() == 'card':                        
                        self.board.blit(self.boardfont.render('?', True, Colors.WHITE),
                            (x_pos - polysize/2 - self.boardfont.size('?')[0]/2,
                             y_pos + cellHeight/2 - self.boardfont.size('?')[1]/2))
                        pygame.draw.polygon(self.board, Colors.WHITE, pointList, 1)
                    
                rect = pygame.draw.rect(self.board, Colors.BLACK, (x_pos, y_pos, cellWidth, cellHeight),margin)

                # Load cell image
                cellImage = pygame.transform.scale(cellImage, (int(cellWidth - margin), int(cellHeight - margin)))
                self.board.blit(cellImage, (x_pos + margin, y_pos + margin))

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
                    pointList = ((x_pos, y_pos),
                                 (x_pos + polysize, y_pos - polysize),
                                 (x_pos + cellWidth - polysize, y_pos - polysize),
                                 (x_pos + cellWidth, y_pos))
                    innerPointList = ((x_pos, y_pos),
                                 (x_pos + polysize + polyMargin, y_pos - polysize + polyMargin),
                                 (x_pos + cellWidth - polysize - polyMargin, y_pos - polysize + polyMargin),
                                 (x_pos + cellWidth, y_pos))
                    poly = pygame.draw.polygon(self.board, cellColor, pointList)
                    poly = pygame.draw.polygon(self.board, Colors.BLACK, pointList, 1)
                    # Store pointList in building object
                    buildings[building].setPointList(pointList)
                    buildings[building].setInnerPointList(innerPointList)

                    if buildings[building].getPurpose() == 'card':
                        self.board.blit(self.boardfont.render('?', True, Colors.WHITE),
                                        (x_pos + cellWidth/2 - self.boardfont.size('?')[0]/2,
                                         y_pos - polysize))
                    if buildings[building].getPurpose() in ['card', 'utility']:
                        pygame.draw.polygon(self.board, Colors.WHITE, pointList, 1)
                    
                rect = pygame.draw.rect(self.board, Colors.BLACK, (x_pos, y_pos, cellWidth, cellHeight),margin)

                # Load cell image
                cellImage = pygame.transform.scale(cellImage, (int(cellWidth - margin), int(cellHeight - margin)))
                self.board.blit(cellImage, (x_pos + margin, y_pos + margin))

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
                    pointList = ((x_pos + cellWidth, y_pos),
                                 (x_pos + cellWidth + polysize, y_pos + polysize),
                                 (x_pos + cellWidth + polysize, y_pos - polysize + cellHeight),
                                 (x_pos + cellWidth, y_pos + cellHeight))
                    innerPointList = ((x_pos + cellWidth, y_pos),
                                 (x_pos + cellWidth + polysize - polyMargin, y_pos + polysize + polyMargin),
                                 (x_pos + cellWidth + polysize - polyMargin, y_pos - polysize - polyMargin + cellHeight),
                                 (x_pos + cellWidth, y_pos + cellHeight))
                    poly = pygame.draw.polygon(self.board, cellColor, pointList)
                    poly = pygame.draw.polygon(self.board, Colors.BLACK, pointList, 1)
                    # Store pointList in building object
                    buildings[building].setPointList(pointList)
                    buildings[building].setInnerPointList(innerPointList)

                    if buildings[building].getPurpose() == 'card':                        
                        self.board.blit(self.boardfont.render('?', True, Colors.WHITE),
                            (x_pos + cellWidth + self.boardfont.size('?')[0]/3,
                             y_pos + cellHeight/2 - self.boardfont.size('?')[1]/2))
                        pygame.draw.polygon(self.board, Colors.WHITE, pointList, 1)
                    
                rect = pygame.draw.rect(self.board, Colors.BLACK, (x_pos, y_pos, cellWidth, cellHeight),margin)

                # Load cell image
                cellImage = pygame.transform.scale(cellImage, (int(cellWidth - margin), int(cellHeight - margin)))
                self.board.blit(cellImage, (x_pos + margin, y_pos + margin))
                
                # Store rect in building object
                buildings[building].setRect(rect)
                

    def getGB(self):
            return self.board

    def colorBuilding(self, building):
        color = building.getColor()
        rect = building.getRect()
        name = building.getName()
        if building.getPurpose() == "academic" or building.getOwner() == None:
            pointList = building.getPointList()
        else:    
            pointList = building.getInnerPointList()
        pygame.draw.polygon(self.board, color, pointList)
        pygame.draw.polygon(self.board, Colors.BLACK, pointList, 1)


    def restoreOwnerColors(self):
        """Used after a screen resize to color the inner trapezoids the right color again."""
        for building in self.buildings:
            if ((building.getPurpose() == "sports"
            or building.getPurpose() == "stealable")
            and building.getOwner() != None):
                self.colorBuilding(building)


    def addGradIcons(self, building, number):
        """Adds the given number of grad icons to the trapezoid of the given building."""
        # First grad icon
        xPosition = building.getPointList()[0][0]
        yPosition = building.getPointList()[0][1]
        if 9 <= building.getSequence() <= 15:
            xPosition = building.getPointList()[1][0]
        elif 17 <= building.getSequence() <= 23:
            yPosition = building.getPointList()[1][1]
        self.board.blit(self.gradIcon, (xPosition, yPosition))

        # If there's 2 or 3...
        for i in range(number - 1):
            if 1 <= building.getSequence() <= 7 or 17 <= building.getSequence() <= 23:
                xPosition += self.gradIcon.get_rect().width
            else:
                yPosition += self.gradIcon.get_rect().height
            self.board.blit(self.gradIcon, (xPosition, yPosition))
            

    def addPlayerGradIcons(self, player):
        """
        Adds the appropriate number of grad icons to all buildings owned by the given
        player.  This is intended to be called right after a player upgrades or when
        the board is resized.
        """
        buildings = player.getBuildings()
        for building in buildings:
            if building.getPurpose() == "academic":
                if building.getDegreeLvl() == "Associate":
                    continue
                elif building.getDegreeLvl() == "Bachelor":
                    self.addGradIcons(building, 1)
                elif building.getDegreeLvl() == "Master":
                    self.addGradIcons(building, 2)
                if building.getDegreeLvl() == "Doctorate":
                    self.addGradIcons(building, 3)
            


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
