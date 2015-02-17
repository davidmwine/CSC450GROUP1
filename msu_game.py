import pygame
from pygame.locals import *
import os
import sys
from rulesMenu import Rules
from startMenu import Start
from optionsMenu import Options
#Only leave one uncommented, each one is a current option
from GameArea import gameArea #Main
#from GameAreaJB import GameArea #Jennifer's Layout
#from GameAreaS import gameArea #John's Layout
#Jennifer and John's layouts don't currently cooperate with the rest
#of the program so they are left commented out for now

os.environ['SDL_VIDEO_CENTERED'] = '1'  # Center the display
pygame.init()

class Game(object):
    screen = None

    def __init__(self):
        #Get screen info and set window to full screen
        self.infoScreen = pygame.display.Info()

        #self.screen = pygame.display.set_mode((self.infoScreen.current_w, self.infoScreen.current_h),pygame.FULLSCREEN)
        self.height_ratio_16x9 = .5625 #Number to multiply width by to get 16x9 ratio for height
        self.y_offset = int((self.infoScreen.current_h-int(self.infoScreen.current_w*self.height_ratio_16x9))/2)

        #Temporary code to test multiple screen sizes 
        #Comment self.screen above
        self.qHD = (960, 540)
        self.HD = (1280, 720)
        self.HDplus = (1600, 900)
        self.fullHD = (1920, 1080)
        self.four_three_ratio = (960, 720)
        self.screen_size = [self.qHD, self.HD, self.HDplus, self.fullHD, self.four_three_ratio]
        self.size = 0
        if self.infoScreen.current_h == self.screen_size[self.size][1]\
           and self.infoScreen.current_w == self.screen_size[self.size][0]:
            self.screen = pygame.display.set_mode(self.screen_size[self.size],pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.screen_size[self.size]) #Select screen size
        self.y_offset = 0 #Set to 0 if not fullscreen, *set to .75 if four_three_ratio selected
        
        pygame.display.set_caption("Mastering MSU")
        self.img_icon_small = pygame.image.load(os.path.join("img","icon_small.png")).convert_alpha()
        pygame.display.set_icon(self.img_icon_small)
        self.nextScreen = "start"
        self.splashShow = False

        #self.round_number = 1

    def font_op(self, size,fontName):  #Pick font size and type
        if fontName == "helvetica":
            fontAndSize = pygame.font.Font(os.path.join("font","helvetica.otf"),size) # "font" is directory for the font file
        elif fontName == "berlin":
            fontAndSize = pygame.font.Font(os.path.join("font","berlin.ttf"),size)
        return fontAndSize
        
    def start(self):
        startMenu = Start(self.screen, self.font_op, self.y_offset)
        rulesMenu = Rules(self.screen, self.font_op, self.y_offset)
        optionsMenu = Options(self.screen, self.font_op, self.y_offset)
        Game = gameArea(self.screen, .5)
        
        while True:
            if self.nextScreen == "start":
                if self.splashShow:
                    startMenu.splash()
                    self.splashShow = False
                self.nextScreen = startMenu.menu()
            if self.nextScreen == "rules":
                self.nextScreen = rulesMenu.run()
                if self.nextScreen == "start":
                    startMenu.backToStart()
            if self.nextScreen == "options":
                self.nextScreen = optionsMenu.run()
                if self.nextScreen == "start":
                    startMenu.backToStart()
            #if self.nextScreen == "game":
                #self.nextScreen = Game.play()
                
                
Game().start()
