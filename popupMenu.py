import pygame
import sys
import os
from Controls import Button
from RadioButton import RadioGroup


class popupMenu(object):
    def __init__(self, parent):
        self.displayInfo = pygame.display.Info()
        self.clock = pygame.time.Clock()
        self._parent = parent
        self._width = self._parent.get_width() / 2
        self._height = self._parent.get_height() / 2
        self._area = parent.subsurface((self._parent.get_width() / 4), (self._parent.get_height() / 4), self._width, self._height)
        self.screen_modes = [(960, 540), (1280, 720), (1600, 900), (1920, 1080), (960, 720)]
        self.res_opt = self.screen_modes.index((self.displayInfo.current_w, self.displayInfo.current_h)) # current resolution option
        self.popupActive = False
        self.optionActive = False
        self.exitCheckActive = False

    def load_buttons(self):
        # RADIO BUTTON GROUP
        self.resolution_radio_buttons = RadioGroup(self._area)
        self.resolution_radio_buttons.newButton(self._area.get_width() / 2 - 80, self._area.get_height() / 2 + 5, 5)
        self.resolution_radio_buttons.newButton(self._area.get_width() / 2 - 80, self._area.get_height() / 2 + 25, 5)
        self.resolution_radio_buttons.newButton(self._area.get_width() / 2 - 80, self._area.get_height() / 2 + 45, 5)
        self.resolution_radio_buttons.newButton(self._area.get_width() / 2 + 20, self._area.get_height() / 2 + 5, 5)
        #self.resolution_radio_buttons.newButton(self._area.get_width() / 2 + 20, self._area.get_height() / 2 + 25, 5) #4:3 not supported yet
        self.resolution_radio_buttons.setCurrent(self.res_opt)

    def change_resolution(self, X, Y):
        # supposed to check radio button and return whichever resolution was selected
        if self.resolution_radio_buttons.checkButton(X, Y):
            self.res_opt = self.resolution_radio_buttons.getCurrent()
            return self.screen_modes[self.resolution_radio_buttons.getCurrent()]
        else:
            return None

    def make_popup_menu(self):
        self.popupActive = True
        self.optionActive = False
        self.exitCheckActive = False
        self._area.fill((190, 192, 194))
        self.text_options = pygame.font.Font(os.path.join("font","berlin.ttf"), 30).render("Options", True, (94, 0, 9))
        self._area.blit(self.text_options, (self._area.get_width()/2 - (0.5 * self.text_options.get_width()), 5))
        self.resume_button = Button(self._area, pygame.Rect(self._area.get_width() / 2 - 100, self._area.get_height() / 2 - 80, 200, 30), "Resume Game", (94, 0, 9), (190, 192, 194))
        self.save_button = Button(self._area, pygame.Rect(self._area.get_width() / 2 - 100, self._area.get_height() / 2 - 40, 200, 30), "Save Game", (94, 0, 9), (190, 192, 194))
        self.gameoptions_button = Button(self._area, pygame.Rect(self._area.get_width() / 2 - 100, self._area.get_height() / 2, 200, 30), "Game Options", (94, 0, 9), (190, 192, 194))
        self.exit_button = Button(self._area, pygame.Rect(self._area.get_width() / 2 - 100, self._area.get_height() / 2 + 40, 200, 30), "Exit Game", (94, 0, 9), (190, 192, 194))

    def game_options(self):
        self.popupActive = True
        self.optionActive = True
        self.exitCheckActive = False
        self._area.fill((190, 192, 194))
        # header
        self.text_options = pygame.font.Font(os.path.join("font","berlin.ttf"), 30).render("Game Options", True, (94, 0, 9))
        self._area.blit(self.text_options, (self._area.get_width()/2 - (0.5 * self.text_options.get_width()), 5))

        # back button
        self.exit_button = Button(self._area, pygame.Rect(self._area.get_width() / 2 - 100, self._area.get_height() / 2 - 80, 200, 30), "Back", (94, 0, 9), (190, 192, 194))

        # resolution options
        self.load_buttons()
        self.text_resolution = pygame.font.Font(os.path.join("font","berlin.ttf"), 20).render("Resolution Options", True, (94, 0, 9))
        self._area.blit(self.text_resolution, (self._area.get_width() / 2 - (0.5 * self.text_resolution.get_width()), self._area.get_height() / 2 - 30))
        self.resoultion_text_1 = pygame.font.Font(os.path.join("font", "berlin.ttf"), 10).render("960x540", True, (0, 0, 0))
        self.resoultion_text_2 = pygame.font.Font(os.path.join("font", "berlin.ttf"), 10).render("1280x720", True, (0, 0, 0))
        self.resoultion_text_3 = pygame.font.Font(os.path.join("font", "berlin.ttf"), 10).render("1600x900", True, (0, 0, 0))
        self.resoultion_text_4 = pygame.font.Font(os.path.join("font", "berlin.ttf"), 10).render("1920x1080", True, (0, 0, 0))
        # self.resoultion_text_5 = pygame.font.Font(os.path.join("font", "berlin.ttf"), 10).render("960x720", True, (0, 0, 0))
        self._area.blit(self.resoultion_text_1, (self._area.get_width() / 2 - 70, self._area.get_height() / 2))
        self._area.blit(self.resoultion_text_2, (self._area.get_width() / 2 - 70, self._area.get_height() / 2 + 20))
        self._area.blit(self.resoultion_text_3, (self._area.get_width() / 2 - 70, self._area.get_height() / 2 + 40))
        self._area.blit(self.resoultion_text_4, (self._area.get_width() / 2 + 30, self._area.get_height() / 2))
        #self._area.blit(self.resoultion_text_5, (self._area.get_width() / 2 + 30, self._area.get_height() / 2 + 20)) #4:3 not supported yet
        self.resolution_radio_buttons.draw()

    def exit_check(self):
        self.popupActive = True
        self.optionActive = False
        self.exitCheckActive = True
        self._area.fill((190, 192, 194))
        self.text = pygame.font.Font(os.path.join("font","berlin.ttf"), 20).render("Are you sure you want to exit?", True, (94, 0, 9))
        self._area.blit(self.text, (self._area.get_width()/2 - (0.5 * self.text.get_width()), 5))
        self.exit_button_yes = Button(self._area, pygame.Rect(self._area.get_width() / 2 - 100, self._area.get_height() / 2 - 60, 200, 30), "Yes", (94, 0, 9), (190, 192, 194))
        self.exit_button_no = Button(self._area, pygame.Rect(self._area.get_width() / 2 - 100, self._area.get_height() / 2 - 20, 200, 30), "No", (94, 0, 9), (190, 192, 194))

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
