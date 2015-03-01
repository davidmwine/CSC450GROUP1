import pygame
import sys
import os
from Controls import Button
from RadioButton import RadioGroup



class popupMenu(object):
    def __init__(self, parent):
        self.clock = pygame.time.Clock()
        self._parent = parent
        self._width = self._parent.get_width() / 2
        self._height = self._parent.get_height() / 2
        self._area = parent.subsurface((self._parent.get_width() / 4), (self._parent.get_height() / 4), self._width, self._height)

    def load_buttons(self):
        # RADIO BUTTON GROUP
        self.resolution_radio_buttons = RadioGroup(self._area)
        self.resolution_radio_buttons.newButton(self._area.get_width() / 2 - 80, self._area.get_height() / 2 - 54, 5)
        self.resolution_radio_buttons.newButton(self._area.get_width() / 2 - 80, self._area.get_height() / 2 - 34, 5)
        self.resolution_radio_buttons.newButton(self._area.get_width() / 2 - 80, self._area.get_height() / 2 - 14, 5)
        self.resolution_radio_buttons.newButton(self._area.get_width() / 2 + 20, self._area.get_height() / 2 - 54, 5)
        #self.resolution_radio_buttons.newButton(self._area.get_width() / 2 + 20, self._area.get_height() / 2 - 34, 5) #4:3 not supported yet

    def make_popup_menu(self):
        self._area.fill((190, 192, 194))
        self.text_options = pygame.font.Font(os.path.join("font","berlin.ttf"), 30).render("Options", True, (94, 0, 9))
        self._area.blit(self.text_options, (self._area.get_width()/2 - (0.5 * self.text_options.get_width()), 5))
        self.resume_button = Button(self._area, pygame.Rect(self._area.get_width() / 2 - 100, self._area.get_height() / 2 - 80, 200, 30), "Resume Game", (94, 0, 9), (190, 192, 194))
        self.save_button = Button(self._area, pygame.Rect(self._area.get_width() / 2 - 100, self._area.get_height() / 2 - 40, 200, 30), "Save Game", (94, 0, 9), (190, 192, 194))
        self.gameoptions_button = Button(self._area, pygame.Rect(self._area.get_width() / 2 - 100, self._area.get_height() / 2, 200, 30), "Video Options", (94, 0, 9), (190, 192, 194))
        self.exit_button = Button(self._area, pygame.Rect(self._area.get_width() / 2 - 100, self._area.get_height() / 2 + 40, 200, 30), "Exit Game", (94, 0, 9), (190, 192, 194))

    def video_options(self):
        self._area.fill((190, 192, 194))
        self.load_buttons()
        self.resolution_radio_buttons.draw()

    def get_width(self):
        return self._area.get_width()

    def get_height(self):
        return self._area.get_height()
