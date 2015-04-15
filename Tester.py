import pygame
import sys
import os
from pygame.locals import *
from SignIn import SignIn


def main():
    pygame.init()
    scale = .50
    screen = pygame.display.set_mode((int(1920*scale), int(1080*scale)))
    
    lobby = SignIn(screen, font_op)
    lobby.run()



def font_op(size,fontName):  #Pick font size and type
        if fontName == "helvetica":
            fontAndSize = pygame.font.Font(os.path.join("font","helvetica.otf"),size) # "font" is directory for the font file
        elif fontName == "berlin":
            fontAndSize = pygame.font.Font(os.path.join("font","berlin.ttf"),int(size))
        return fontAndSize
main()
