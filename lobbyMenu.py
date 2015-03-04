import pygame
from pygame.locals import *
import os
import sys
from GameArea import GameArea
from player import Player
from playersDisplay import PlayersDisplay

class Lobby(object):
    def __init__(self, screen, font_op, y_offset, ratio):
        self.screen = screen
        self.font_op = font_op
        self.y_offset = y_offset
        self.load_images()
        self.game_start = False
        self.ratio = ratio

    def load_images(self):     
        self.img_menu_bg = pygame.image.load(os.path.join("img","menu_bg4.png")).convert()
        

    def buttonClick(self):
        mouseX,mouseY = pygame.mouse.get_pos()
        #Game start
        if mouseX > self.screen.get_width()/2-310\
            and mouseX < self.screen.get_width()/2-190\
            and mouseY > self.y_offset+5.8*self.screen.get_height()/7 and mouseY < self.y_offset+5.8*self.screen.get_height()/7+30:
            self.game_start = True
            return True
        #Exit lobby
        if mouseX > self.screen.get_width()/2+194\
            and mouseX < self.screen.get_width()/2+295\
            and mouseY > self.screen.get_height()/1.2+self.y_offset-5 and mouseY < self.screen.get_height()/1.2+self.y_offset+self.text_exit_lobby.get_height()+5:
            return False
        return True

    def run(self):
        self.rules_header = "Lobby"
        lobby_exit = False
        self.text_exit_lobby = self.font_op(22,"berlin").render("Exit Lobby",True,(220,146,40))
        self.text_game_start = self.font_op(22,"berlin").render("Game Start",True,(220,146,40))
        p1 = Player("player1", "Agriculture")
        p2 = Player("player2", "Arts and Letters")
        p3 = Player("player3", "Natural and Applied Sciences")
        p4 = Player("player4", "Education")
        p5 = Player("player5", "Health and Human Services")
        p6 = Player("player6", "Humanities and Public Affairs")
        players = [p1, p2, p3, p4, p5, p6]
        #self.text_exit_rules_bg = self.font_op(22,"berlin").render("Exit Rules",True,(75,75,75))
        while not lobby_exit:
            self.screen.blit(pygame.transform.scale(self.img_menu_bg,(self.screen.get_width(),\
                            int(self.screen.get_height()-(2*self.y_offset)))),(0,self.y_offset))
            #Draw Rects for 6 player 
            pygame.draw.rect(self.screen,(255,255,255),Rect((self.screen.get_width()/2-300,self.screen.get_height()/8),\
                                                            (290,20+self.screen.get_height()/8)))
            pygame.draw.rect(self.screen,(255,255,255),Rect((self.screen.get_width()/2-300,2*self.screen.get_height()/8+50),\
                                                            (290,20+self.screen.get_height()/8)))
            pygame.draw.rect(self.screen,(255,255,255),Rect((self.screen.get_width()/2-300,3*self.screen.get_height()/8+100),\
                                                            (290,20+self.screen.get_height()/8)))
            pygame.draw.rect(self.screen,(255,255,255),Rect((self.screen.get_width()/2+10,self.screen.get_height()/8),\
                                                            (290,20+self.screen.get_height()/8)))
            pygame.draw.rect(self.screen,(255,255,255),Rect((self.screen.get_width()/2+10,2*self.screen.get_height()/8+50),\
                                                            (290,20+self.screen.get_height()/8)))
            pygame.draw.rect(self.screen,(255,255,255),Rect((self.screen.get_width()/2+10,3*self.screen.get_height()/8+100),\
                                                            (290,20+self.screen.get_height()/8)))

            self.screen.blit(self.text_game_start,(self.screen.get_width()/2-300,self.screen.get_height()/1.2+self.y_offset))
            self.screen.blit(self.text_exit_lobby,(self.screen.get_width()/2+198,self.screen.get_height()/1.2+self.y_offset))
            
            header = self.font_op(50,"berlin").render(self.rules_header,True,(255,255,255))
            self.screen.blit(header,(self.screen.get_width()/2-0.5*header.get_width(),self.screen.get_height()/50+self.y_offset))
            
            #Can delete this line, placeholder# self.screen.blit(header,(self.screen.get_width()/2-0.5*header.get_width(),5*self.screen.get_height()/6+self.y_offset)) 
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        lobby_exit = True
                        break
                elif event.type == MOUSEBUTTONUP:  #Perform action on click
                    if not self.buttonClick():
                        lobby_exit = True
                        break
                    if self.game_start and self.buttonClick():
                        lobby_exit = True
                        break
                    
                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
            pygame.display.update()
        if self.game_start:
            playGame = GameArea(self.screen, self.ratio)
            playGame.play()
        else:
            return "start"
