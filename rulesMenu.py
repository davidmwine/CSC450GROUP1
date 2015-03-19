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
        self.rules_count = 3  #Number of rules/rule pages - *change later

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
               and mouseY > self.screen.get_height()/8+self.y_offset+335 and mouseY < self.screen.get_height()/8+self.y_offset+self.img_arrow_left.get_height()+345:
                self.rules_next_page(-1)
                return True
        #Next page
        if self.rules_page < self.rules_count:
            if mouseX > self.screen.get_width()/2+245\
               and mouseX < self.screen.get_width()/2+320\
               and mouseY > self.screen.get_height()/8+self.y_offset+335 and mouseY < self.screen.get_height()/8+self.y_offset+self.img_arrow.get_height()+345:
                self.rules_next_page(1)
                return True
        #Index:Introduction
        if mouseX > self.screen.get_width()/2-168\
               and mouseX < self.screen.get_width()/2-157+self.text_intro.get_width()\
               and mouseY > self.screen.get_height()/8+self.y_offset+375 and mouseY < self.screen.get_height()/8+self.y_offset+self.text_intro.get_height()+385:
                self.rules_next_page(1,True)
                return True
        #Index:Objective
        if mouseX > self.screen.get_width()/2-153+self.text_intro.get_width()\
               and mouseX < self.screen.get_width()/2-142+self.text_intro.get_width()+self.text_objective.get_width()\
               and mouseY > self.screen.get_height()/8+self.y_offset+375 and mouseY < self.screen.get_height()/8+self.y_offset+self.text_objective.get_height()+385:
                self.rules_next_page(2,True)
                return True
        #Index:General
        if mouseX > self.screen.get_width()/2-138+self.text_intro.get_width()+self.text_objective.get_width()\
               and mouseX < self.screen.get_width()/2-127+self.text_intro.get_width()+self.text_objective.get_width()+self.text_general.get_width()\
               and mouseY > self.screen.get_height()/8+self.y_offset+375 and mouseY < self.screen.get_height()/8+self.y_offset+self.text_general.get_height()+385:
                self.rules_next_page(3,True)
                return True  
        return True

    def rules_next_page(self, pageNum=None, index=False):
        if pageNum == None:
            self.rules_page = 1
        elif index == True:
                self.rules_page = pageNum
        else:
            self.rules_page += pageNum

        if self.rules_page == 1:
            self.rules_header = "Introduction"
            self.rules_words = ["Mastering MSU is a turn based game for online play.",
                                "The game supports up to six players competing",
                                "against each other to rule the campus. The game is",
                                "free to download and free to play."]
        if self.rules_page == 2:
            self.rules_header = "Objective"
            self.rules_words = ["Here are some rules for you to look at and stuff.",
                                "Here's some more info."]
        if self.rules_page == 3:
            self.rules_header = "General Rules"
            self.rules_words = ["Here are some rules for you to look at and stuff.",
                                "Here's some more info."]


    def run(self):
        self.rules_next_page()
        
        self.text_exit_rules = self.font_op(22,"berlin").render("Exit Rules",True,(220,146,40))
        
        #Index text
        self.text_intro = self.font_op(22,"berlin").render("Introduction",True,(255,255,255))
        self.text_objective = self.font_op(22,"berlin").render("Objective",True,(255,255,255))
        self.text_general = self.font_op(22,"berlin").render("General",True,(255,255,255))
        self.text_rule1 = self.font_op(20,"berlin").render("Pieces",True,(255,255,255))
        self.text_rule2 = self.font_op(20,"berlin").render("Properties",True,(255,255,255))
        self.text_rule3 = self.font_op(20,"berlin").render("Rule 3",True,(255,255,255))
        self.text_rule4 = self.font_op(20,"berlin").render("Rule 4",True,(255,255,255))
        self.text_rule5 = self.font_op(20,"berlin").render("Rule 5",True,(255,255,255))
        self.text_rule6 = self.font_op(20,"berlin").render("Rule 6",True,(255,255,255))
        self.text_rule7 = self.font_op(20,"berlin").render("Rule 7",True,(255,255,255))
        self.text_rule8 = self.font_op(20,"berlin").render("Rule 8",True,(255,255,255))
        self.text_rule9 = self.font_op(20,"berlin").render("Rule 9",True,(255,255,255))
        self.text_rule10 = self.font_op(20,"berlin").render("Rule 10",True,(255,255,255))
        self.text_rule11 = self.font_op(20,"berlin").render("Rule 11",True,(255,255,255))
        self.text_rule12 = self.font_op(20,"berlin").render("Rule 12",True,(255,255,255))
        self.text_rule13 = self.font_op(20,"berlin").render("Rule 13",True,(255,255,255))
        self.text_rule14 = self.font_op(20,"berlin").render("Rule 14",True,(255,255,255))
        self.text_rule15 = self.font_op(20,"berlin").render("Rule 15",True,(255,255,255))
        self.text_rule16 = self.font_op(20,"berlin").render("Rule 16",True,(255,255,255))
        self.text_rule17 = self.font_op(20,"berlin").render("Rule 17",True,(255,255,255))
        self.text_rule18 = self.font_op(20,"berlin").render("Rule 18",True,(255,255,255))
        self.text_rule19 = self.font_op(20,"berlin").render("Rule 19",True,(255,255,255))
        self.text_rule20 = self.font_op(20,"berlin").render("Rule 20",True,(255,255,255))

        self.rules_index = [self.text_intro, self.text_objective, self.text_general, self.text_rule1,
                                self.text_rule2, self.text_rule3, self.text_rule4, self.text_rule5,
                                self.text_rule6, self.text_rule7, self.text_rule8, self.text_rule9,
                                self.text_rule10, self.text_rule11, self.text_rule12, self.text_rule13,
                                self.text_rule14, self.text_rule15, self.text_rule16, self.text_rule17,
                                self.text_rule18, self.text_rule19, self.text_rule20]
            
        rules_exit = False
        
        while not rules_exit:
            self.screen.blit(pygame.transform.scale(self.img_menu_bg,(self.screen.get_width(),\
                            int(self.screen.get_height()-(2*self.y_offset)))),(0,self.y_offset))

            self.text_header = self.font_op(50,"berlin").render(self.rules_header,True,(255,255,255))
            self.screen.blit(self.text_header,(self.screen.get_width()/2-0.5*self.text_header.get_width(),self.screen.get_height()/50+self.y_offset))

            #Rules rects
            pygame.draw.rect(self.screen,(255,255,255),Rect((self.screen.get_width()/2-300,self.screen.get_height()/8+self.y_offset),\
                                                            (600,365)))
            pygame.draw.rect(self.screen,(0,0,0),Rect((self.screen.get_width()/2-300,self.screen.get_height()/8+self.y_offset),\
                                                      (600,365)),2)

            #Page number / exit button
            self.screen.blit(self.text_exit_rules,(self.screen.get_width()/2+198,self.screen.get_height()/8+self.y_offset))
            self.screen.blit(self.font_op(22,"berlin").render(str(self.rules_page)+" of "+\
                                str(self.rules_count),True,(220,146,40)),(self.screen.get_width()/2-294,self.screen.get_height()/8+self.y_offset))

            #Draw red line
            pygame.draw.line(self.screen, (242,107,122), (self.screen.get_width()/2-298,150+self.y_offset),\
                             (self.screen.get_width()/2+298,150+self.y_offset), 1)
            #Draw blue lines
            for line in range(11): 
                pygame.draw.line(self.screen, (209,229,240), (self.screen.get_width()/2-298,175+self.y_offset+line*25),\
                                 (self.screen.get_width()/2+297,175+self.y_offset+line*25), 1)

            #Rules index rects
            pygame.draw.rect(self.screen,(220,146,40),Rect((self.screen.get_width()/2-400,self.screen.get_height()/8+self.y_offset+375),\
                                                            (800,90)))
            pygame.draw.rect(self.screen,(255,255,255),Rect((self.screen.get_width()/2-400,self.screen.get_height()/8+self.y_offset+375),\
                                                            (800,90)),2)
            
            #Display rules index
            spacer = 0
            for text in range(len(self.rules_index)):
                if text >= 0 and text <= 2:
                    self.screen.blit(self.rules_index[text],((self.screen.get_width()/2-162)+spacer,self.screen.get_height()/8+self.y_offset+380))
                    spacer += self.rules_index[text].get_width() + 15
                    if text == 2:
                        spacer = 0
                elif text >= 3 and text <= 12:
                    self.screen.blit(self.rules_index[text],((self.screen.get_width()/2-390)+spacer,self.screen.get_height()/8+self.y_offset+405))
                    spacer += self.rules_index[text].get_width() + 15
                    if text == 12:
                        spacer = 0
                elif text >= 13 and text <= 22:
                    self.screen.blit(self.rules_index[text],((self.screen.get_width()/2-390)+spacer,self.screen.get_height()/8+self.y_offset+430))
                    spacer += self.rules_index[text].get_width() + 15
                    
            #Next/Prev rule arrows
            if self.rules_page < self.rules_count:
                self.screen.blit(self.img_arrow,(self.screen.get_width()/2+250,self.screen.get_height()/8+self.y_offset+340))
            if self.rules_page > 1:
                self.screen.blit(self.img_arrow_left,(self.screen.get_width()/2-315,self.screen.get_height()/8+self.y_offset+340))

            #Display rules on page  
            for text in range(len(self.rules_words)): 
                textOut = self.font_op(18,"helvetica").render(self.rules_words[text],True,(35,35,35))
                self.screen.blit(textOut,(self.screen.get_width()/2-250,156+self.y_offset+text*25))
                
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        rules_exit = True
                        break
                elif event.type == MOUSEBUTTONDOWN: 
                    if not self.buttonClick():
                        rules_exit = True
                        break
                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
            pygame.display.update()
        return "start"
