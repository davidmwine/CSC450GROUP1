import pygame
from pygame.locals import *
import os
import sys

class Rules(object):
    def __init__(self, screen, font_op, y_offset):
        self.screen = screen
        self.font_op = font_op
        self.y_offset = y_offset
        self.load_images()
        self.rules_count = 3  #Number of rules/rule pages

    def load_images(self):     
        self.img_arrow = pygame.image.load(os.path.join("img","arrow.png")).convert_alpha()
        self.img_arrow_left = pygame.image.load(os.path.join("img","arrowLeft.png")).convert_alpha()
        self.img_menu_bg = pygame.image.load(os.path.join("img","menu_bg4.png")).convert()
        

    def buttonClick(self):
        mouseX,mouseY = pygame.mouse.get_pos()
        #Exit rules
        if mouseX > self.screen.get_width()/2+194\
           and mouseX < self.screen.get_width()/2+295\
           and mouseY > self.screen.get_height()/8+self.y_offset-5 and mouseY < self.screen.get_height()/8+self.y_offset+self.text_exit_rules.get_height()+5:
            return False
        #Prev page
        if self.rules_page > 1:
            if mouseX > self.screen.get_width()/2-310\
               and mouseX < self.screen.get_width()/2-254\
               and mouseY > self.y_offset+5*self.screen.get_height()/7-5 and mouseY < self.y_offset+5*self.screen.get_height()/7+self.img_arrow_left.get_height()+5:
                self.rules_next_page(-1)
                return True
        #Next page
        if self.rules_page < self.rules_count:
            if mouseX > self.screen.get_width()/2+245\
               and mouseX < self.screen.get_width()/2+320\
               and mouseY > self.y_offset+5*self.screen.get_height()/7-5 and mouseY < self.y_offset+5*self.screen.get_height()/7+self.img_arrow_left.get_height()+5:
                self.rules_next_page(1)
                return True
        return True

    def run(self):
        self.rules_next_page()
        rules_exit = False
        self.text_exit_rules = self.font_op(22,"berlin").render("Exit Rules",True,(220,146,40))
        #self.text_exit_rules_bg = self.font_op(22,"berlin").render("Exit Rules",True,(75,75,75))
        while not rules_exit:
            self.screen.blit(pygame.transform.scale(self.img_menu_bg,(self.screen.get_width(),\
                            int(self.screen.get_height()-(2*self.y_offset)))),(0,self.y_offset))
            pygame.draw.rect(self.screen,(255,255,255),Rect((self.screen.get_width()/2-300,self.screen.get_height()/8+self.y_offset),\
                                                            (600,self.y_offset+5*self.screen.get_height()/8)))
            #self.screen.blit(self.img_rules,((self.screen.get_width()/2)-(self.img_rules.get_width()/2),\
                                             #self.screen.get_height()-150-self.y_offset))
            pygame.draw.rect(self.screen,(0,0,0),Rect((self.screen.get_width()/2-300,self.screen.get_height()/8+self.y_offset),\
                                                      (600,self.y_offset+5*self.screen.get_height()/8)),2)
            self.screen.blit(self.text_exit_rules,(self.screen.get_width()/2+198,self.screen.get_height()/8+self.y_offset))

            pygame.draw.line(self.screen, (242,107,122), (self.screen.get_width()/2-298,1.8*self.screen.get_height()/8+self.y_offset),\
                             (self.screen.get_width()/2+298,1.8*self.screen.get_height()/8+self.y_offset), 1) #Draw red line
            lineRange = int((self.screen.get_height()/8+(self.y_offset/2))/7)
            for line in range(lineRange): #Draw blue lines
                pygame.draw.line(self.screen, (209,229,240), (self.screen.get_width()/2-298,2.2*self.screen.get_height()/8+self.y_offset+line*25),\
                                 (self.screen.get_width()/2+297,2.2*self.screen.get_height()/8+self.y_offset+line*25), 1)
 
            if self.rules_page < self.rules_count:
                self.screen.blit(self.img_arrow,(self.screen.get_width()/2+250,(1.28*self.y_offset)+5*self.screen.get_height()/7))
            if self.rules_page > 1:
                self.screen.blit(self.img_arrow_left,(self.screen.get_width()/2-315,(1.28*self.y_offset)+5*self.screen.get_height()/7))

            #Page number display
            self.screen.blit(self.font_op(22,"berlin").render(str(self.rules_page)+" of "+\
                                str(self.rules_count),True,(220,146,40)),(self.screen.get_width()/2-294,self.screen.get_height()/8+self.y_offset))
            
            header = self.font_op(50,"berlin").render(self.rules_header,True,(255,255,255))
            self.screen.blit(header,(self.screen.get_width()/2-0.5*header.get_width(),self.screen.get_height()/50+self.y_offset))
            
            #Can delete this line, placeholder# self.screen.blit(header,(self.screen.get_width()/2-0.5*header.get_width(),5*self.screen.get_height()/6+self.y_offset))
             
            for text in range(len(self.rules_words)): #Display rules on a page 
                textOut = self.font_op(18,"helvetica").render(self.rules_words[text],True,(35,35,35))
                self.screen.blit(textOut,(self.screen.get_width()/2-240,1.92*self.screen.get_height()/8+(1.28*self.y_offset)+text*25))
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        rules_exit = True
                        break
                elif event.type == MOUSEBUTTONDOWN:  #Perform action on click
                    if not self.buttonClick():
                        rules_exit = True
                        break
                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
            pygame.display.update()
        return "start"

    def rules_next_page(self, pageNum=None):
        if pageNum == None:
            self.rules_page = 1
        else:
            self.rules_page += pageNum
        self.img_rules = pygame.Surface((self.screen.get_width(),150+self.y_offset)).convert()
        bottom_image = "rulesBottom1.png"

        if self.rules_page == 1:
            self.rules_header = "Introduction"
            self.rules_words = ["Mastering MSU is a turn based game for online",
                                "play. The game supports up to six players",
                                "competing against each other to rule the",
                                "campus. The game is free to download and free",
                                "to play."]
        if self.rules_page == 2:
            bottom_image = "rulesBottom2.png"
            self.rules_header = "Objective"
            self.rules_words = ["Here are some rules for you to look at and",
                                "stuff. Here's some more info."]
        if self.rules_page == 3:
            bottom_image = "rulesBottom3.png"
            self.rules_header = "General Rules"
            self.rules_words = ["Here are some rules for you to look at and",
                                "stuff. Here's some more info."]
            
        #self.img_bottom = pygame.image.load(os.path.join("img",bottom_image)).convert()
        #self.img_rules.blit(pygame.transform.scale(self.img_bottom, (self.img_rules.get_width(),150)),(0,0))
