import pygame
from pygame.locals import *
import os
import sys
from RadioButton import RadioGroup
from CheckBox import CheckBox
from StartMenu import Start


class Options(object):
    def __init__(self, screen, infoScreen, fontOp, yOffset):
        self.screen = screen
        self.infoScreen = infoScreen
        self.fontOp = fontOp
        self.yOffset = yOffset
        self.resolutionOption = 0
        self.soundEffectsOff = False
        self.musicOff = False
        self.loadImages()
        self.loadButtons(self.resolutionOption)
        self.screenModes = [(960, 540), (1280, 720), (1600, 900), (1920, 1080), (960, 720)]

    def loadButtons(self, resolutionOption):
        # RADIO BUTTON GROUP
        self.resolutionButtons = RadioGroup(self.screen)
        self.resolutionButtons.newButton(self.screen.get_width() / 2 - 80, self.screen.get_height() / 2 - 54 + self.yOffset, 5)
        self.resolutionButtons.newButton(self.screen.get_width() / 2 - 80, self.screen.get_height() / 2 - 34 + self.yOffset, 5)
        self.resolutionButtons.newButton(self.screen.get_width() / 2 - 80, self.screen.get_height() / 2 - 14 + self.yOffset, 5)
        self.resolutionButtons.newButton(self.screen.get_width() / 2 + 20, self.screen.get_height() / 2 - 54 + self.yOffset, 5)
        #self.resolutionButtons.newButton(self.screen.get_width() / 2 + 20, self.screen.get_height() / 2 - 34 + self.yOffset, 5) #4:3 not supported yet
        # CHECKBOXES
        self.soundEffectsCheckbox = CheckBox(self.screen, self.screen.get_width() / 2 - 80, self.screen.get_height() / 2 + 58 + self.yOffset, 10)
        self.musicCheckbox = CheckBox(self.screen, self.screen.get_width() / 2 - 80, self.screen.get_height()/2 + 78 + self.yOffset, 10)

        # FOR RELOADING BUTTONS
        # set the checked resolution box
        self.resolutionButtons.setCurrent(resolutionOption)
        # if mute sound effects box should be checked check them, other wise leave unchecked
        if self.soundEffectsOff == True:
            if self.soundEffectsCheckbox.getChecked() == False:
                self.soundEffectsCheckbox.setChecked(self.screen.get_width() / 2 - 79, self.screen.get_height() / 2 + 59 + self.yOffset)
        else:
            if self.soundEffectsCheckbox.getChecked() == True:
                self.soundEffectsCheckbox.setChecked(self.screen.get_width() / 2 - 79, self.screen.get_height() / 2 + 59 + self.yOffset)
        # if mute music box should be checked check them, other wise leave unchecked
        if self.musicOff == True:
            if self.musicCheckbox.getChecked() == False:
                self.musicCheckbox.setChecked(self.screen.get_width() / 2 - 79, self.screen.get_height()/2 + 79 + self.yOffset)
        else:
            if self.musicCheckbox.getChecked() == True:
                self.musicCheckbox.setChecked(self.screen.get_width() / 2 - 79, self.screen.get_height()/2 + 79 + self.yOffset)


    def loadImages(self):
        self.imgMenuBG = pygame.image.load(os.path.join("img", "menu_bg4.png")).convert()

    def buttonClick(self):
        mouseX, mouseY = pygame.mouse.get_pos()

        if mouseX > self.screen.get_width() / 2 + 178 \
                and mouseX < self.screen.get_width() / 2 + 198 \
                and mouseY > self.screen.get_height() / 2 - 123 + self.yOffset and mouseY < self.screen.get_height() / 2 - 103 + self.yOffset:
            return False

        if self.resolutionButtons.checkButton(mouseX, mouseY):
            self.resolutionOption = self.resolutionButtons.getCurrent()
            if self.infoScreen.current_h == self.screenModes[self.resolutionButtons.getCurrent()][1]\
               and self.infoScreen.current_w == self.screenModes[self.resolutionButtons.getCurrent()][0]:
                self.screen = pygame.display.set_mode(self.screenModes[self.resolutionButtons.getCurrent()], pygame.FULLSCREEN)
            else:
                self.screen = pygame.display.set_mode(self.screenModes[self.resolutionButtons.getCurrent()])

        self.soundEffectsCheckbox.setChecked(mouseX, mouseY)
        self.soundEffectsOff = self.soundEffectsCheckbox.getChecked()

        self.musicCheckbox.setChecked(mouseX, mouseY)
        self.musicOff = self.musicCheckbox.getChecked()
        if self.musicCheckbox.getChecked() == True:
            pygame.mixer.Sound(os.path.join('sound','start_menu.wav')).stop()

        return True

    def run(self):
        optionsExit = False
        while not optionsExit:
            # background image
            self.screen.blit(self.imgMenuBG, (0, 0))
            self.screen.blit(pygame.transform.scale(self.imgMenuBG,(self.screen.get_width(), int(self.screen.get_height()-(2*self.yOffset)))),(0,self.yOffset))
            # rectangle window w/ exit button
            self.textExitOptions = self.fontOp(22, "helvetica").render("X", True, (255, 0, 0))
            pygame.draw.rect(self.screen, (126, 51, 58), Rect((self.screen.get_width() / 2 - 200, self.screen.get_height() / 2 - 125 + self.yOffset), (400, 250 + self.yOffset)))
            pygame.draw.rect(self.screen, (255, 255, 255), Rect((self.screen.get_width() / 2 + 178, self.screen.get_height() / 2 - 123 + self.yOffset), (self.textExitOptions.get_width() + 6, 20)))
            self.screen.blit(self.textExitOptions, (self.screen.get_width() / 2 + 182, self.screen.get_height() / 2 - 127 + self.yOffset))
            pygame.draw.rect(self.screen, (94, 0, 9), Rect((self.screen.get_width() / 2 - 200, self.screen.get_height() / 2 - 125 + self.yOffset), (400, 250 + self.yOffset)), 2)
            # header
            header = self.fontOp(50, "berlin").render("Game Options", True, (255, 255, 255))
            self.screen.blit(header, (self.screen.get_width() / 2 - 0.5 * header.get_width(), 4+self.yOffset))
            # video options
            videoOptions = self.fontOp(20, "berlin").render("Video options", True, (255, 255, 255))
            self.screen.blit(videoOptions, (self.screen.get_width() / 2 - 0.5 * videoOptions.get_width(), self.screen.get_height() / 2 - 110 + self.yOffset))
            screenResolution = self.fontOp(12, "berlin").render("Screen Resolution", True, (255, 255, 255))
            self.screen.blit(screenResolution, (self.screen.get_width() / 2 - 0.5 * screenResolution.get_width(), self.screen.get_height() / 2 - 80 + self.yOffset))
            self.resolutionText1 = self.fontOp(10, "berlin").render("960x540", True, (255, 255, 255))
            self.resolutionText2 = self.fontOp(10, "berlin").render("1280x720", True, (255, 255, 255))
            self.resolutionText3 = self.fontOp(10, "berlin").render("1600x900", True, (255, 255, 255))
            self.resolutionText4 = self.fontOp(10, "berlin").render("1920x1080", True, (255, 255, 255))
            self.resolutionText5 = self.fontOp(10, "berlin").render("960x720", True, (255, 255, 255))
            self.screen.blit(self.resolutionText1, (self.screen.get_width() / 2 - 70, self.screen.get_height() / 2 - 60 + self.yOffset))
            self.screen.blit(self.resolutionText2, (self.screen.get_width() / 2 - 70, self.screen.get_height() / 2 - 40 + self.yOffset))
            self.screen.blit(self.resolutionText3, (self.screen.get_width() / 2 - 70, self.screen.get_height() / 2 - 20 + self.yOffset))
            self.screen.blit(self.resolutionText4, (self.screen.get_width() / 2 + 30, self.screen.get_height() / 2 - 60 + self.yOffset))
            #self.screen.blit(self.resolutionText5, (self.screen.get_width() / 2 + 30, self.screen.get_height() / 2 - 40 + self.yOffset)) #4:3 not supported yet
            self.resolutionButtons.draw()

            # audio option
            audioOptions = self.fontOp(20, "berlin").render("Audio options", True, (255, 255, 255))
            self.screen.blit(audioOptions, (self.screen.get_width() / 2 - 0.5 * audioOptions.get_width(), self.screen.get_height() / 2 + 30 + self.yOffset))
            self.textSoundEffectOption = self.fontOp(12, "berlin").render("Mute sound effects", True, (255, 255, 255))
            self.textMusicOption = self.fontOp(12, "berlin").render("Mute music", True, (255, 255, 255))
            self.screen.blit(self.textSoundEffectOption, (self.screen.get_width() / 2 - 60, self.screen.get_height()/2 + 55 + self.yOffset))
            self.screen.blit(self.textMusicOption, (self.screen.get_width() / 2 - 60, self.screen.get_height()/2 + 75 + self.yOffset))
            self.soundEffectsCheckbox.draw()
            self.musicCheckbox.draw()

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        optionsExit = True
                        break
                elif event.type == MOUSEBUTTONDOWN:  # Perform action on click
                    if not self.buttonClick():
                        optionsExit = True
                        break
                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            self.loadButtons(self.resolutionOption)
            pygame.display.update()
        return "start"
