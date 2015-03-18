import pygame
import sys
import os
from pygame.locals import *
from lobby import Lobby


def main():
    pygame.init()
    screen = pygame.display.set_mode((int(1920*.5), int(1080*.5)))
    
    lobby = Lobby(font_op, screen, .5)
    lobby.run()



def font_op(size,fontName):  #Pick font size and type
        if fontName == "helvetica":
            fontAndSize = pygame.font.Font(os.path.join("font","helvetica.otf"),size) # "font" is directory for the font file
        elif fontName == "berlin":
            fontAndSize = pygame.font.Font(os.path.join("font","berlin.ttf"),size)
        return fontAndSize
main()
