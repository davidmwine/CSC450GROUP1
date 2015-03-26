import pygame
import sys
import os
from Controls import Button
from RadioButton import RadioGroup


class PopupMenu(object):
    def __init__(self, parent):
        self.displayInfo = pygame.display.Info()
        self.clock = pygame.time.Clock()
        self.parent = parent
        self.width = self.parent.get_width() / 2
        self.height = self.parent.get_height() / 2
        self.area = parent.subsurface((self.parent.get_width() / 4), (self.parent.get_height() / 4), self.width, self.height)
        self.screenModes = [(960, 540), (1280, 720), (1600, 900), (1920, 1080), (960, 720)]## various screen sizes available
        self.resOpt = self.screenModes.index((self.displayInfo.current_w, self.displayInfo.current_h)) # current resolution option
        self.popupActive = False
        self.optionActive = False
        self.exitCheckActive = False

    def loadButtons(self):
        # RADIO BUTTON GROUP
        self.resolveButton = RadioGroup(self.area)
        self.resolveButton.newButton(self.area.get_width() / 2 - 80, self.area.get_height() / 2 + 5, 5)
        self.resolveButton.newButton(self.area.get_width() / 2 - 80, self.area.get_height() / 2 + 25, 5)
        self.resolveButton.newButton(self.area.get_width() / 2 - 80, self.area.get_height() / 2 + 45, 5)
        self.resolveButton.newButton(self.area.get_width() / 2 + 20, self.area.get_height() / 2 + 5, 5)
        #self.resolveButton.newButton(self._area.get_width() / 2 + 20, self._area.get_height() / 2 + 25, 5) #4:3 not supported yet
        self.resolveButton.setCurrent(self.resOpt)
        
    def changeResolution(self, X, Y):
        # supposed to check radio button and return whichever resolution was selected
        if self.resolveButton.checkButton(X - self.parent.get_width() / 4, Y - self.parent.get_height() / 4):
            self.resOpt = self.resolveButton.getCurrent()
            return self.screenModes[self.resolveButton.getCurrent()]
        else:
            return None

    def makePopupMenu(self):
        self.popupActive = True
        self.optionActive = False
        self.exitCheckActive = False
        self.area.fill((190, 192, 194))
        self.textOptions = pygame.font.Font(os.path.join("font","berlin.ttf"), 30).render("Options", True, (94, 0, 9))
        self.area.blit(self.textOptions, (self.area.get_width()/2 - (0.5 * self.textOptions.get_width()), 5))
        self.resumeButton = Button(self.area, pygame.Rect(self.area.get_width() / 2 - 100, self.area.get_height() / 2 - 80, 200, 30), "Resume Game", (94, 0, 9), (190, 192, 194))
        self.saveButton = Button(self.area, pygame.Rect(self.area.get_width() / 2 - 100, self.area.get_height() / 2 - 40, 200, 30), "Save Game", (94, 0, 9), (190, 192, 194))
        self.gameOptionsButton = Button(self.area, pygame.Rect(self.area.get_width() / 2 - 100, self.area.get_height() / 2, 200, 30), "Game Options", (94, 0, 9), (190, 192, 194))
        self.exitButton = Button(self.area, pygame.Rect(self.area.get_width() / 2 - 100, self.area.get_height() / 2 + 40, 200, 30), "Exit Game", (94, 0, 9), (190, 192, 194))

    def gameOptions(self):
        self.popupActive = True
        self.optionActive = True
        self.exitCheckActive = False
        self.area.fill((190, 192, 194))
        # header
        self.textOptions = pygame.font.Font(os.path.join("font","berlin.ttf"), 30).render("Game Options", True, (94, 0, 9))
        self.area.blit(self.textOptions, (self.area.get_width()/2 - (0.5 * self.textOptions.get_width()), 5))

        # back button
        self.exitButton = Button(self.area, pygame.Rect(self.area.get_width() / 2 - 100, self.area.get_height() / 2 - 80, 200, 30), "Back", (94, 0, 9), (190, 192, 194))

        # resolution options
        self.loadButtons()
        self.textResolution = pygame.font.Font(os.path.join("font","berlin.ttf"), 20).render("Resolution Options", True, (94, 0, 9))
        self.area.blit(self.textResolution, (self.area.get_width() / 2 - (0.5 * self.textResolution.get_width()), self.area.get_height() / 2 - 30))
        self.resolutionText1 = pygame.font.Font(os.path.join("font", "berlin.ttf"), 10).render("960x540", True, (0, 0, 0))
        self.resolutionText2 = pygame.font.Font(os.path.join("font", "berlin.ttf"), 10).render("1280x720", True, (0, 0, 0))
        self.resolutionText3 = pygame.font.Font(os.path.join("font", "berlin.ttf"), 10).render("1600x900", True, (0, 0, 0))
        self.resolutionText4 = pygame.font.Font(os.path.join("font", "berlin.ttf"), 10).render("1920x1080", True, (0, 0, 0))
        # self.resolutionText5 = pygame.font.Font(os.path.join("font", "berlin.ttf"), 10).render("960x720", True, (0, 0, 0))
        self.area.blit(self.resolutionText1, (self.area.get_width() / 2 - 70, self.area.get_height() / 2))
        self.area.blit(self.resolutionText2, (self.area.get_width() / 2 - 70, self.area.get_height() / 2 + 20))
        self.area.blit(self.resolutionText3, (self.area.get_width() / 2 - 70, self.area.get_height() / 2 + 40))
        self.area.blit(self.resolutionText4, (self.area.get_width() / 2 + 30, self.area.get_height() / 2))
        #self._area.blit(self.resolutionText5, (self._area.get_width() / 2 + 30, self._area.get_height() / 2 + 20)) #4:3 not supported yet
        self.resolveButton.draw()

    def exitCheck(self):
        self.popupActive = True
        self.optionActive = False
        self.exitCheckActive = True
        self.area.fill((190, 192, 194))
        self.text = pygame.font.Font(os.path.join("font","berlin.ttf"), 20).render("Are you sure you want to exit?", True, (94, 0, 9))
        self.area.blit(self.text, (self.area.get_width()/2 - (0.5 * self.text.get_width()), 5))
        self.exitButtonYes = Button(self.area, pygame.Rect(self.area.get_width() / 2 - 100, self.area.get_height() / 2 - 60, 200, 30), "Yes", (94, 0, 9), (190, 192, 194))
        self.exitButtonNo = Button(self.area, pygame.Rect(self.area.get_width() / 2 - 100, self.area.get_height() / 2 - 20, 200, 30), "No", (94, 0, 9), (190, 192, 194))

    def getWidth(self):
        return self.area.get_width()

    def getHeight(self):
        return self.area.get_height()

    def getPopupActive(self):
        return self.popupActive

    def setPopupActive(self, x):
        self.popupActive = x

    def getOptionsActive(self):
        return self.optionActive

    def setOptionsActive(self, x):
        self.optionActive = x

    def getExitCheckActive(self):
        return self.exitCheckActive

    def setExitCheckActive(self, x):
        self.ExitCheckActive = x
