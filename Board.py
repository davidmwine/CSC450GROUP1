# Drawing the basic board layout

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

                # Remove these if statement, testing images
                if seq == 0:
                    carrington = pygame.image.load(os.path.join("img","buildings","CarringtonHall.png")).convert()
                    carrington = pygame.transform.scale(carrington, (int(self.scale*205), int(self.scale*142)))
                    self.board.blit(carrington,(x_pos, y_pos))
                if seq == 1:
                    siceluff = pygame.image.load(os.path.join("img","buildings","SiceluffHall.png")).convert()
                    siceluff = pygame.transform.scale(siceluff, (int(self.scale*136), int(self.scale*142)))
                    self.board.blit(siceluff,(x_pos, y_pos))
                if seq == 2:
                    cheek = pygame.image.load(os.path.join("img","buildings","CheekHall.png")).convert()
                    cheek = pygame.transform.scale(cheek, (int(self.scale*136), int(self.scale*142)))
                    self.board.blit(cheek,(x_pos, y_pos))
                if seq == 3:
                    bookstore = pygame.image.load(os.path.join("img","buildings","UniversityBookstore.png")).convert()
                    bookstore = pygame.transform.scale(bookstore, (int(self.scale*136), int(self.scale*142)))
                    self.board.blit(bookstore,(x_pos, y_pos))
                if seq == 4:
                    hammons = pygame.image.load(os.path.join("img","buildings","HammonsField.png")).convert()
                    hammons = pygame.transform.scale(hammons, (int(self.scale*136), int(self.scale*142)))
                    self.board.blit(hammons,(x_pos, y_pos))
                if seq == 5:
                    greenwood = pygame.image.load(os.path.join("img","buildings","GreenwoodLabSchool.png")).convert()
                    greenwood = pygame.transform.scale(greenwood, (int(self.scale*136), int(self.scale*142)))
                    self.board.blit(greenwood,(x_pos, y_pos))
                if seq == 6:
                    foster = pygame.image.load(os.path.join("img","buildings","FosterRecreationCenter.png")).convert()
                    foster = pygame.transform.scale(foster, (int(self.scale*136), int(self.scale*142)))
                    self.board.blit(foster,(x_pos, y_pos))
                if seq == 7:
                    juanita = pygame.image.load(os.path.join("img","buildings","JuanitaKHammons.png")).convert()
                    juanita = pygame.transform.scale(juanita, (int(self.scale*136), int(self.scale*142)))
                    self.board.blit(juanita,(x_pos, y_pos))

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

                # Remove these if statements, testing images
                if seq == 8:
                    north = pygame.image.load(os.path.join("img","buildings","BearParkNorth.png")).convert()
                    north = pygame.transform.scale(north, (int(self.scale*205), int(self.scale*142)))
                    self.board.blit(north,(x_pos, y_pos))
                if seq == 9:
                    hammonscenter = pygame.image.load(os.path.join("img","buildings","HammonsStudentCenter.png")).convert()
                    hammonscenter = pygame.transform.scale(hammonscenter, (int(self.scale*205), int(self.scale*94)))
                    self.board.blit(hammonscenter,(x_pos, y_pos))
                if seq == 10:
                    brick = pygame.image.load(os.path.join("img","buildings","BrickCity.png")).convert()
                    brick = pygame.transform.scale(brick, (int(self.scale*205), int(self.scale*94)))
                    self.board.blit(brick,(x_pos, y_pos))
                if seq == 11:
                    kings = pygame.image.load(os.path.join("img","buildings","KingsStreetAnnex.png")).convert()
                    kings = pygame.transform.scale(kings, (int(self.scale*205), int(self.scale*94)))
                    self.board.blit(kings,(x_pos, y_pos))
                if seq == 12:
                    jqh = pygame.image.load(os.path.join("img","buildings","JQHArena.png")).convert()
                    jqh = pygame.transform.scale(jqh, (int(self.scale*205), int(self.scale*94)))
                    self.board.blit(jqh,(x_pos, y_pos))
                if seq == 13:
                    forsythe = pygame.image.load(os.path.join("img","buildings","ForsytheAthleticsCenter.png")).convert()
                    forsythe = pygame.transform.scale(forsythe, (int(self.scale*205), int(self.scale*94)))
                    self.board.blit(forsythe,(x_pos, y_pos))
                if seq == 14:
                    mcdonald = pygame.image.load(os.path.join("img","buildings","McDonaldArena.png")).convert()
                    mcdonald = pygame.transform.scale(mcdonald, (int(self.scale*205), int(self.scale*94)))
                    self.board.blit(mcdonald,(x_pos, y_pos))
                if seq == 15:
                    psu = pygame.image.load(os.path.join("img","buildings","PlasterStudentUnion.png")).convert()
                    psu = pygame.transform.scale(psu, (int(self.scale*205), int(self.scale*94)))
                    self.board.blit(psu,(x_pos, y_pos))
                    
                
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

                # Remove these if statements, testing images
                if seq == 16:
                    south = pygame.image.load(os.path.join("img","buildings","BearParkSouth.png")).convert()
                    south = pygame.transform.scale(south, (int(self.scale*205), int(self.scale*142)))
                    self.board.blit(south,(x_pos, y_pos))
                
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

            #remove this (needed for image dimesions)
            print(cellWidth, cellHeight)
                

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
    
    gb = GameBoard(1, buildingsFromBuildings)
    
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
