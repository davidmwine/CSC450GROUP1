import pygame
from pygame.locals import *
import os
import sys

class Rules(object):
    def __init__(self, screen, fontOp, yoffset):
        self.screen = screen
        self.fontOp = fontOp
        self.yoffset = yoffset
        self.loadImages()
        self.rulescount = 3  #Number of rules/rule pages - *change later

    def loadImages(self):     
        self.imgarrow = pygame.image.load(os.path.join("img","arrow.png")).convert_alpha()
        self.imgarrowleft = pygame.image.load(os.path.join("img","arrowLeft.png")).convert_alpha()
        self.imgmenubg = pygame.image.load(os.path.join("img","menu_bg4.png")).convert()
        

    def buttonClick(self):
        mousex,mousey = pygame.mouse.get_pos()
        #Exit rules
        if mousex > self.screen.get_width()/2+194\
           and mousex < self.screen.get_width()/2+295\
           and mousey > self.screen.get_height()/8+self.yoffset-5 and mousey < self.screen.get_height()/8+self.yoffset+self.textexitrules.get_height()+5:
            return False
        #Prev page
        if self.rulespage > 1:
            if mousex > self.screen.get_width()/2-310\
               and mousex < self.screen.get_width()/2-254\
               and mousey > self.screen.get_height()/8+self.yoffset+335 and mousey < self.screen.get_height()/8+self.yoffset+self.imgarrowleft.get_height()+345:
                self.rulesNextPage(-1)
                return True
        #Next page
        if self.rulespage < self.rulescount:
            if mousex > self.screen.get_width()/2+245\
               and mousex < self.screen.get_width()/2+320\
               and mousey > self.screen.get_height()/8+self.yoffset+335 and mousey < self.screen.get_height()/8+self.yoffset+self.imgarrow.get_height()+345:
                self.rulesNextPage(1)
                return True
        #Index:Introduction
        if mousex > self.screen.get_width()/2-168\
               and mousex < self.screen.get_width()/2-157+self.textintro.get_width()\
               and mousey > self.screen.get_height()/8+self.yoffset+375 and mousey < self.screen.get_height()/8+self.yoffset+self.textintro.get_height()+385:
                self.rulesNextPage(1,True)
                return True
        #Index:Objective
        if mousex > self.screen.get_width()/2-153+self.textintro.get_width()\
               and mousex < self.screen.get_width()/2-142+self.textintro.get_width()+self.textobjective.get_width()\
               and mousey > self.screen.get_height()/8+self.yoffset+375 and mousey < self.screen.get_height()/8+self.yoffset+self.textobjective.get_height()+385:
                self.rulesNextPage(2,True)
                return True
        #Index:General
        if mousex > self.screen.get_width()/2-138+self.textintro.get_width()+self.textobjective.get_width()\
               and mousex < self.screen.get_width()/2-127+self.textintro.get_width()+self.textobjective.get_width()+self.text_general.get_width()\
               and mousey > self.screen.get_height()/8+self.yoffset+375 and mousey < self.screen.get_height()/8+self.yoffset+self.text_general.get_height()+385:
                self.rulesNextPage(3,True)
                return True  
        return True

    def rulesNextPage(self, pagenum=None, index=False):
        if pagenum == None:
            self.rulespage = 1
        elif index == True:
                self.rulespage = pagenum
        else:
            self.rulespage += pagenum

        if self.rulespage == 1:
            self.rulesheader = "Introduction"
            self.ruleswords = ["Mastering MSU is a turn based game for online play.",
                                "The game supports up to six players competing",
                                "against each other to rule the campus. The game is",
                                "free to download and free to play."]
        if self.rulespage == 2:
            self.rulesheader = "Objective"
            self.ruleswords = ["Here are some rules for you to look at and stuff.",
                                "Here's some more info."]
        if self.rulespage == 3:
            self.rulesheader = "General Rules"
            self.ruleswords = ["Here are some rules for you to look at and stuff.",
                                "Here's some more info."]


    def run(self):
        self.rulesNextPage()
        
        self.textexitrules = self.fontOp(22,"berlin").render("Exit Rules",True,(220,146,40))
        
        #Index text
        self.textintro = self.fontOp(22,"berlin").render("Introduction",True,(255,255,255))
        self.textobjective = self.fontOp(22,"berlin").render("Objective",True,(255,255,255))
        self.text_general = self.fontOp(22,"berlin").render("General",True,(255,255,255))
        self.textrule1 = self.fontOp(20,"berlin").render("Pieces",True,(255,255,255))
        self.textrule2 = self.fontOp(20,"berlin").render("Properties",True,(255,255,255))
        self.textrule3 = self.fontOp(20,"berlin").render("Rule 3",True,(255,255,255))
        self.textrule4 = self.fontOp(20,"berlin").render("Rule 4",True,(255,255,255))
        self.textrule5 = self.fontOp(20,"berlin").render("Rule 5",True,(255,255,255))
        self.textrule6 = self.fontOp(20,"berlin").render("Rule 6",True,(255,255,255))
        self.textrule7 = self.fontOp(20,"berlin").render("Rule 7",True,(255,255,255))
        self.textrule8 = self.fontOp(20,"berlin").render("Rule 8",True,(255,255,255))
        self.textrule9 = self.fontOp(20,"berlin").render("Rule 9",True,(255,255,255))
        self.textrule10 = self.fontOp(20,"berlin").render("Rule 10",True,(255,255,255))
        self.textrule11 = self.fontOp(20,"berlin").render("Rule 11",True,(255,255,255))
        self.textrule12 = self.fontOp(20,"berlin").render("Rule 12",True,(255,255,255))
        self.textrule13 = self.fontOp(20,"berlin").render("Rule 13",True,(255,255,255))
        self.textrule14 = self.fontOp(20,"berlin").render("Rule 14",True,(255,255,255))
        self.textrule15 = self.fontOp(20,"berlin").render("Rule 15",True,(255,255,255))
        self.textrule16 = self.fontOp(20,"berlin").render("Rule 16",True,(255,255,255))
        self.textrule17 = self.fontOp(20,"berlin").render("Rule 17",True,(255,255,255))
        self.textrule18 = self.fontOp(20,"berlin").render("Rule 18",True,(255,255,255))
        self.textrule19 = self.fontOp(20,"berlin").render("Rule 19",True,(255,255,255))
        self.textrule20 = self.fontOp(20,"berlin").render("Rule 20",True,(255,255,255))

        self.rulesindex = [self.textintro, self.textobjective, self.text_general, self.textrule1,
                                self.textrule2, self.textrule3, self.textrule4, self.textrule5,
                                self.textrule6, self.textrule7, self.textrule8, self.textrule9,
                                self.textrule10, self.textrule11, self.textrule12, self.textrule13,
                                self.textrule14, self.textrule15, self.textrule16, self.textrule17,
                                self.textrule18, self.textrule19, self.textrule20]
            
        rulesexit = False
        
        while not rulesexit:
            self.screen.blit(pygame.transform.scale(self.imgmenubg,(self.screen.get_width(),\
                            int(self.screen.get_height()-(2*self.yoffset)))),(0,self.yoffset))

            self.text_header = self.fontOp(50,"berlin").render(self.rulesheader,True,(255,255,255))
            self.screen.blit(self.text_header,(self.screen.get_width()/2-0.5*self.text_header.get_width(),self.screen.get_height()/50+self.yoffset))

            #Rules rects
            pygame.draw.rect(self.screen,(255,255,255),Rect((self.screen.get_width()/2-300,self.screen.get_height()/8+self.yoffset),\
                                                            (600,365)))
            pygame.draw.rect(self.screen,(0,0,0),Rect((self.screen.get_width()/2-300,self.screen.get_height()/8+self.yoffset),\
                                                      (600,365)),2)

            #Page number / exit button
            self.screen.blit(self.textexitrules,(self.screen.get_width()/2+198,self.screen.get_height()/8+self.yoffset))
            self.screen.blit(self.fontOp(22,"berlin").render(str(self.rulespage)+" of "+\
                                str(self.rulescount),True,(220,146,40)),(self.screen.get_width()/2-294,self.screen.get_height()/8+self.yoffset))

            #Draw red line
            pygame.draw.line(self.screen, (242,107,122), (self.screen.get_width()/2-298,150+self.yoffset),\
                             (self.screen.get_width()/2+298,150+self.yoffset), 1)
            #Draw blue lines
            for line in range(11): 
                pygame.draw.line(self.screen, (209,229,240), (self.screen.get_width()/2-298,175+self.yoffset+line*25),\
                                 (self.screen.get_width()/2+297,175+self.yoffset+line*25), 1)

            #Rules index rects
            pygame.draw.rect(self.screen,(220,146,40),Rect((self.screen.get_width()/2-400,self.screen.get_height()/8+self.yoffset+375),\
                                                            (800,90)))
            pygame.draw.rect(self.screen,(255,255,255),Rect((self.screen.get_width()/2-400,self.screen.get_height()/8+self.yoffset+375),\
                                                            (800,90)),2)
            
            #Display rules index
            spacer = 0
            for text in range(len(self.rulesindex)):
                if text >= 0 and text <= 2:
                    self.screen.blit(self.rulesindex[text],((self.screen.get_width()/2-162)+spacer,self.screen.get_height()/8+self.yoffset+380))
                    spacer += self.rulesindex[text].get_width() + 15
                    if text == 2:
                        spacer = 0
                elif text >= 3 and text <= 12:
                    self.screen.blit(self.rulesindex[text],((self.screen.get_width()/2-390)+spacer,self.screen.get_height()/8+self.yoffset+405))
                    spacer += self.rulesindex[text].get_width() + 15
                    if text == 12:
                        spacer = 0
                elif text >= 13 and text <= 22:
                    self.screen.blit(self.rulesindex[text],((self.screen.get_width()/2-390)+spacer,self.screen.get_height()/8+self.yoffset+430))
                    spacer += self.rulesindex[text].get_width() + 15
                    
            #Next/Prev rule arrows
            if self.rulespage < self.rulescount:
                self.screen.blit(self.imgarrow,(self.screen.get_width()/2+250,self.screen.get_height()/8+self.yoffset+340))
            if self.rulespage > 1:
                self.screen.blit(self.imgarrowleft,(self.screen.get_width()/2-315,self.screen.get_height()/8+self.yoffset+340))

            #Display rules on page  
            for text in range(len(self.ruleswords)): 
                textOut = self.fontOp(18,"helvetica").render(self.ruleswords[text],True,(35,35,35))
                self.screen.blit(textOut,(self.screen.get_width()/2-250,156+self.yoffset+text*25))
                
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        rulesexit = True
                        break
                elif event.type == MOUSEBUTTONDOWN: 
                    if not self.buttonClick():
                        rulesexit = True
                        break
                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
            pygame.display.update()
        return "start"
