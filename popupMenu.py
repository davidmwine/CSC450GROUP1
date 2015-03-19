import pygame
import sys
import os
from Controls import Button
from Radiobutton import RadioGroup


class PopupMenu(object):
    def __init__(self, parent):
        self.displayInfo = pygame.display.Info()
        self.clock = pygame.time.Clock()
        self.parent = parent
        self.width = self.parent.get_width() / 2
        self.height = self.parent.get_height() / 2
        self.area = parent.subsurface((self.parent.get_width() / 4), (self.parent.get_height() / 4), self.width, self.height)
        self.screenmodes = [(960, 540), (1280, 720), (1600, 900), (1920, 1080), (960, 720)]## various screen sizes available
        self.resopt = self.screenmodes.index((self.displayInfo.current_w, self.displayInfo.current_h)) # current resolution option
        self.popupActive = False
        self.optionActive = False
        self.exitCheckActive = False

    def loadButtons(self):
        # RADIO BUTTON GROUP
        self.resolvebutton = RadioGroup(self._area)
        self.resolvebutton.newButton(self.area.get_width() / 2 - 80, self.area.get_height() / 2 + 5, 5)
        self.resolvebutton.newButton(self.area.get_width() / 2 - 80, self.area.get_height() / 2 + 25, 5)
        self.resolvebutton.newButton(self.area.get_width() / 2 - 80, self.area.get_height() / 2 + 45, 5)
        self.resolvebutton.newButton(self.area.get_width() / 2 + 20, self.area.get_height() / 2 + 5, 5)
        #self.resolution_radio_buttons.newButton(self._area.get_width() / 2 + 20, self._area.get_height() / 2 + 25, 5) #4:3 not supported yet
        self.resolvebutton.setCurrent(self.resopt)

    def changeResolution(self, X, Y):
        # supposed to check radio button and return whichever resolution was selected
        if self.resolvebutton.checkButton(X, Y):
            self.resopt = self.resolvebutton.getCurrent()
            return self.screenmodes[self.resolvebutton.getCurrent()]
        else:
            return None

    def makePopupMenu(self):
        self.popupActive = True
        self.optionActive = False
        self.exitCheckActive = False
        self.area.fill((190, 192, 194))
        self.textoptions = pygame.font.Font(os.path.join("font","berlin.ttf"), 30).render("Options", True, (94, 0, 9))
        self.area.blit(self.textOptions, (self.area.get_width()/2 - (0.5 * self.textoptions.get_width()), 5))
        self.resumebutton = Button(self.area, pygame.Rect(self.area.get_width() / 2 - 100, self.area.get_height() / 2 - 80, 200, 30), "Resume Game", (94, 0, 9), (190, 192, 194))
        self.savebutton = Button(self.area, pygame.Rect(self.area.get_width() / 2 - 100, self.area.get_height() / 2 - 40, 200, 30), "Save Game", (94, 0, 9), (190, 192, 194))
        self.gameoptionsbutton = Button(self.area, pygame.Rect(self.area.get_width() / 2 - 100, self.area.get_height() / 2, 200, 30), "Game Options", (94, 0, 9), (190, 192, 194))
        self.exitbutton = Button(self.area, pygame.Rect(self.area.get_width() / 2 - 100, self.area.get_height() / 2 + 40, 200, 30), "Exit Game", (94, 0, 9), (190, 192, 194))

    def gameOptions(self):
        self.popupActive = True
        self.optionActive = True
        self.exitCheckActive = False
        self.area.fill((190, 192, 194))
        # header
        self.textoptions = pygame.font.Font(os.path.join("font","berlin.ttf"), 30).render("Game Options", True, (94, 0, 9))
        self.area.blit(self.textoptions, (self.area.get_width()/2 - (0.5 * self.textoptions.get_width()), 5))

        # back button
        self.exitbutton = Button(self.area, pygame.Rect(self.area.get_width() / 2 - 100, self.area.get_height() / 2 - 80, 200, 30), "Back", (94, 0, 9), (190, 192, 194))

        # resolution options
        self.loadButtons()
        self.textresolution = pygame.font.Font(os.path.join("font","berlin.ttf"), 20).render("Resolution Options", True, (94, 0, 9))
        self.area.blit(self.textresolution, (self.area.get_width() / 2 - (0.5 * self.textresolution.get_width()), self.area.get_height() / 2 - 30))
        self.resoultiontext1 = pygame.font.Font(os.path.join("font", "berlin.ttf"), 10).render("960x540", True, (0, 0, 0))
        self.resoultiontext2 = pygame.font.Font(os.path.join("font", "berlin.ttf"), 10).render("1280x720", True, (0, 0, 0))
        self.resoultiontext3 = pygame.font.Font(os.path.join("font", "berlin.ttf"), 10).render("1600x900", True, (0, 0, 0))
        self.resoultiontext4 = pygame.font.Font(os.path.join("font", "berlin.ttf"), 10).render("1920x1080", True, (0, 0, 0))
        # self.resoultion_text_5 = pygame.font.Font(os.path.join("font", "berlin.ttf"), 10).render("960x720", True, (0, 0, 0))
        self.area.blit(self.resoultiontext1, (self.area.get_width() / 2 - 70, self.area.get_height() / 2))
        self.area.blit(self.resoultiontext2, (self.area.get_width() / 2 - 70, self.area.get_height() / 2 + 20))
        self.area.blit(self.resoultiontext3, (self.area.get_width() / 2 - 70, self.area.get_height() / 2 + 40))
        self.area.blit(self.resoultiontext4, (self.area.get_width() / 2 + 30, self.area.get_height() / 2))
        #self._area.blit(self.resoultion_text_5, (self._area.get_width() / 2 + 30, self._area.get_height() / 2 + 20)) #4:3 not supported yet
        self.resolvebutton.draw()

    def exit_check(self):
        self.popupActive = True
        self.optionActive = False
        self.exitCheckActive = True
        self.area.fill((190, 192, 194))
        self.text = pygame.font.Font(os.path.join("font","berlin.ttf"), 20).render("Are you sure you want to exit?", True, (94, 0, 9))
        self.area.blit(self.text, (self.area.get_width()/2 - (0.5 * self.text.get_width()), 5))
        self.exitbuttonyes = Button(self.area, pygame.Rect(self.area.get_width() / 2 - 100, self.area.get_height() / 2 - 60, 200, 30), "Yes", (94, 0, 9), (190, 192, 194))
        self.exitbuttonno = Button(self.area, pygame.Rect(self.area.get_width() / 2 - 100, self.area.get_height() / 2 - 20, 200, 30), "No", (94, 0, 9), (190, 192, 194))

    def get_width(self):
        return self._area.get_width()

    def get_height(self):
        return self._area.get_height()

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
