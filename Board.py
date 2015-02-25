# Drawing the basic board layout

import pygame
import sys
import math
from building import Building
from pygame.locals import *
pygame.init()

size = [800, 800]
margin = 5 
WIDTH = size[0]
HEIGHT = size[1]

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


# Screen Setup
WINDOW = pygame.display.set_mode([WIDTH,HEIGHT])
CAPTION = pygame.display.set_caption('Mastering MSU')



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
        # game variables
        corner_width=size[0]/8
        corner_height=size[1]/8
        width=(size[0]-corner_width*2)/9
        height=(size[1] -corner_height*2)/9
        margin =(size[0]-(corner_width*2)-(width*8))/9
        
        
        #85,140,195,250,305,360,415,470, 525
        #example (SCREEN, (Color), (x, y, width, height))
        SCREEN = pygame.display.get_surface()
        background = pygame.Surface(SCREEN.get_size())
        background.fill((MAROON))
        SCREEN.blit(background, (0, 0))


        #left
        rect1 = pygame.draw.rect(SCREEN, (WHITE), (0,0, corner_width, corner_height)) #top left
        rect2 = pygame.draw.rect(SCREEN, (WHITE), (0,(corner_height+margin), corner_width, height))
        rect3 = pygame.draw.rect(SCREEN, (WHITE), (0,(corner_height+height+(margin*2)), corner_width, height))
        rect4 = pygame.draw.rect(SCREEN, (WHITE), (0,(corner_height+(height*2)+(margin*3)), corner_width, height))
        rect5 = pygame.draw.rect(SCREEN, (WHITE), (0,(corner_height+(height*3)+(margin*4)), corner_width, height))
        rect6 = pygame.draw.rect(SCREEN, (WHITE), (0,(corner_height+(height*4)+(margin*5)), corner_width, height))
        rect7 = pygame.draw.rect(SCREEN, (WHITE), (0,(corner_height+(height*5)+(margin*6)), corner_width, height))
        rect8 = pygame.draw.rect(SCREEN, (WHITE), (0,(corner_height+(height*6)+(margin*7)), corner_width, height))
        rect9 = pygame.draw.rect(SCREEN, (WHITE), (0,(corner_height+(height*7)+(margin*8)), corner_width, height))

        #top
        rect19 = pygame.draw.rect(SCREEN, (WHITE), ((corner_width+(width*8)+(margin*9)),0, corner_width, corner_height)) #top right
        rect11 = pygame.draw.rect(SCREEN, (WHITE), ((corner_width+margin), 0, width, corner_height))
        rect12 = pygame.draw.rect(SCREEN, (WHITE), ((corner_width+width+(margin*2)),0, width, corner_height))
        rect13 = pygame.draw.rect(SCREEN, (WHITE), ((corner_width+(width*2)+(margin*3)),0, width, corner_height))
        rect14 = pygame.draw.rect(SCREEN, (WHITE), ((corner_width+(width*3)+(margin*4)),0, width, corner_height))
        rect15 = pygame.draw.rect(SCREEN, (WHITE), ((corner_width+(width*4)+(margin*5)),0, width, corner_height))
        rect16 = pygame.draw.rect(SCREEN, (WHITE), ((corner_width+(width*5)+(margin*6)),0, width, corner_height))
        rect17 = pygame.draw.rect(SCREEN, (WHITE), ((corner_width+(width*6)+(margin*7)),0, width, corner_height))
        rect18 = pygame.draw.rect(SCREEN, (WHITE), ((corner_width+(width*7)+(margin*8)),0, width, corner_height))

        #right
        rect20 = pygame.draw.rect(SCREEN, (WHITE), ((corner_width+(width*8)+(margin*9)),(corner_height+margin), corner_width, height))
        rect21 = pygame.draw.rect(SCREEN, (WHITE), ((corner_width+(width*8)+(margin*9)),(corner_height+height+(margin*2)), corner_width, height))
        rect22 = pygame.draw.rect(SCREEN, (WHITE), ((corner_width+(width*8)+(margin*9)),(corner_height+(height*2)+(margin*3)),corner_width, height))
        rect23 = pygame.draw.rect(SCREEN, (WHITE), ((corner_width+(width*8)+(margin*9)),(corner_height+(height*3)+(margin*4)), corner_width, height))
        rect24 = pygame.draw.rect(SCREEN, (WHITE), ((corner_width+(width*8)+(margin*9)),(corner_height+(height*4)+(margin*5)), corner_width, height))
        rect25 = pygame.draw.rect(SCREEN, (WHITE), ((corner_width+(width*8)+(margin*9)),(corner_height+(height*5)+(margin*6)), corner_width, height))
        rect26 = pygame.draw.rect(SCREEN, (WHITE), ((corner_width+(width*8)+(margin*9)),(corner_height+(height*6)+(margin*7)), corner_width, height))
        rect27 = pygame.draw.rect(SCREEN, (WHITE), ((corner_width+(width*8)+(margin*9)),(corner_height+(height*7)+(margin*8)), corner_width, height))
        rect28 = pygame.draw.rect(SCREEN, (WHITE), ((corner_width+(width*8)+(margin*9)),((corner_height)+(margin*9)+(height*8)), corner_width, corner_height)) #bottom right

        #bottom
        rect10 = pygame.draw.rect(SCREEN, (WHITE), (0,((corner_height)+(margin*9)+(height*8)), corner_width, corner_height)) #bottom left
        rect29 = pygame.draw.rect(SCREEN, (WHITE), ((corner_width+(margin)),((corner_height)+(margin*9)+(height*8)), width, corner_height))
        rect30 = pygame.draw.rect(SCREEN, (WHITE), ((corner_width+(width)+(margin*2)),((corner_height)+(margin*9)+(height*8)), width, corner_height))
        rect31 = pygame.draw.rect(SCREEN, (WHITE), ((corner_width+(width*2)+(margin*3)),((corner_height)+(margin*9)+(height*8)), width, corner_height))
        rect32 = pygame.draw.rect(SCREEN, (WHITE), ((corner_width+(width*3)+(margin*4)),((corner_height)+(margin*9)+(height*8)), width, corner_height))
        rect33 = pygame.draw.rect(SCREEN, (WHITE), ((corner_width+(width*4)+(margin*5)),((corner_height)+(margin*9)+(height*8)), width, corner_height))
        rect34 = pygame.draw.rect(SCREEN, (WHITE), ((corner_width+(width*5)+(margin*6)),((corner_height)+(margin*9)+(height*8)), width, corner_height))
        rect35 = pygame.draw.rect(SCREEN, (WHITE), ((corner_width+(width*6)+(margin*7)),((corner_height)+(margin*9)+(height*8)), width, corner_height))
        rect36 = pygame.draw.rect(SCREEN, (WHITE), ((corner_width+(width*7)+(margin*8)),((corner_height)+(margin*9)+(height*8)), width, corner_height))

        #This is the BLUE grouping
        insiderect1 = pygame.draw.rect(SCREEN, (BLUE), ((corner_width+margin), (corner_height-20), width, 20))   
        insiderect2 = pygame.draw.rect(SCREEN, (BLUE), ((corner_width+(width*2)+(margin*3)),(corner_height-20), width, 20))  
        insiderect3 = pygame.draw.rect(SCREEN, (BLUE), ((corner_width+(width*3)+(margin*4)),(corner_height-20), width, 20))

        #This is the RED grouping
        insiderect4 = pygame.draw.rect(SCREEN, (RED), ((corner_width+(width*4)+(margin*5)),(corner_height-20), width, 20))
        insiderect5 = pygame.draw.rect(SCREEN, (RED), ((corner_width+(width*6)+(margin*7)),(corner_height-20), width, 20))
        insiderect6 = pygame.draw.rect(SCREEN, (RED), ((corner_width+(width*7)+(margin*8)),(corner_height-20), width, 20))

        #This is the GREEN grouping
        insiderect7 = pygame.draw.rect(SCREEN, (GREEN), ((corner_width+(width*6)+(margin*7)),(corner_height)+(margin*9)+(height*8), width, 20))
        insiderect8 = pygame.draw.rect(SCREEN, (GREEN), ((corner_width+(width*7)+(margin*8)),(corner_height)+(margin*9)+(height*8), width, 20))

        #This is the GOLDEN grouping
        insiderect9 = pygame.draw.rect(SCREEN, (GOLDEN),  ((corner_width+(margin)),(corner_height)+(margin*9)+(height*8), width, 20))
        insiderect10 = pygame.draw.rect(SCREEN, (GOLDEN), ((corner_width+(width*2)+(margin*3)),(corner_height)+(margin*9)+(height*8), width, 20))
        insiderect11 = pygame.draw.rect(SCREEN, (GOLDEN), ((corner_width+(width*3)+(margin*4)),(corner_height)+(margin*9)+(height*8), width, 20))
        

        #This is the LTBLUE grouping
        insiderect12 = pygame.draw.rect(SCREEN, (LTBLUE), ((corner_width+(width*8)+(margin*9)),(corner_height+margin), 20, height))
        insiderect13 = pygame.draw.rect(SCREEN, (LTBLUE), ((corner_width+(width*8)+(margin*9)),(corner_height+(height*2)+(margin*3)), 20, height))
        insiderect14 = pygame.draw.rect(SCREEN, (LTBLUE), ((corner_width+(width*8)+(margin*9)),(corner_height+(height*3)+(margin*4)), 20, height))

        
        #This is the PEACOCK grouping
        insiderect15 = pygame.draw.rect(SCREEN, (PEACOCK), ((corner_width+(width*8)+(margin*9)),((corner_height)+(margin*6)+(height*5)), 20, height))
        insiderect16 = pygame.draw.rect(SCREEN, (PEACOCK), ((corner_width+(width*8)+(margin*9)),((corner_height)+(margin*8)+(height*7)), 20, height))

        #This is the PURPLE grouping
        insiderect17 = pygame.draw.rect(SCREEN, (PURPLE), (corner_width-20,(corner_height+(margin)), 20, height))   
        insiderect18 = pygame.draw.rect(SCREEN, (PURPLE), (corner_width-20,(corner_height+(height*2)+(margin*3)), 20, height))  
        insiderect19 = pygame.draw.rect(SCREEN, (PURPLE), (corner_width-20,(corner_height+(height*3)+(margin*4)), 20, height))

        #This is the ORANGE grouping
        insiderect20 = pygame.draw.rect(SCREEN, (ORANGE), (corner_width-20,(corner_height+(height*4)+(margin*5)), 20, height))
        insiderect21 = pygame.draw.rect(SCREEN, (ORANGE), (corner_width-20,(corner_height+(height*6)+(margin*7)), 20, height))
        insiderect22 = pygame.draw.rect(SCREEN, (ORANGE), (corner_width-20,(corner_height+(height*7)+(margin*8)), 20, height))

        #-------------------------------------------------------------------------------
        # Refresh Display
        pygame.display.flip()
        pygame.display.update()
        #-------------------------------------------------------------------------------


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
