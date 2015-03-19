import pygame
from pygame.locals import *
import os
import sys
from RadioButton import RadioGroup
from CheckBox import CheckBox
from startMenu import Start


class Options(object):
    def __init__(self, screen, infoScreen, fontOp, yoffset):
        self.screen = screen
        self.infoScreen = infoScreen
        self.fontOp = fontOp
        self.yoffset = yoffset
        self.resolutionoption = 0
        self.soundeffectsoff = False
        self.musicoff = False
        self.loadImages()
        self.loadButtons(self.resolutionoption)
        self.screenmodes = [(960, 540), (1280, 720), (1600, 900), (1920, 1080), (960, 720)]

    def loadButtons(self, resolutionoption):
        # RADIO BUTTON GROUP
        self.resolutionbuttons = RadioGroup(self.screen)
        self.resolutionbuttons.newButton(self.screen.get_width() / 2 - 80, self.screen.get_height() / 2 - 54 + self.yoffset, 5)
        self.resolutionbuttons.newButton(self.screen.get_width() / 2 - 80, self.screen.get_height() / 2 - 34 + self.yoffset, 5)
        self.resolutionbuttons.newButton(self.screen.get_width() / 2 - 80, self.screen.get_height() / 2 - 14 + self.yoffset, 5)
        self.resolutionbuttons.newButton(self.screen.get_width() / 2 + 20, self.screen.get_height() / 2 - 54 + self.yoffset, 5)
        #self.resolutionbuttons.newButton(self.screen.get_width() / 2 + 20, self.screen.get_height() / 2 - 34 + self.yoffset, 5) #4:3 not supported yet
        # CHECKBOXES
        self.soundeffectscheckbox = CheckBox(self.screen, self.screen.get_width() / 2 - 80, self.screen.get_height() / 2 + 58 + self.yoffset, 10)
        self.musiccheckbox = CheckBox(self.screen, self.screen.get_width() / 2 - 80, self.screen.get_height()/2 + 78 + self.yoffset, 10)

        # FOR RELOADING BUTTONS
        # set the checked resolution box
        self.resolutionbuttons.setCurrent(resolutionoption)
        # if mute sound effects box should be checked check them, other wise leave unchecked
        if self.soundeffectsoff == True:
            if self.soundeffectscheckbox.getChecked() == False:
                self.soundeffectscheckbox.setChecked(self.screen.get_width() / 2 - 79, self.screen.get_height() / 2 + 59 + self.yoffset)
        else:
            if self.soundeffectscheckbox.getChecked() == True:
                self.soundeffectscheckbox.setChecked(self.screen.get_width() / 2 - 79, self.screen.get_height() / 2 + 59 + self.yoffset)
        # if mute music box should be checked check them, other wise leave unchecked
        if self.musicoff == True:
            if self.musiccheckbox.getChecked() == False:
                self.musiccheckbox.setChecked(self.screen.get_width() / 2 - 79, self.screen.get_height()/2 + 79 + self.yoffset)
        else:
            if self.musiccheckbox.getChecked() == True:
                self.musiccheckbox.setChecked(self.screen.get_width() / 2 - 79, self.screen.get_height()/2 + 79 + self.yoffset)


    def loadImages(self):
        self.imgmenubg = pygame.image.load(os.path.join("img", "menu_bg4.png")).convert()

    def buttonClick(self):
        mousex, mousey = pygame.mouse.get_pos()

        if mousex > self.screen.get_width() / 2 + 178 \
                and mousex < self.screen.get_width() / 2 + 198 \
                and mousey > self.screen.get_height() / 2 - 123 + self.yoffset and mousey < self.screen.get_height() / 2 - 103 + self.yoffset:
            return False

        if self.resolutionbuttons.checkButton(mousex, mousey):
            self.resolutionoption = self.resolutionbuttons.getCurrent()
            if self.infoScreen.current_h == self.screenmodes[self.resolutionbuttons.getCurrent()][1]\
               and self.infoScreen.current_w == self.screenmodes[self.resolutionbuttons.getCurrent()][0]:
                self.screen = pygame.display.set_mode(self.screenmodes[self.resolutionbuttons.getCurrent()], pygame.FULLSCREEN)
            else:
                self.screen = pygame.display.set_mode(self.screenmodes[self.resolutionbuttons.getCurrent()])

        self.soundeffectscheckbox.setChecked(mousex, mousey)
        self.soundeffectsoff = self.soundeffectscheckbox.getChecked()

        self.musiccheckbox.setChecked(mousex, mousey)
        self.musicoff = self.musiccheckbox.getChecked()
        if self.musiccheckbox.getChecked() == True:
            pygame.mixer.Sound(os.path.join('sound','start_menu.wav')).stop()

        return True

    def run(self):
        optionsexit = False
        while not optionsexit:
            # background image
            self.screen.blit(self.imgmenubg, (0, 0))
            self.screen.blit(pygame.transform.scale(self.imgmenubg,(self.screen.get_width(), int(self.screen.get_height()-(2*self.yoffset)))),(0,self.yoffset))
            # rectangle window w/ exit button
            self.text_exit_options = self.fontOp(22, "helvetica").render("X", True, (255, 0, 0))
            pygame.draw.rect(self.screen, (126, 51, 58), Rect((self.screen.get_width() / 2 - 200, self.screen.get_height() / 2 - 125 + self.yoffset), (400, 250 + self.yoffset)))
            pygame.draw.rect(self.screen, (255, 255, 255), Rect((self.screen.get_width() / 2 + 178, self.screen.get_height() / 2 - 123 + self.yoffset), (self.text_exit_options.get_width() + 6, 20)))
            self.screen.blit(self.text_exit_options, (self.screen.get_width() / 2 + 182, self.screen.get_height() / 2 - 127 + self.yoffset))
            pygame.draw.rect(self.screen, (94, 0, 9), Rect((self.screen.get_width() / 2 - 200, self.screen.get_height() / 2 - 125 + self.yoffset), (400, 250 + self.yoffset)), 2)
            # header
            header = self.fontOp(50, "berlin").render("Game Options", True, (255, 255, 255))
            self.screen.blit(header, (self.screen.get_width() / 2 - 0.5 * header.get_width(), 4+self.yoffset))
            # video options
            videooptions = self.fontOp(20, "berlin").render("Video options", True, (255, 255, 255))
            self.screen.blit(videooptions, (self.screen.get_width() / 2 - 0.5 * videooptions.get_width(), self.screen.get_height() / 2 - 110 + self.yoffset))
            screenresolution = self.fontOp(12, "berlin").render("Screen Resolution", True, (255, 255, 255))
            self.screen.blit(screenresolution, (self.screen.get_width() / 2 - 0.5 * screenresolution.get_width(), self.screen.get_height() / 2 - 80 + self.yoffset))
            self.resolutiontext1 = self.fontOp(10, "berlin").render("960x540", True, (255, 255, 255))
            self.resolutiontext2 = self.fontOp(10, "berlin").render("1280x720", True, (255, 255, 255))
            self.resolutiontext3 = self.fontOp(10, "berlin").render("1600x900", True, (255, 255, 255))
            self.resolutiontext4 = self.fontOp(10, "berlin").render("1920x1080", True, (255, 255, 255))
            self.resolutiontext5 = self.fontOp(10, "berlin").render("960x720", True, (255, 255, 255))
            self.screen.blit(self.resolutiontext1, (self.screen.get_width() / 2 - 70, self.screen.get_height() / 2 - 60 + self.yoffset))
            self.screen.blit(self.resolutiontext2, (self.screen.get_width() / 2 - 70, self.screen.get_height() / 2 - 40 + self.yoffset))
            self.screen.blit(self.resolutiontext3, (self.screen.get_width() / 2 - 70, self.screen.get_height() / 2 - 20 + self.yoffset))
            self.screen.blit(self.resolutiontext4, (self.screen.get_width() / 2 + 30, self.screen.get_height() / 2 - 60 + self.yoffset))
            #self.screen.blit(self.resolutiontext5, (self.screen.get_width() / 2 + 30, self.screen.get_height() / 2 - 40 + self.yoffset)) #4:3 not supported yet
            self.resolutionbuttons.draw()

            # audio option
            audiooptions = self.fontOp(20, "berlin").render("Audio options", True, (255, 255, 255))
            self.screen.blit(audiooptions, (self.screen.get_width() / 2 - 0.5 * audiooptions.get_width(), self.screen.get_height() / 2 + 30 + self.yoffset))
            self.textsoundeffectoption = self.fontOp(12, "berlin").render("Mute sound effects", True, (255, 255, 255))
            self.textmusicoption = self.fontOp(12, "berlin").render("Mute music", True, (255, 255, 255))
            self.screen.blit(self.textsoundeffectoption, (self.screen.get_width() / 2 - 60, self.screen.get_height()/2 + 55 + self.yoffset))
            self.screen.blit(self.textmusicoption, (self.screen.get_width() / 2 - 60, self.screen.get_height()/2 + 75 + self.yoffset))
            self.soundeffectscheckbox.draw()
            self.musiccheckbox.draw()

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        optionsexit = True
                        break
                elif event.type == MOUSEBUTTONDOWN:  # Perform action on click
                    if not self.buttonClick():
                        optionsexit = True
                        break
                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            self.loadButtons(self.resolutionoption)
            pygame.display.update()
        return "start"
