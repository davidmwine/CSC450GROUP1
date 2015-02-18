import pygame
from pygame.locals import *
import os
import sys
from RadioButton import RadioGroup
from CheckBox import CheckBox
from startMenu import Start


class Options(object):
    def __init__(self, screen, infoScreen, font_op, y_offset):
        self.screen = screen
        self.infoScreen = infoScreen
        self.font_op = font_op
        self.y_offset = y_offset
        self.res_opt = 0
        self.soundeffectsOff = False
        self.musicOff = False
        self.load_images()
        self.load_buttons(self.res_opt, self.soundeffectsOff, self.musicOff)
        self.screen_modes = [(960, 540), (1280, 720), (1600, 900), (1920, 1080), (960, 720)]

    def load_buttons(self, res_opt, soundeffectsOn, musicOn):
        # RADIO BUTTON GROUP
        self.resolution_radio_buttons = RadioGroup(self.screen)
        self.resolution_radio_buttons.newButton(self.screen.get_width() / 2 - 80, self.screen.get_height() / 2 - 54 + self.y_offset, 5)
        self.resolution_radio_buttons.newButton(self.screen.get_width() / 2 - 80, self.screen.get_height() / 2 - 34 + self.y_offset, 5)
        self.resolution_radio_buttons.newButton(self.screen.get_width() / 2 - 80, self.screen.get_height() / 2 - 14 + self.y_offset, 5)
        self.resolution_radio_buttons.newButton(self.screen.get_width() / 2 + 20, self.screen.get_height() / 2 - 54 + self.y_offset, 5)
        #self.resolution_radio_buttons.newButton(self.screen.get_width() / 2 + 20, self.screen.get_height() / 2 - 34 + self.y_offset, 5) #4:3 not supported yet
        # CHECKBOXES
        self.checkbox_soundeffects = CheckBox(self.screen, self.screen.get_width() / 2 - 80, self.screen.get_height() / 2 + 58 + self.y_offset, 10)
        self.checkbox_music = CheckBox(self.screen, self.screen.get_width() / 2 - 80, self.screen.get_height()/2 + 78 + self.y_offset, 10)

        # FOR RELOADING BUTTONS
        # set the checked resolution box
        self.resolution_radio_buttons.setCurrent(res_opt)
        # if mute sound effects box should be checked check them, other wise leave unchecked
        if self.soundeffectsOff == True:
            if self.checkbox_soundeffects.getChecked() == False:
                self.checkbox_soundeffects.setChecked(self.screen.get_width() / 2 - 79, self.screen.get_height() / 2 + 59 + self.y_offset)
        else:
            if self.checkbox_soundeffects.getChecked() == True:
                self.checkbox_soundeffects.setChecked(self.screen.get_width() / 2 - 79, self.screen.get_height() / 2 + 59 + self.y_offset)
        # if mute music box should be checked check them, other wise leave unchecked
        if self.musicOff == True:
            if self.checkbox_music.getChecked() == False:
                self.checkbox_music.setChecked(self.screen.get_width() / 2 - 79, self.screen.get_height()/2 + 79 + self.y_offset)
        else:
            if self.checkbox_music.getChecked() == True:
                self.checkbox_music.setChecked(self.screen.get_width() / 2 - 79, self.screen.get_height()/2 + 79 + self.y_offset)


    def load_images(self):
        self.img_menu_bg = pygame.image.load(os.path.join("img", "menu_bg4.png")).convert()

    def buttonClick(self):
        mouseX, mouseY = pygame.mouse.get_pos()

        if mouseX > self.screen.get_width() / 2 + 178 \
                and mouseX < self.screen.get_width() / 2 + 198 \
                and mouseY > self.screen.get_height() / 2 - 123 + self.y_offset and mouseY < self.screen.get_height() / 2 - 103 + self.y_offset:
            return False

        if self.resolution_radio_buttons.checkButton(mouseX, mouseY):
            self.res_opt = self.resolution_radio_buttons.getCurrent()
            if self.infoScreen.current_h == self.screen_modes[self.resolution_radio_buttons.getCurrent()][1]\
               and self.infoScreen.current_w == self.screen_modes[self.resolution_radio_buttons.getCurrent()][0]:
                self.screen = pygame.display.set_mode(self.screen_modes[self.resolution_radio_buttons.getCurrent()], pygame.FULLSCREEN)
            else:
                self.screen = pygame.display.set_mode(self.screen_modes[self.resolution_radio_buttons.getCurrent()])

        self.checkbox_soundeffects.setChecked(mouseX, mouseY)
        self.soundeffectsOff = self.checkbox_soundeffects.getChecked()

        self.checkbox_music.setChecked(mouseX, mouseY)
        self.musicOff = self.checkbox_music.getChecked()
        if self.checkbox_music.getChecked() == True:
            pygame.mixer.Sound(os.path.join('sound','start_menu.wav')).stop()

        return True

    def run(self):
        options_exit = False
        while not options_exit:
            # background image
            self.screen.blit(self.img_menu_bg, (0, 0))
            self.screen.blit(pygame.transform.scale(self.img_menu_bg,(self.screen.get_width(), int(self.screen.get_height()-(2*self.y_offset)))),(0,self.y_offset))
            # rectangle window w/ exit button
            self.text_exit_options = self.font_op(22, "helvetica").render("X", True, (255, 0, 0))
            pygame.draw.rect(self.screen, (126, 51, 58), Rect((self.screen.get_width() / 2 - 200, self.screen.get_height() / 2 - 125 + self.y_offset), (400, 250 + self.y_offset)))
            pygame.draw.rect(self.screen, (255, 255, 255), Rect((self.screen.get_width() / 2 + 178, self.screen.get_height() / 2 - 123 + self.y_offset), (self.text_exit_options.get_width() + 6, 20)))
            self.screen.blit(self.text_exit_options, (self.screen.get_width() / 2 + 182, self.screen.get_height() / 2 - 127 + self.y_offset))
            pygame.draw.rect(self.screen, (94, 0, 9), Rect((self.screen.get_width() / 2 - 200, self.screen.get_height() / 2 - 125 + self.y_offset), (400, 250 + self.y_offset)), 2)
            # header
            header = self.font_op(50, "berlin").render("Game Options", True, (255, 255, 255))
            self.screen.blit(header, (self.screen.get_width() / 2 - 0.5 * header.get_width(), 4+self.y_offset))
            # video options
            video_options = self.font_op(20, "berlin").render("Video options", True, (255, 255, 255))
            self.screen.blit(video_options, (self.screen.get_width() / 2 - 0.5 * video_options.get_width(), self.screen.get_height() / 2 - 110 + self.y_offset))
            screen_resolution = self.font_op(12, "berlin").render("Screen Resolution", True, (255, 255, 255))
            self.screen.blit(screen_resolution, (self.screen.get_width() / 2 - 0.5 * screen_resolution.get_width(), self.screen.get_height() / 2 - 80 + self.y_offset))
            self.resoultion_text_1 = self.font_op(10, "berlin").render("960x540", True, (255, 255, 255))
            self.resoultion_text_2 = self.font_op(10, "berlin").render("1280x720", True, (255, 255, 255))
            self.resoultion_text_3 = self.font_op(10, "berlin").render("1600x900", True, (255, 255, 255))
            self.resoultion_text_4 = self.font_op(10, "berlin").render("1920x1080", True, (255, 255, 255))
            self.resoultion_text_5 = self.font_op(10, "berlin").render("960x720", True, (255, 255, 255))
            self.screen.blit(self.resoultion_text_1, (self.screen.get_width() / 2 - 70, self.screen.get_height() / 2 - 60 + self.y_offset))
            self.screen.blit(self.resoultion_text_2, (self.screen.get_width() / 2 - 70, self.screen.get_height() / 2 - 40 + self.y_offset))
            self.screen.blit(self.resoultion_text_3, (self.screen.get_width() / 2 - 70, self.screen.get_height() / 2 - 20 + self.y_offset))
            self.screen.blit(self.resoultion_text_4, (self.screen.get_width() / 2 + 30, self.screen.get_height() / 2 - 60 + self.y_offset))
            #self.screen.blit(self.resoultion_text_5, (self.screen.get_width() / 2 + 30, self.screen.get_height() / 2 - 40 + self.y_offset)) #4:3 not supported yet
            self.resolution_radio_buttons.draw()

            # audio option
            audio_options = self.font_op(20, "berlin").render("Audio options", True, (255, 255, 255))
            self.screen.blit(audio_options, (self.screen.get_width() / 2 - 0.5 * audio_options.get_width(), self.screen.get_height() / 2 + 30 + self.y_offset))
            self.text_sound_effect_option = self.font_op(12, "berlin").render("Mute sound effects", True, (255, 255, 255))
            self.text_music_option = self.font_op(12, "berlin").render("Mute music", True, (255, 255, 255))
            self.screen.blit(self.text_sound_effect_option, (self.screen.get_width() / 2 - 60, self.screen.get_height()/2 + 55 + self.y_offset))
            self.screen.blit(self.text_music_option, (self.screen.get_width() / 2 - 60, self.screen.get_height()/2 + 75 + self.y_offset))
            self.checkbox_soundeffects.draw()
            self.checkbox_music.draw()

            # player option
            # player_options = self.font_op(12, "berlin").render("Player options", True, (255, 255, 255))
            # self.screen.blit(player_options, (self.screen.get_width() / 2 - 0.5 * player_options.get_width(), self.screen.get_height()/2 + 100 + self.y_offset))

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
            self.load_buttons(self.res_opt, self.soundeffectsOff, self.musicOff)
            pygame.display.update()
        return "start"
