import pygame
from pygame.locals import *
import os
import sys
from rulesMenu import Rules
from startMenu import Start
from optionsMenu import Options
from GameArea import GameArea
from Sound import Sound

os.environ['SDL_VIDEO_CENTERED'] = '1'  # Center the display
pygame.mixer.pre_init(44100, -16, 2, 2048) # Setup mixer to avoid sound lag
pygame.init()

class Game(object):
    screen = None

    def __init__(self):
        #Get screen info and set window to full screen
        self.infoScreen = pygame.display.Info()

        #self.screen = pygame.display.set_mode((self.infoScreen.current_w, self.infoScreen.current_h),pygame.FULLSCREEN)
        self.heightRatio16x9 = .5625 #Number to multiply width by to get 16x9 ratio for height
        self.yOffset = int((self.infoScreen.current_h-int(self.infoScreen.current_w*self.heightRatio16x9))/2)

        #Temporary code to test multiple screen sizes 
        #Comment self.screen above
        self.qHD = (960, 540)
        self.HD = (1280, 720)
        self.HDplus = (1600, 900)
        self.fullHD = (1920, 1080)
        self.fourThreeRatio = (960, 720)
        self.screenSize = [self.qHD, self.HD, self.HDplus, self.fullHD, self.fourThreeRatio]
        self.size = 0
        self.ratio = self.screenSize[self.size][0]/1920
        if self.infoScreen.current_h == self.screenSize[self.size][1]\
           and self.infoScreen.current_w == self.screenSize[self.size][0]:
            self.screen = pygame.display.set_mode(self.screenSize[self.size],pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.screenSize[self.size]) #Select screen size
        self.yOffset = 0 #Set to 0 if not fullscreen, *set to .75 if fourThreeRatio selected
        
        pygame.display.set_caption("Mastering MSU")
        self.imgIconSmall = pygame.image.load(os.path.join("img","icon_small.png")).convert_alpha()
        pygame.display.set_icon(self.imgIconSmall)
        self.nextScreen = "start"
        self.splashShow = True

        self.intro = Sound('intro')
        self.click = Sound('click')
        self.bgMusic = Sound('start_menu')
        
        #self.round_number = 1

    def fontOp(self, size, fontName):  #Pick font size and type
        if fontName == "helvetica":
            fontAndSize = pygame.font.Font(os.path.join("font","helvetica.otf"),size) # "font" is directory for the font file
        elif fontName == "berlin":
            fontAndSize = pygame.font.Font(os.path.join("font","berlin.ttf"),size)
        return fontAndSize
        
    def start(self):
<<<<<<< HEAD
        startMenu = Start(self.screen, self.font_op, self.y_offset, self.intro, self.click, self.bgMusic)
        rulesMenu = Rules(self.screen, self.font_op, self.y_offset, self.click)
        optionsMenu = Options(self.screen, self.infoScreen, self.font_op, self.y_offset, self.click, self.bgMusic)
=======
        startMenu = Start(self.screen, self.fontOp, self.yOffset)
        rulesMenu = Rules(self.screen, self.fontOp, self.yOffset)
        optionsMenu = Options(self.screen, self.infoScreen, self.fontOp, self.yOffset)
>>>>>>> origin/Josh
        playGame = GameArea(self.screen, self.ratio)
        
        while True:
            if playGame.getScale() != self.screen.get_height()/1080:
                self.ratio = self.screen.get_height()/1080
                playGame = GameArea(self.screen, self.ratio)
            if self.nextScreen == "start":
                if self.splashShow:
                    startMenu.splash()
                    self.splashShow = False
                self.nextScreen = startMenu.menu()
            elif self.nextScreen == "rules":
                self.nextScreen = rulesMenu.run()
                if self.nextScreen == "start":
                    startMenu.backToStart()
            elif self.nextScreen == "options":
                self.nextScreen = optionsMenu.run()
                if self.nextScreen == "start":
                    startMenu.backToStart()
            elif self.nextScreen == "game":
                self.nextScreen = playGame.play()
                
                
Game().start()
