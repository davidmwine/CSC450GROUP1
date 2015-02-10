import pygame
from pygame.locals import *
import os
import sys
from rulesMenu import Rules
from startMenu import Start
from optionsMenu import Options

os.environ['SDL_VIDEO_CENTERED'] = '1'  # Center the display
pygame.init()
#clock = pygame.time.Clock()

'''class Player(object):
    
    def __init__(self, name):
        self.name = name
        self.game_piece = None  #Player's game piece
        self.money = 1000  #Amount of money to start with
        self.pos = 0  #Starting position
        self.grad_points = 0 '''
class Game(object):
    screen = None

    def __init__(self):
        #Get screen info and set window to full screen
        '''infoScreen = pygame.display.Info()  
        self.screen = pygame.display.set_mode((infoScreen.current_w, infoScreen.current_h))'''
        
        self.screen = pygame.display.set_mode((800, 600))  #Set display window size
        pygame.display.set_caption("Mastering MSU")
        self.img_icon_small = pygame.image.load(os.path.join("img","icon_small.png")).convert_alpha()
        pygame.display.set_icon(self.img_icon_small)
        self.nextScreen = "start"
        self.splashShow = True

        #self.round_number = 1

    def font_op(self, size,fontName):  #Pick font size and type
        if fontName == "helvetica":
            fontAndSize = pygame.font.Font(os.path.join("font","helvetica.OTF"),size) # "font" is directory for the font file
        elif fontName == "berlin":
            fontAndSize = pygame.font.Font(os.path.join("font","berlin.TTF"),size)
            fontAndSize = pygame.font.Font(os.path.join("font","helvetica.otf"),size) # "font" is directory for the font file
        elif fontName == "berlin":
            fontAndSize = pygame.font.Font(os.path.join("font","berlin.ttf"),size)
        return fontAndSize
        
    def start(self):
        while True:
            if self.nextScreen == "start":
                startMenu = Start(self.screen, self.font_op)
                '''if self.splashShow:
                    startMenu.splash()
                    self.splashShow = False'''
                if self.splashShow:
                    startMenu.splash()
                    self.splashShow = False
                self.nextScreen = startMenu.menu()
            if self.nextScreen == "rules":
                rulesMenu = Rules(self.screen, self.font_op)
                self.nextScreen = rulesMenu.run()
            if self.nextScreen == "options":
                optionsMenu = Options(self.screen, self.font_op)
                self.nextScreen = optionsMenu.run()

Game().start()
