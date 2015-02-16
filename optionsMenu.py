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
        #EXAMPLE RADIO BUTTON GROUP
        self.r1 = RadioGroup(self.screen)
        self.r1.newButton(self.screen.get_width()/2, self.screen.get_height()/2, 10)
        self.r1.newButton(self.screen.get_width()/2, self.screen.get_height()/2 + 30, 10)
        self.r1.newButton(self.screen.get_width()/2, self.screen.get_height()/2 + 60, 10)
        #EXAMPLE CHECKBOXES
        self.c1 = CheckBox(self.screen, self.screen.get_width()/4, self.screen.get_height()/2, 10)
        self.c2 = CheckBox(self.screen, self.screen.get_width()/4, self.screen.get_height()/2 + 30, 10)
        self.c3 = CheckBox(self.screen, self.screen.get_width()/4, self.screen.get_height()/2 + 60, 10)

    def load_images(self):
        self.img_menu_bg = pygame.image.load(os.path.join("img", "menu_bg4.png")).convert()
        #self.img_icon_exit_x = pygame.image.load(os.path.join("img", "exit.png")).convert_alpha()

    def buttonClick(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        if mouseX > self.screen.get_width() - 153 \
                and mouseX < self.screen.get_width() - 28 \
                and mouseY > 57+self.y_offset and mouseY < 117+self.y_offset:
            return False

        #RADIO BUTTONS AND CHECKBOX EXAMPLE
        self.r1.checkButton(mouseX, mouseY)
        self.c1.setChecked(mouseX, mouseY)
        self.c2.setChecked(mouseX, mouseY)
        self.c3.setChecked(mouseX, mouseY)
        return True

    def run(self):
        options_exit = False
        while not options_exit:
            # background image
            self.screen.blit(self.img_menu_bg, (0, 0))
            # rectangle window w/ exit button
            pygame.draw.rect(self.screen, (126, 51, 58), Rect((self.screen.get_width() / 2 - 300, 75), (600, 450)))
            pygame.draw.rect(self.screen, (255, 255, 255), Rect((self.screen.get_width() - 150, 78), (48, 20)))
            self.screen.blit(self.img_icon_exit_x, (self.screen.get_width() - 151, 62))
            pygame.draw.rect(self.screen, (94, 0, 9), Rect((self.screen.get_width() / 2 - 300, 75), (600, 450)), 5)
            # header
            header = self.font_op(50, "berlin").render(self.options_header, True, (255, 255, 255))
            self.screen.blit(header, (self.screen.get_width() / 2 - 0.5 * header.get_width(), 4))
            # video options
            video_options = self.font_op(12, "berlin").render("Video options", True, (255, 255, 255))
            self.screen.blit(video_options, (self.screen.get_width() / 2 - 0.5 * video_options.get_width(), 85))

            # audio option
            audio_options = self.font_op(12, "berlin").render("Audio options", True, (255, 255, 255))
            self.screen.blit(audio_options, (self.screen.get_width() / 2 - 0.5 * audio_options.get_width(), 225))

            # player option
            player_options = self.font_op(12, "berlin").render("Player options", True, (255, 255, 255))
            self.screen.blit(player_options, (self.screen.get_width() / 2 - 0.5 * player_options.get_width(), 375))

            self.screen.blit(pygame.transform.scale(self.img_menu_bg,(self.screen.get_width(),\
                            int(self.screen.get_height()-(2*self.y_offset)))),(0,self.y_offset))
            # rectangle window w/ exit button
            pygame.draw.rect(self.screen, (126, 51, 58), Rect((self.screen.get_width() / 2 - 300, self.screen.get_height()/2 - 200+self.y_offset), (600, 450+self.y_offset)))
            pygame.draw.rect(self.screen, (255, 255, 255), Rect((self.screen.get_width() - 153, 78+self.y_offset), (125, 20)))
            #self.screen.blit(self.img_icon_exit_x, (self.screen.get_width() - 151, 62))
            self.text_exit_options = self.font_op(22,"berlin").render("Exit Options",True,(220,146,40))
            #self.screen.blit(self.text_exit_options,(self.screen.get_width()/2+198,self.screen.get_height()/8+self.y_offset))
            self.screen.blit(self.text_exit_options,(self.screen.get_width() - 151, 75+self.y_offset))
            pygame.draw.rect(self.screen, (94, 0, 9), Rect((self.screen.get_width() / 2 - 300, self.screen.get_height()/2 - 200+self.y_offset), (600, 450+self.y_offset)), 5)
            # header
            header = self.font_op(50, "berlin").render(self.options_header, True, (255, 255, 255))
            self.screen.blit(header, (self.screen.get_width() / 2 - 0.5 * header.get_width(), 4+self.y_offset))
            # video options
            video_options = self.font_op(12, "berlin").render("Video options", True, (255, 255, 255))
            self.screen.blit(video_options, (self.screen.get_width() / 2 - 0.5 * video_options.get_width(), self.screen.get_height()/2 - 190+self.y_offset))

            # audio option
            audio_options = self.font_op(12, "berlin").render("Audio options", True, (255, 255, 255))
            self.screen.blit(audio_options, (self.screen.get_width() / 2 - 0.5 * audio_options.get_width(), self.screen.get_height()/2 - 50 + self.y_offset))

            # player option
            player_options = self.font_op(12, "berlin").render("Player options", True, (255, 255, 255))
            self.screen.blit(player_options, (self.screen.get_width() / 2 - 0.5 * player_options.get_width(), self.screen.get_height()/2 + 100 + self.y_offset))

            #EXAMPLE DRAWING OF RADIO BUTTONS
            self.r1.draw()

            #EXAMPLE DRAWING OF CHECKBOXES
            self.c1.draw()
            self.c2.draw()
            self.c3.draw()

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        options_exit = True
                        break
                elif event.type == MOUSEBUTTONDOWN:  # Perform action on click
                    if not self.buttonClick():
                        options_exit = True
                        break
            pygame.display.update()
        return "start"
                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
        return "start"
