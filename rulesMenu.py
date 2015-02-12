import pygame
from pygame.locals import *
import os
import sys

class Rules(object):
    def __init__(self, screen, font_op):
        self.screen = screen
        self.font_op = font_op
        self.load_images()
        self.rules_count = 3  #Number of rules/rule pages

    def load_images(self):     
        self.img_arrow = pygame.image.load(os.path.join("img","arrow.png")).convert_alpha()
        self.img_arrow_left = pygame.image.load(os.path.join("img","arrowLeft.png")).convert_alpha()
        self.img_menu_bg = pygame.image.load(os.path.join("img","menu_bg4.png")).convert()
        self.img_icon_exit_x = pygame.image.load(os.path.join("img","exit.png")).convert_alpha() #Rules exit
        

    def buttonClick(self):
        mouseX,mouseY = pygame.mouse.get_pos() 
        if mouseX > self.screen.get_width()-156\
           and mouseX < self.screen.get_width()-96\
           and mouseY > 57 and mouseY < 117:
            return False 
        if self.rules_page > 1:
            if mouseX > self.screen.get_width()/2-310\
               and mouseX < self.screen.get_width()/2-254\
               and mouseY > 385 and mouseY < 428:
                self.rules_next_page(-1)
                return True
        if self.rules_page < self.rules_count:
            if mouseX > self.screen.get_width()/2+245\
               and mouseX < self.screen.get_width()/2+320\
               and mouseY > 385 and mouseY < 428:
                self.rules_next_page(1)
                return True
        return True

    def run(self):
        self.rules_next_page()
        rules_exit = False
        while not rules_exit:
            self.screen.blit(self.img_menu_bg, (0, 0))
            pygame.draw.rect(self.screen,(255,255,255),Rect((self.screen.get_width()/2-300,75),(600,350)))
            self.screen.blit(self.img_rules,(0,450))
            pygame.draw.rect(self.screen,(0,0,0),Rect((self.screen.get_width()/2-300,75),(600,350)),1)
            self.screen.blit(self.img_icon_exit_x,(self.screen.get_width()- 151,62))
            if self.rules_page < self.rules_count:
                self.screen.blit(self.img_arrow,(self.screen.get_width()/2+250,390))
            if self.rules_page > 1:
                self.screen.blit(self.img_arrow_left,(self.screen.get_width()/2-315,390))

            #Page number display
            self.screen.blit(self.font_op(22,"helvetica").render(str(self.rules_page)+"/"+str(self.rules_count),True,(68,201,20)),(self.screen.get_width()/2-294,77))

            header = self.font_op(50,"berlin").render(self.rules_header,True,(255,255,255))
            self.screen.blit(header,(self.screen.get_width()/2-0.5*header.get_width(),4))
            for text in range(len(self.rules_words)): #Display rules on a page 
                textOut = self.font_op(20,"helvetica").render(self.rules_words[text],True,(0,0,0))
                self.screen.blit(textOut,(self.screen.get_width()/2-240,130+text*25))
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        rules_exit = True
                        break
                elif event.type == MOUSEBUTTONDOWN:  #Perform action on click
                    if not self.buttonClick():
                        rules_exit = True
                        break
            pygame.display.update()
        return "start"

    def rules_next_page(self, pageNum=None):
        if pageNum == None:
            self.rules_page = 1
        else:
            self.rules_page += pageNum
        self.img_rules = pygame.Surface((800,150)).convert()
        bottom_image = "rulesBottom1.png"

        if self.rules_page == 1:
            self.rules_header = "Rules Intro Header"
            self.rules_words = ["Here are some rules for you to look at. Wow",
                                "look at all of this great stuff on this line.",
                                "Here's some more info. RRRRrrrrrrrrrrrrrrrrrr",
                                "rrrrrrrrrr."]
        if self.rules_page == 2:
            bottom_image = "rulesBottom2.png"
            self.rules_header = "General Rules"
            self.rules_words = ["Here are some rules for you to look at and",
                                "stuff. Here's some more info."]
        if self.rules_page == 3:
            bottom_image = "rulesBottom3.png"
            self.rules_header = "More Rules"
            self.rules_words = ["Here are some rules for you to look at and",
                                "stuff. Here's some more info."]   
        self.img_rules.blit(pygame.image.load(os.path.join("img",bottom_image)), (50, 0), Rect((0,0),(750,150)))  
