import pygame
from pygame.locals import *
import os
import sys


class Options(object):
    def __init__(self, screen, font_op):
        self.screen = screen
        self.font_op = font_op
        self.options_header = "Game Options"
        self.load_images()

    def load_images(self):
        self.img_menu_bg = pygame.image.load(os.path.join("img", "menu_bg4.png")).convert()
        self.img_icon_exit_x = pygame.image.load(os.path.join("img", "exit.png")).convert_alpha()

    def buttonClick(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        if mouseX > self.screen.get_width() - 156 \
                and mouseX < self.screen.get_width() - 96 \
                and mouseY > 57 and mouseY < 117:
            return False
from RadioButton import RadioGroup
from CheckBox import CheckBox


class Options(object):
    def __init__(self, screen, font_op, y_offset):
        self.screen = screen
        self.font_op = font_op
        self.y_offset = y_offset
        self.options_header = "Game Options"
        self.load_images()
        self.load_buttons()

    def load_buttons(self):
        # RADIO BUTTON GROUP
        self.resolution_radio_buttons = RadioGroup(self.screen)
        self.resolution_radio_buttons.newButton(self.screen.get_width() / 2 - 230, self.screen.get_height() / 2 - 140, 5)
        self.resolution_radio_buttons.newButton(self.screen.get_width() / 2 - 230, self.screen.get_height() / 2 - 120, 5)
        self.resolution_radio_buttons.newButton(self.screen.get_width() / 2 - 230, self.screen.get_height() / 2 - 100, 5)
        self.resolution_radio_buttons.newButton(self.screen.get_width() / 2 - 130, self.screen.get_height() / 2 - 140, 5)
        self.resolution_radio_buttons.newButton(self.screen.get_width() / 2 - 130, self.screen.get_height() / 2 - 120, 5)
        # CHECKBOXES
        self.checkbox_soundeffects = CheckBox(self.screen, self.screen.get_width() / 2 - 170, self.screen.get_height() / 2 - 27, 10)
        self.checkbox_music = CheckBox(self.screen, self.screen.get_width() / 2 + 30, self.screen.get_height()/2 - 27, 10)

    def load_images(self):
        self.img_menu_bg = pygame.image.load(os.path.join("img", "menu_bg4.png")).convert()

    def buttonClick(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        if mouseX > self.screen.get_width() - 310 \
                and mouseX < self.screen.get_width() - 180 \
                and mouseY > 73+self.y_offset and mouseY < 93+self.y_offset:
            return False

        #RADIO BUTTONS AND CHECKBOX
        self.resolution_radio_buttons.checkButton(mouseX, mouseY)
        self.checkbox_soundeffects.setChecked(mouseX, mouseY)
        self.checkbox_music.setChecked(mouseX, mouseY)
        return True

    def run(self):
        options_exit = False
        while not options_exit:
            # background image
            self.screen.blit(self.img_menu_bg, (0, 0))
            self.screen.blit(pygame.transform.scale(self.img_menu_bg,(self.screen.get_width(), int(self.screen.get_height()-(2*self.y_offset)))),(0,self.y_offset))
            # rectangle window w/ exit button
            self.text_exit_options = self.font_op(22, "berlin").render("Exit Options", True, (220, 146, 40))
            pygame.draw.rect(self.screen, (126, 51, 58), Rect((self.screen.get_width() / 2 - 300, self.screen.get_height()/2 - 200+self.y_offset), (600, 450+self.y_offset)))
            pygame.draw.rect(self.screen, (255, 255, 255), Rect((self.screen.get_width() - 310, 73+self.y_offset), (self.text_exit_options.get_width() + 5, 20)))
            self.screen.blit(self.text_exit_options, (self.screen.get_width() - 308, 70+self.y_offset))
            pygame.draw.rect(self.screen, (94, 0, 9), Rect((self.screen.get_width() / 2 - 300, self.screen.get_height()/2 - 200+self.y_offset), (600, 450+self.y_offset)), 5)

            # header
            header = self.font_op(50, "berlin").render(self.options_header, True, (255, 255, 255))
            self.screen.blit(header, (self.screen.get_width() / 2 - 0.5 * header.get_width(), 4+self.y_offset))
            # video options
            video_options = self.font_op(12, "berlin").render("Video options", True, (255, 255, 255))
            self.screen.blit(video_options, (self.screen.get_width() / 2 - 0.5 * video_options.get_width(), self.screen.get_height()/2 - 190+self.y_offset))
            screen_resolution = self.font_op(12, "berlin").render("Screen Resolution", True, (255, 255, 255))
            self.screen.blit(screen_resolution, (self.screen.get_width() / 2 - 200, self.screen.get_height() / 2 - 170 + self.y_offset))
            self.resoultion_text_1 = self.font_op(10, "berlin").render("960x540", True, (192, 192, 192))
            self.resoultion_text_2 = self.font_op(10, "berlin").render("1280x720", True, (192, 192, 192))
            self.resoultion_text_3 = self.font_op(10, "berlin").render("1600x900", True, (192, 192, 192))
            self.resoultion_text_4 = self.font_op(10, "berlin").render("1920x1080", True, (192, 192, 192))
            self.resoultion_text_5 = self.font_op(10, "berlin").render("960x720", True, (192, 192, 192))
            self.screen.blit(self.resoultion_text_1, (self.screen.get_width() / 2 - 220, self.screen.get_height() / 2 - 147 + self.y_offset))
            self.screen.blit(self.resoultion_text_2, (self.screen.get_width() / 2 - 220, self.screen.get_height() / 2 - 127 + self.y_offset))
            self.screen.blit(self.resoultion_text_3, (self.screen.get_width() / 2 - 220, self.screen.get_height() / 2 - 107 + self.y_offset))
            self.screen.blit(self.resoultion_text_4, (self.screen.get_width() / 2 - 120, self.screen.get_height() / 2 - 147 + self.y_offset))
            self.screen.blit(self.resoultion_text_5, (self.screen.get_width() / 2 - 120, self.screen.get_height() / 2 - 127 + self.y_offset))
            self.resolution_radio_buttons.draw()

            # audio option
            audio_options = self.font_op(12, "berlin").render("Audio options", True, (255, 255, 255))
            self.screen.blit(audio_options, (self.screen.get_width() / 2 - 0.5 * audio_options.get_width(), self.screen.get_height()/2 - 50 + self.y_offset))
            self.text_sound_effect_option = self.font_op(12, "berlin").render("Mute sound effects", True, (255, 255, 255))
            self.text_music_option = self.font_op(12, "berlin").render("Mute music", True, (255, 255, 255))
            self.screen.blit(self.text_sound_effect_option, (self.screen.get_width() / 2 - 150, self.screen.get_height()/2 - 30 + self.y_offset))
            self.screen.blit(self.text_music_option, (self.screen.get_width() / 2 + 50, self.screen.get_height()/2 - 30 + self.y_offset))
            self.checkbox_soundeffects.draw()
            self.checkbox_music.draw()

            # player option
            player_options = self.font_op(12, "berlin").render("Player options", True, (255, 255, 255))
            self.screen.blit(player_options, (self.screen.get_width() / 2 - 0.5 * player_options.get_width(), self.screen.get_height()/2 + 100 + self.y_offset))

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        options_exit = True
                        break
                elif event.type == MOUSEBUTTONDOWN:  # Perform action on click
                    if not self.buttonClick():
                        options_exit = True
                        break
                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
        return "start"
