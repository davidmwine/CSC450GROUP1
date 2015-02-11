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