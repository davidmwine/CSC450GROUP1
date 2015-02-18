# Drawing the basic board layout

import pygame
import sys
import math
from building import Building
from pygame.locals import *
  
MAROON   = (80, 0, 0)                               # RGB code for Maroon       (University color - background)
LTGRAY   = (200, 200, 200)                          # RGB code for light Gray   (Unowned)
PURPLE   = (128, 0, 128)                            # RGB code for Purple       (Arts & Letters)
RED      = (255, 0, 0)                              # RGB code for Red          (Business)
LTBLUE   = (173, 216, 230)                          # RGB code for Light Blue   (Education)
ORANGE   = (255, 140, 0)                            # RGB code for Orange       (Health & Human Services)
PEACOCK  = (0, 128, 128)                            # RGB code for Peacock Blue (Humanities & Public Affairs)
GOLDEN   = (255, 215, 0)                            # RGB code for Golden Yellow (Natural and Applied Science)
LTGREEN  = (0, 128, 0)                              # RGB code for Green        (Agriculture)
BLACK    = (0, 0, 0)                                # RGB code for Black        
WHITE    = (255, 255, 255)                          # RGB code for White        
BLUE     = (0, 0, 255)                              # RGB code for Blue         
GREEN    = (0, 255, 0)                              # RGB code for Green        


buildings = []
boardorder = 0
buildings.append( Building('Carrington Hall', boardorder+len(buildings), 'special') )
buildings.append( Building('Siceluff Hall', boardorder+len(buildings), 'academic') )
buildings.append( Building('Cheek Hall', boardorder+len(buildings), 'academic') ) 
buildings.append( Building('Wells House', boardorder+len(buildings), 'support') ) 
buildings.append( Building('University Bookstore', boardorder+len(buildings), 'support') ) 
buildings.append( Building('Hammons Field', boardorder+len(buildings), 'sports') ) 
buildings.append( Building('Greenwood Lab School', boardorder+len(buildings), 'academic') )
buildings.append( Building('Blair-Shannon House', boardorder+len(buildings), 'support') )
buildings.append( Building('Foster Recreation Center', boardorder+len(buildings), 'support') )
buildings.append( Building('Bear Park North', boardorder+len(buildings), 'special') )
buildings.append( Building('Pummill Hall', boardorder+len(buildings), 'academic') )
buildings.append( Building('Juanita K Hammons', boardorder+len(buildings), 'support') )
buildings.append( Building('Hill Hall', boardorder+len(buildings), 'academic') )
buildings.append( Building('JQH Arena', boardorder+len(buildings), 'sports') )
buildings.append( Building('Ellis Hall', boardorder+len(buildings), 'academic') )
buildings.append( Building('Hammons Student Center', boardorder+len(buildings), 'support') )
buildings.append( Building('Craig Hall', boardorder+len(buildings), 'academic') ) 
buildings.append( Building('Allison South Stadium', boardorder+len(buildings), 'sports') )
buildings.append( Building('Art Annex', boardorder+len(buildings), 'support') )
buildings.append( Building('Brick City', boardorder+len(buildings), 'academic') ) 
buildings.append( Building('Karls Hall', boardorder+len(buildings), 'academic') ) 
buildings.append( Building('Kings St Annex', boardorder+len(buildings), 'academic') ) 
buildings.append( Building('Meyer Library', boardorder+len(buildings), 'support') )
buildings.append( Building('Forsythe Athletics Center', boardorder+len(buildings), 'support') ) 
buildings.append( Building('Power House', boardorder+len(buildings), 'support') ) 
buildings.append( Building('Freudenberger House', boardorder+len(buildings), 'support') ) 
buildings.append( Building('Bear Park South', boardorder+len(buildings), 'special') )
buildings.append( Building('Plaster Sports Complex', boardorder+len(buildings), 'sports') )
buildings.append( Building('Central Stores & Maintenance', boardorder+len(buildings), 'support') ) 
buildings.append( Building('Temple Hall', boardorder+len(buildings), 'academic') )      
buildings.append( Building('Kemper Hall', boardorder+len(buildings), 'academic') ) 
buildings.append( Building('Strong Hall', boardorder+len(buildings), 'academic') ) 
buildings.append( Building('Glass Hall', boardorder+len(buildings), 'academic') ) 
buildings.append( Building('McDonald Arena', boardorder+len(buildings), 'academic') )  
buildings.append( Building('Plaster Student Union', boardorder+len(buildings), 'support') )
buildings.append( Building('Accreditation Review', boardorder+len(buildings), 'special') )

nullspace = boardorder+len(buildings)
buildings.append( Building('', nullspace, 'nullspace') )            # Null Space 
  

class GameBoard(object):

    def __init__(self, scale, isSubscreen=False):

        # Width and height of each grid location
        self.scale = scale
        size = [int(self.scale*1440), int(self.scale*1020)]                                   # set the overall size
        margin = 2                                         # sets the margin between each cell
        padding = 3                                         # sets the padding for text
        width  = (math.floor(size[0]/10)-margin)            # set the Width of each cell
        height = (math.floor(size[1]/10)-margin)            # set the Height of each cell

        if isSubscreen == False:
            pygame.init()
            self.board = pygame.display.set_mode(size)
            pygame.display.set_caption("Mastering MSU")              #Name of title
        else:
            self.board = pygame.Surface(size)
            
        boardfont = pygame.font.Font(None, 16)

        boardSpace = 0
        # Create a 2 dimensional array/list of lists.
        # The outer ( or rows ) dimension
        grid = []
        for row in range(10):
            # The inner ( or columns ) dimension
            grid.append([])
            for column in range(10):
                if row == 0 or row == 9 or column == 0 or column == 9:
                    grid[row].append(buildings[boardSpace])
                    mine = grid[row][column]
                    grid[row][column].setPosition([row, column])
                    boardSpace += 1
                else:
                    grid[row].append(buildings[nullspace])
                    mine = grid[row][column]
                    grid[row][column].setPosition([row, column])
                color = grid[row][column].getColor()
                pygame.draw.rect(self.board, color, [(margin+width)*column+margin,(margin+height)*row+margin, width,height])
                self.board.blit(boardfont.render(mine.getName(), True, BLACK), [(margin+width)*column+margin,((margin+height)+1)*row+margin, width,height])

    def getGB(self):
        return self.board


def main():
    
    gb = GameBoard(0.5)

    #pd.screen.blit(pd.getPD(), (0, 0))
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
