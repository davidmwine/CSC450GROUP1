''' Sound and resolution options in start menu '''
import pygame
from pygame.locals import *
import os
import sys
from RadioButton import RadioGroup
from StartMenu import Start

class Options(object):
    def __init__(self, screen, infoScreen, fontOp, yOffset, bgMusic, click, soundOn):
        self.screen = screen
        self.infoScreen = infoScreen
        self.fontOp = fontOp
        self.yOffset = yOffset
        resIndex = {960: 0, 1280: 1, 1600: 2, 1920: 3}
        self.resolutionOption = resIndex[self.screen.get_width()]
        self.soundEffectsOff = False
        self.musicOff = pygame.mixer.get_busy()
        self.loadImages()
        self.loadText()
        self.loadButtons(self.resolutionOption)
        self.screenModes = [(960, 540), (1280, 720), (1600, 900), (1920, 1080), (960, 720)]
        self.click = click
        self.bgMusic = bgMusic
        self.sonarSound = pygame.mixer.Sound(os.path.join('sound','sonar.wav'))   #Sound option button
        self.btsound = pygame.mixer.Sound(os.path.join('sound','button.wav'))     #Screen resolution option button
        self.soundOn = soundOn
        print("MIXER BUSY IS", self.soundOn)

    def loadButtons(self, resolutionOption):
        #Radio button group
        self.resolutionButtons = RadioGroup(self.screen)
        self.resolutionButtons.newButton(self.screen.get_width() / 2 - 140, self.screen.get_height() / 2 + 46 + self.yOffset, 5)
        self.resolutionButtons.newButton(self.screen.get_width() / 2 - 140, self.screen.get_height() / 2 + 66 + self.yOffset, 5)
        self.resolutionButtons.newButton(self.screen.get_width() / 2 - 140, self.screen.get_height() / 2 + 86 + self.yOffset, 5)
        self.resolutionButtons.newButton(self.screen.get_width() / 2 - 140, self.screen.get_height() / 2 + 106 + self.yOffset, 5)

        #FOR RELOADING BUTTONS
        #Set the checked resolution box
        self.resolutionButtons.setCurrent(resolutionOption)
  
    def loadImages(self):
        self.img_menu_bg = pygame.image.load(os.path.join("img", "menu_bg4.png")).convert()
        self.img_on = pygame.image.load(os.path.join("img", "on_small.png")).convert_alpha()
        self.img_off = pygame.image.load(os.path.join("img", "off_small.png")).convert_alpha()

    def loadText(self):
        self.text_exit_options = self.fontOp(18,"berlin").render("Exit",True,(220,146,40))
        self.screen_resolution = self.fontOp(26, "berlin").render("Screen", True, (220,146,40))
        self.screen_resolution2 = self.fontOp(26, "berlin").render("Resolution", True, (220,146,40))
        self.header = self.fontOp(50, "berlin").render("Game Options", True, (255, 255, 255))
        self.resoultion_text_1 = self.fontOp(18, "berlin").render("960x540", True, (255, 255, 255))
        self.resoultion_text_2 = self.fontOp(18, "berlin").render("1280x720", True, (255, 255, 255))
        self.resoultion_text_3 = self.fontOp(18, "berlin").render("1600x900", True, (255, 255, 255))
        self.resoultion_text_4 = self.fontOp(18, "berlin").render("1920x1080", True, (255, 255, 255))
        self.audio_options = self.fontOp(26, "berlin").render("Sound", True, (220,146,40))
        #self.text_sound_effect_option = self.fontOp(18, "berlin").render("Effects", True, (255, 255, 255))
        self.text_music_option = self.fontOp(18, "berlin").render("Music", True, (255, 255, 255))

    def drawCircles(self):
        circle_color = [0,0,0]
        circle_color2 = [255,255,255]
        circle_size = 110
        circle_size2 = 102
        circle_edge_thickness = 4
        #Screen resolution circles
        pygame.draw.circle(self.screen, circle_color, (self.screen.get_width() // 2 - 100, \
                                                        self.screen.get_height() // 2 + 50), circle_size)
        pygame.draw.circle(self.screen, circle_color2, (self.screen.get_width() // 2 - 100, \
                                                        self.screen.get_height() // 2 + 50), circle_size2, circle_edge_thickness)
        circle_size = 100
        circle_size2 = 92 
        #Audio circles
        pygame.draw.circle(self.screen, circle_color, (self.screen.get_width() // 2 + 125, \
                                                        self.screen.get_height() // 2 + 165), circle_size)
        pygame.draw.circle(self.screen, circle_color2, (self.screen.get_width() // 2 + 125, \
                                                        self.screen.get_height() // 2 + 165), circle_size2, circle_edge_thickness)
        circle_size = 35
        circle_size2 = 27
        #Exit circles
        pygame.draw.circle(self.screen, circle_color, (self.screen.get_width() // 2 + 143, \
                                                        self.screen.get_height() // 2 - 86), circle_size)
        pygame.draw.circle(self.screen, circle_color2, (self.screen.get_width() // 2 + 143, \
                                                        self.screen.get_height() // 2 - 86), circle_size2, circle_edge_thickness)
        
    def buttonClick(self):
        mouseX, mouseY = pygame.mouse.get_pos()

        #Exit button
        if mouseX > self.screen.get_width() / 2 + 105 \
                and mouseX < self.screen.get_width() / 2 + 180 \
                and mouseY > self.screen.get_height() / 2 - 125 + self.yOffset \
                and mouseY < self.screen.get_height() / 2 - 50 + self.yOffset:
            self.click.play()
            return False

        if self.resolutionButtons.checkButton(mouseX, mouseY):
            self.btsound.play()
            self.resolutionOption = self.resolutionButtons.getCurrent()
            if self.infoScreen.current_h == self.screenModes[self.resolutionButtons.getCurrent()][1]\
               and self.infoScreen.current_w == self.screenModes[self.resolutionButtons.getCurrent()][0]:
                self.screen = pygame.display.set_mode(self.screenModes[self.resolutionButtons.getCurrent()], pygame.FULLSCREEN)
            else:
                self.screen = pygame.display.set_mode(self.screenModes[self.resolutionButtons.getCurrent()])

        '''#Effects button
        if mouseX > self.screen.get_width() / 2 + 132 \
                and mouseX < self.screen.get_width() / 2 + 177 \
                and mouseY > self.screen.get_height() / 2 + 186 + self.yOffset \
                and mouseY < self.screen.get_height() / 2 + 205 + self.yOffset:
            self.click.play()
            self.soundEffectsOff = not self.soundEffectsOff
            self.click.setSound('click')
            self.click.play()'''


        #Music button
        if mouseX > self.screen.get_width() / 2 + 132 \
                and mouseX < self.screen.get_width() / 2 + 177 \
                and mouseY > self.screen.get_height() / 2 + 160 + self.yOffset \
                and mouseY < self.screen.get_height() / 2 + 181 + self.yOffset:
            #self.bgMusic.setSound('start_menu')
            if self.soundOn:
                pygame.mixer.stop()
                self.soundOn = False
            else:
                self.bgMusic.play()
                self.soundOn = True
            self.sonarSound.play()
                
        return True

    def run(self):
        options_exit = False
        while not options_exit:
            #Background image
            self.screen.blit(pygame.transform.scale(self.img_menu_bg,(self.screen.get_width(), \
                                                            int(self.screen.get_height() - (2 * self.yOffset)))),(0, self.yOffset))
            #Draw circles
            self.drawCircles()

            #Header
            self.screen.blit(self.header, (self.screen.get_width() / 2 - 0.5 * self.header.get_width(), 4 + self.yOffset))

            #Exit 
            self.screen.blit(self.text_exit_options, (self.screen.get_width() / 2 + 128, \
                                                      self.screen.get_height() / 2 - 97 + self.yOffset))
            #Video options
            self.screen.blit(self.screen_resolution, (self.screen.get_width() / 2 - 0.5 * self.screen_resolution.get_width() - 100, \
                                                      self.screen.get_height() / 2 - 28 + self.yOffset))
            self.screen.blit(self.screen_resolution2, (self.screen.get_width() / 2 - 0.5 * self.screen_resolution2.get_width() - 100, \
                                                      self.screen.get_height() / 2 - 5 + self.yOffset))
            self.screen.blit(self.resoultion_text_1, (self.screen.get_width() / 2 - 130, self.screen.get_height() / 2 + 34 + self.yOffset))
            self.screen.blit(self.resoultion_text_2, (self.screen.get_width() / 2 - 130, self.screen.get_height() / 2 + 54 + self.yOffset))
            self.screen.blit(self.resoultion_text_3, (self.screen.get_width() / 2 - 130, self.screen.get_height() / 2 + 74 + self.yOffset))
            self.screen.blit(self.resoultion_text_4, (self.screen.get_width() / 2 - 130, self.screen.get_height() / 2 + 94 + self.yOffset))
            self.resolutionButtons.draw()

            #Audio options
            self.screen.blit(self.audio_options, (self.screen.get_width() / 2 - 0.5 * self.audio_options.get_width() + 125, \
                                                  self.screen.get_height() / 2 + 123 + self.yOffset))
            self.screen.blit(self.text_music_option, (self.screen.get_width() / 2 + 78, \
                                                  self.screen.get_height()/2 + 162 + self.yOffset))
            #self.screen.blit(self.text_sound_effect_option, (self.screen.get_width() / 2 + 78, \
                                                  #self.screen.get_height()/2 + 184 + self.yOffset))

            #Audio on/off buttons      
            if self.soundOn:
                self.screen.blit(self.img_on,(self.screen.get_width()/2 + 133,self.screen.get_height()/2 + 163 + self.yOffset))
            else:
                self.screen.blit(self.img_off,(self.screen.get_width()/2+ 133,self.screen.get_height()/2 + 163 + self.yOffset))

            '''if self.soundEffectsOff == False:
                self.screen.blit(self.img_on,(self.screen.get_width()/2 + 133,self.screen.get_height()/2 + 186 + self.yOffset))
            else:
                self.screen.blit(self.img_off,(self.screen.get_width()/2 + 133,self.screen.get_height()/2 + 186 + self.yOffset))
            '''
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        options_exit = True
                        break
                elif event.type == MOUSEBUTTONDOWN:
                    if not self.buttonClick():
                        options_exit = True
                        break
                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            self.loadButtons(self.resolutionOption)
            pygame.display.update()
        return "start"
