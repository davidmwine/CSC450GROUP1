import pygame
from pygame.locals import *
import os
import sys
import random

class Start(object):
    def __init__(self, screen, font_op, y_offset):
        self.screen = screen
        self.font_op = font_op
        self.y_offset = y_offset
        self.gameActive = 0  #Is the game running or not
        self.percentOfMax = self.screen.get_height()/1080
        #self.quitGame = False
        self.soundRunning = 0
        self.load_images()
        self.load_sounds()
        self.menuOn = True
        self.rulesOn = False
        self.optionsOn = False
        self.clock = pygame.time.Clock()
        self.extraPad = self.screen.get_height()/16

    def backToStart(self):
        self.rulesOn = False
        self.optionsOn = False
        self.menuOn = True

    def backToStart(self):
        self.rulesOn = False
        self.menuOn = True

    def backToStart(self):
        self.rulesOn = False
        self.menuOn = True

    def load_images(self):
        self.img_logo = pygame.image.load(os.path.join("img","logo.png")).convert_alpha()
        self.img_menu_bg = pygame.image.load(os.path.join("img","menu_bg4.png")).convert()
        self.img_icon_start = pygame.image.load(os.path.join("img","Dice2b.png")).convert_alpha()
        self.img_icon_resume = pygame.image.load(os.path.join("img","thumb_up2.png")).convert_alpha()
        self.img_icon_rules = pygame.image.load(os.path.join("img","book-brownb.png")).convert_alpha()
        self.img_icon_options = pygame.image.load(os.path.join("img","Gear_01b.png")).convert_alpha()
        self.img_icon_exit = pygame.image.load(os.path.join("img","Exitb.png")).convert_alpha() #Game exit

    def load_sounds(self): 
        self.sound_intro = pygame.mixer.Sound(os.path.join('sound','radio.wav'))
        self.sound_start_menu = pygame.mixer.Sound(os.path.join('sound','start_menu.wav'))

    def splash(self):           
        start_time = pygame.time.get_ticks()/1000.0
        text_color = [0,0,0]
        circle_coordinate = 200
        circle_thickness = 50
        circle_color = (94,0,9)
        circle_color_select = 1

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.leaveGame()
                    
            self.clock.tick(30)
            self.screen.fill((0,0,0))
            time = pygame.time.get_ticks()/1000. - start_time
            
            if time > 1 and time < 6:
                try:
                    pygame.draw.circle(self.screen, circle_color, (int(self.screen.get_width()/2), int(self.screen.get_height()/2) ), circle_coordinate, circle_thickness)
                except ValueError:
                    pass
                circle_thickness += 4
                
                if circle_coordinate >= self.screen.get_width():
                    circle_coordinate = 200
                    circle_thickness = 50
                    if circle_color_select == -1:
                        circle_color = (94,0,9)
                    else:
                        circle_color = (255,255,255)
                    circle_color_select = -circle_color_select
                else:
                    circle_coordinate += 15
                    
                for i in range(3):
                    if text_color[i] < 255:
                        text_color[i] += 1.3
                text_title = self.font_op(118,"berlin").render("Mastering MSU",True,text_color)
                #text_team1 = font_op(24,"helvetica").render("a Team 1 game",True,text_color)
             
                self.screen.blit(self.img_logo,(self.screen.get_width()/2-0.5*self.img_logo.get_width(),\
                                                (self.screen.get_height()/2)-self.img_logo.get_height()+self.y_offset))
                
                self.screen.blit(text_title,(self.screen.get_width()/2-0.5*text_title.get_width(),\
                                             (self.screen.get_height()/2)-0.5*self.img_logo.get_height()+self.y_offset+60))
                #self.screen.blit(text_team1,(self.screen.get_width()/2-0.5*text_team1.get_width(),\
                                             #(self.screen.get_height()/2)-0.5*self.img_logo.get_height()+self.y_offset+60))
            if time > 1 and self.soundRunning == 0:
                self.sound_intro.play()
                self.sound_intro.fadeout(6000)
                self.soundRunning = 1
            if time > 6.5:
                self.soundRunning = 0
                break
            
            pygame.display.update()
            #pygame.time.delay(60)

    def leaveGame(self):
        pygame.quit()
        sys.exit()

    def highlight(self):
        mouseX,mouseY = pygame.mouse.get_pos() 
        if mouseX > self.screen.get_width()/2-117\
           and mouseX < self.screen.get_width()/2-52+self.text_start.get_width()\
           and mouseY > (self.screen.get_height()/4+self.y_offset-5)+self.extraPad \
           and mouseY < (self.screen.get_height()/4+self.y_offset+self.text_start.get_height()+5)+self.extraPad:
            self.text_start = self.font_op(32,"berlin").render("Start Game",True,(255,255,255))
        elif self.gameActive == 1:
            self.text_start = self.font_op(32,"berlin").render("Start Game",True,(220,146,40))  
            if mouseX > self.screen.get_width()/2-117\
               and mouseX < self.screen.get_width()/2-52+self.text_resume.get_width()\
               and mouseY > (70+self.screen.get_height()/4+self.y_offset)+self.extraPad and \
               mouseY < (80+self.screen.get_height()/4+self.y_offset+self.text_resume.get_height())+self.extraPad:
                self.text_resume = self.font_op(32,"berlin").render("Resume Game",True,(255,255,255))
            else:
                self.text_resume = self.font_op(32,"berlin").render("Resume Game",True,(220,146,40))
        else:
            self.text_start = self.font_op(32,"berlin").render("Start Game",True,(220,146,40))    
        if mouseX > self.screen.get_width()/2-117\
           and mouseX < self.screen.get_width()/2-52+self.text_rules.get_width()\
           and mouseY > (70+self.screen.get_height()/4+self.y_offset+75*self.gameActive)+self.extraPad\
           and mouseY < (80+self.screen.get_height()/4+self.y_offset+self.text_rules.get_height()+75*self.gameActive)+self.extraPad:
            self.text_rules = self.font_op(32,"berlin").render("Rules",True,(255,255,255))
        else:
            self.text_rules = self.font_op(32,"berlin").render("Rules",True,(220,146,40))
        if mouseX > self.screen.get_width()/2-117\
           and mouseX < self.screen.get_width()/2-52+self.text_options.get_width()\
           and mouseY > (145+self.screen.get_height()/4+self.y_offset+75*self.gameActive)+self.extraPad\
           and mouseY < (155+self.screen.get_height()/4+self.y_offset+self.text_options.get_height()+75*self.gameActive)+self.extraPad:
            self.text_options = self.font_op(32,"berlin").render("Options",True,(255,255,255))
        else:
            self.text_options = self.font_op(32,"berlin").render("Options",True,(220,146,40))       
        if mouseX > self.screen.get_width()/2-117\
           and mouseX < self.screen.get_width()/2-52+self.text_exit.get_width()\
           and mouseY > (220+self.screen.get_height()/4+self.y_offset+75*self.gameActive)+self.extraPad\
           and mouseY < (230+self.screen.get_height()/4+self.y_offset+self.text_exit.get_height()+75*self.gameActive)+self.extraPad:
            self.text_exit = self.font_op(32,"berlin").render("Exit",True,(255,255,255))
        else:
            self.text_exit = self.font_op(32,"berlin").render("Exit",True,(220,146,40))

    def buttonClick(self):
        mouseX,mouseY = pygame.mouse.get_pos()
        #Rules
        if mouseX > self.screen.get_width()/2-117\
           and mouseX < self.screen.get_width()/2-52+self.text_rules.get_width()\
           and mouseY > (70+self.screen.get_height()/4+self.y_offset+75*self.gameActive)+self.extraPad\
           and mouseY < (80+self.screen.get_height()/4+self.y_offset+self.text_rules.get_height()+75*self.gameActive)+self.extraPad:
            self.menuOn = False
            self.rulesOn = True
        #Options
        if mouseX > self.screen.get_width()/2-117\
           and mouseX < self.screen.get_width()/2-52+self.text_options.get_width()\
           and mouseY > (145+self.screen.get_height()/4+self.y_offset+75*self.gameActive)+self.extraPad\
           and mouseY < (155+self.screen.get_height()/4+self.y_offset+self.text_options.get_height()+75*self.gameActive)+self.extraPad:
            self.menuOn = False
            self.optionsOn = True
        #Game
        #if mouseX > self.screen.get_width()/2-117\
        #   and mouseX < self.screen.get_width()/2-52+self.text_start.get_width()\
        #   and mouseY > (self.screen.get_height()/4+self.y_offset-5)+self.extraPad \
        #   and mouseY < (self.screen.get_height()/4+self.y_offset+self.text_start.get_height()+5)+self.extraPad:
        #    self.menuOn = False
        #    self.gameOn = True
        #Exit
        if mouseX > self.screen.get_width()/2-117\
           and mouseX < self.screen.get_width()/2-52+self.text_exit.get_width()\
           and mouseY > (220+self.screen.get_height()/4+self.y_offset+75*self.gameActive)+self.extraPad\
           and mouseY < (230+self.screen.get_height()/4+self.y_offset+self.text_exit.get_height()+75*self.gameActive)+self.extraPad:
            self.leaveGame()
        

    def imageDisplay(self):
        self.screen.fill((0,0,0))
        self.screen.blit(pygame.transform.scale(self.img_menu_bg,(self.screen.get_width(),\
                        int(self.screen.get_height()-(2*self.y_offset)))),(0,self.y_offset))
        
        self.screen.blit(self.text_header_bg,(self.screen.get_width()/2-3-0.5*self.text_header_bg.get_width()+4,(4+self.screen.get_height()/30+self.y_offset)+self.extraPad))
        self.screen.blit(self.text_header,(self.screen.get_width()/2-3-0.5*self.text_header.get_width(),(self.screen.get_height()/30+self.y_offset)+self.extraPad))

        self.screen.blit(self.text_start_bg,(self.screen.get_width()/2-55,(2+self.screen.get_height()/4+self.y_offset)+self.extraPad))
        self.screen.blit(self.text_start,(self.screen.get_width()/2-57,(self.screen.get_height()/4+self.y_offset)+self.extraPad)) 
        self.screen.blit(self.text_rules_bg,(self.screen.get_width()/2-55,(77+self.screen.get_height()/4+self.y_offset+75*self.gameActive)+self.extraPad))
        self.screen.blit(self.text_rules,(self.screen.get_width()/2-57,(75+self.screen.get_height()/4+self.y_offset+75*self.gameActive)+self.extraPad))
        self.screen.blit(self.text_options_bg,(self.screen.get_width()/2-55,(152+self.screen.get_height()/4+self.y_offset+75*self.gameActive)+self.extraPad))
        self.screen.blit(self.text_options,(self.screen.get_width()/2-57,(150+self.screen.get_height()/4+self.y_offset+75*self.gameActive)+self.extraPad))
        self.screen.blit(self.text_exit_bg,(self.screen.get_width()/2-55,(227+self.screen.get_height()/4+self.y_offset+75*self.gameActive)+self.extraPad))
        self.screen.blit(self.text_exit,(self.screen.get_width()/2-57,(225+self.screen.get_height()/4+self.y_offset+75*self.gameActive)+self.extraPad))

        self.screen.blit(self.img_icon_start,(self.screen.get_width()/2-112,(self.screen.get_height()/4+self.y_offset-5)+self.extraPad))
        self.screen.blit(self.img_icon_rules,(self.screen.get_width()/2-112,(70+self.screen.get_height()/4+self.y_offset+75*self.gameActive)+self.extraPad))
        self.screen.blit(self.img_icon_options,(self.screen.get_width()/2-112,(145+self.screen.get_height()/4+self.y_offset+75*self.gameActive)+self.extraPad))
        self.screen.blit(self.img_icon_exit,(self.screen.get_width()/2-112,(220+self.screen.get_height()/4+self.y_offset+75*self.gameActive)+self.extraPad))

    def menu(self):
        self.text_header = self.font_op(90,"berlin").render("Mastering MSU",True,(255,255,255))
        self.text_header_bg = self.font_op(90,"berlin").render("Mastering MSU",True,(0,0,0))
        self.text_start = self.font_op(32,"berlin").render("Start Game",True,(220,146,40))
        self.text_start_bg = self.font_op(32,"berlin").render("Start Game",True,(0,0,0))
        self.text_resume = self.font_op(32,"berlin").render("Resume Game",True,(220,146,40))
        self.text_resume_bg = self.font_op(32,"berlin").render("Resume Game",True,(0,0,0))
        self.text_rules = self.font_op(32,"berlin").render("Rules",True,(220,146,40))
        self.text_rules_bg = self.font_op(32,"berlin").render("Rules",True,(0,0,0))
        self.text_options = self.font_op(32,"berlin").render("Options",True,(220,146,40))
        self.text_options_bg = self.font_op(32,"berlin").render("Options",True,(0,0,0))
        self.text_exit = self.font_op(32,"berlin").render("Exit",True,(220,146,40))
        self.text_exit_bg = self.font_op(32,"berlin").render("Exit",True,(0,0,0))

        #menu = True
        #rulesActive = False

        while self.menuOn:
            self.clock.tick(30)
            #self.screen.fill((240,240,240))

            if self.soundRunning == 0:
                self.sound_start_menu.play(-1) 
                self.soundRunning = 1

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.leaveGame()
                #if event.type == KEYDOWN:
                    #if event.key == K_ESCAPE:
                        #if rulesActive == True:
                            #rulesActive = False
                        #if self.gameActive == 1:
                            #menu = False
                            
                if event.type == MOUSEMOTION:  #Highlight text on hover
                    self.highlight()
                        
                if event.type == MOUSEBUTTONDOWN:  #Perform action on click
                    self.buttonClick()
            self.imageDisplay()

            if self.gameActive == 1:
                self.screen.blit(self.text_resume_bg,(self.screen.get_width()/2-55,(77+self.screen.get_height()/4+self.y_offset)+self.extraPad))
                self.screen.blit(self.text_resume,(self.screen.get_width()/2-57,(75+self.screen.get_height()/4+self.y_offset)+self.extraPad))
                self.screen.blit(self.img_icon_resume,(self.screen.get_width()/2-112,(70+self.screen.get_height()/4+self.y_offset)+self.extraPad))
            
            pygame.display.update()
        if self.rulesOn:
            return "rules"
        if self.optionsOn:
            return "options"
        if self.gameOn:
            return "game"
