import pygame, sys, os
from pygame.locals import *
from player import Player
from globals import Globals
from ChatBox import chatBox
from RadioButton import RadioGroup
from textWrap import *


class Lobby():

    def __init__(self, font_op ,parent ,scale = 1):
        
        self.width = int(scale*1920)
        self.height = int(scale*1080)
        self.font_op = font_op
        self.scale = scale
        self.parent = parent
        self.screen = pygame.Surface((self.width, self.height))
        self.game_type = [self.hostDraw,self.lfgDraw, self.localGameDraw]
        self.game_opt = 0


    def load(self, game_opt):
        self.bg = pygame.image.load(os.path.join("img","menu_bg4.png"))
        self.text_list = []
        self.text_list.append(self.font_op(20, 'berlin').render("Host a game.", 1, (0,0,0)))
        self.text_list.append(self.font_op(20, 'berlin').render("Join a game.",1,(0,0,0)))
        self.text_list.append(self.font_op(20, 'berlin').render("Start a local game.",1,(0,0,0)))
        self.width_list = [i.get_width() for i in self.text_list] #for bliting in loop
        self.width_less_radio = self.width - sum(self.width_list)
        
        self.game_type_radio = RadioGroup(self.screen)
        
        self.game_type_radio.newButton(self.width_less_radio/2, self.height/8+15, 5)
        self.game_type_radio.newButton(self.width_less_radio/2+ self.width_list[0] +32, self.height/8+15, 5)
        self.game_type_radio.newButton(self.width_less_radio/2+ sum(self.width_list[:2]) +50, self.height/8+15, 5)
        self.game_type_radio.setCurrent(game_opt)



    def buttonClick(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        if self.game_type_radio.checkButton(mouseX, mouseY):
            self.game_opt = self.game_type_radio.getCurrent()
            
    def alwaysDraw(self):
        
        self.screen.blit(self.bg, (0,0))
        for i in range(len(self.text_list)):
            self.screen.blit(self.text_list[i], (self.width_less_radio/2 +20*(i+1) + sum(self.width_list[:i]),
                                                 self.height/8,self.width_list[i],self.text_list[i].get_height()))
        self.game_type_radio.draw()
        
        


    def hostDraw(self):
        self.host_screen = self.screen.subsurface(self.width/10, self.height/3,self.width*8/10, self.height/3)
        self.host_screen.fill((255,255,255))
        text1 = self.font_op(20, 'berlin').render("Please select game attributes.",1,(0,0,0))
        #playersnumber
        text_rect = (((self.host_screen.get_width() - text1.get_width())/2, self.host_screen.get_height()/10))
        self.host_screen.blit(text1, text_rect)
        
        
                             
                            


    def lfgDraw(self):
        self.lfg_screen = self.screen.subsurface(self.width/10, self.height/3,self.width*2/3, self.height*2/3-self.height/10)
        self.lfg_screen.fill((255,255,255))
        text1 = self.font_op(20, 'berlin').render("Please select a game to join.",1,(0,0,0))
        text_rect = (((self.lfg_screen.get_width() - text1.get_width())/2, self.host_screen.get_height()/10))
        self.lfg_screen.blit(text1, text_rect)


    def localGameDraw(self):
        self.local_screen = self.screen.subsurface(self.width/10, self.height/3,self.width*8/10, self.height/3)
        self.local_screen.fill((255,255,255))
        text1 = self.font_op(20, 'berlin').render("Please select game attributes.",1,(0,0,0))
        text_rect = (((self.local_screen.get_width() - text1.get_width())/2, self.host_screen.get_height()/10))
        self.local_screen.blit(text1, text_rect)


    
    def run(self):
        self.load(0)
        self.gameExit = False
        while not self.gameExit:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    self.buttonClick()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                        break
            self.alwaysDraw()
            self.game_type[self.game_opt]()
            self.parent.blit(self.screen, (0,0))
            pygame.display.update()
            
            

        

    
