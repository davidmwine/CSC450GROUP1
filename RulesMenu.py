import pygame
from pygame.locals import *
import os
import sys

class Rules(object):
    def __init__(self, screen, fontOp, yOffset):
        self.screen = screen
        self.fontOp = fontOp
        self.yOffset = yOffset
        self.loadImages()
        self.rulesCount = 3  #Number of rules/rule pages - *change later

    def loadImages(self):     
        self.imgArrow = pygame.image.load(os.path.join("img","arrow.png")).convert_alpha()
        self.imgArrowLeft = pygame.image.load(os.path.join("img","arrowLeft.png")).convert_alpha()
        self.imgMenuBG = pygame.image.load(os.path.join("img","menu_bg4.png")).convert()
        

    def buttonClick(self):
        mouseX,mouseY = pygame.mouse.get_pos()
        #Exit rules
        if mouseX > self.screen.get_width()/2+194\
           and mouseX < self.screen.get_width()/2+295\
           and mouseY > self.screen.get_height()/8+self.yOffset-5 and mouseY < self.screen.get_height()/8+self.yOffset+self.textExitRules.get_height()+5:
            return False
        #Prev page
        if self.rulesPage > 1:
            if mouseX > self.screen.get_width()/2-310\
               and mouseX < self.screen.get_width()/2-254\
               and mouseY > self.screen.get_height()/8+self.yOffset+335 and mouseY < self.screen.get_height()/8+self.yOffset+self.imgArrowLeft.get_height()+345:
                self.rulesNextPage(-1)
                return True
        #Next page
        if self.rulesPage < self.rulesCount:
            if mouseX > self.screen.get_width()/2+245\
               and mouseX < self.screen.get_width()/2+320\
               and mouseY > self.screen.get_height()/8+self.yOffset+335 and mouseY < self.screen.get_height()/8+self.yOffset+self.imgArrow.get_height()+345:
                self.rulesNextPage(1)
                return True
        #Index:Introduction
        if mouseX > self.screen.get_width()/2-168\
               and mouseX < self.screen.get_width()/2-157+self.textIntro.get_width()\
               and mouseY > self.screen.get_height()/8+self.yOffset+375 and mouseY < self.screen.get_height()/8+self.yOffset+self.textIntro.get_height()+385:
                self.rulesNextPage(1,True)
                return True
        #Index:Objective
        if mouseX > self.screen.get_width()/2-153+self.textIntro.get_width()\
               and mouseX < self.screen.get_width()/2-142+self.textIntro.get_width()+self.textObjective.get_width()\
               and mouseY > self.screen.get_height()/8+self.yOffset+375 and mouseY < self.screen.get_height()/8+self.yOffset+self.textObjective.get_height()+385:
                self.rulesNextPage(2,True)
                return True
        #Index:General
        if mouseX > self.screen.get_width()/2-138+self.textIntro.get_width()+self.textObjective.get_width()\
               and mouseX < self.screen.get_width()/2-127+self.textIntro.get_width()+self.textObjective.get_width()+self.textGeneral.get_width()\
               and mouseY > self.screen.get_height()/8+self.yOffset+375 and mouseY < self.screen.get_height()/8+self.yOffset+self.textGeneral.get_height()+385:
                self.rulesNextPage(3,True)
                return True  
        return True

    def rulesNextPage(self, pageNum=None, index=False):
        if pageNum == None:
            self.rulesPage = 1
        elif index == True:
                self.rulesPage = pageNum
        else:
            self.rulesPage += pageNum

        if self.rulesPage == 1:
            self.rulesHeader = "Introduction"
            self.rulesWords = ["Mastering MSU is a turn based game for online play.",
                                "The game supports up to six players competing",
                                "against each other to rule the campus. The game is",
                                "free to download and free to play."]
        if self.rulesPage == 2:
            self.rulesHeader = "Objective"
            self.rulesWords = ["Here are some rules for you to look at and stuff.",
                                "Here's some more info."]
        if self.rulesPage == 3:
            self.rulesHeader = "General Rules"
            self.rulesWords = ["Here are some rules for you to look at and stuff.",
                                "Here's some more info."]


    def run(self):
        self.rulesNextPage()
        
        self.textExitRules = self.fontOp(22,"berlin").render("Exit Rules",True,(220,146,40))
        
        #Index text
        self.textIntro = self.fontOp(22,"berlin").render("Introduction",True,(255,255,255))
        self.textObjective = self.fontOp(22,"berlin").render("Objective",True,(255,255,255))
        self.textGeneral = self.fontOp(22,"berlin").render("General",True,(255,255,255))
        self.textRule1 = self.fontOp(20,"berlin").render("Pieces",True,(255,255,255))
        self.textRule2 = self.fontOp(20,"berlin").render("Properties",True,(255,255,255))
        self.textRule3 = self.fontOp(20,"berlin").render("Rule 3",True,(255,255,255))
        self.textRule4 = self.fontOp(20,"berlin").render("Rule 4",True,(255,255,255))
        self.textRule5 = self.fontOp(20,"berlin").render("Rule 5",True,(255,255,255))
        self.textRule6 = self.fontOp(20,"berlin").render("Rule 6",True,(255,255,255))
        self.textRule7 = self.fontOp(20,"berlin").render("Rule 7",True,(255,255,255))
        self.textRule8 = self.fontOp(20,"berlin").render("Rule 8",True,(255,255,255))
        self.textRule9 = self.fontOp(20,"berlin").render("Rule 9",True,(255,255,255))
        self.textRule10 = self.fontOp(20,"berlin").render("Rule 10",True,(255,255,255))
        self.textRule11 = self.fontOp(20,"berlin").render("Rule 11",True,(255,255,255))
        self.textRule12 = self.fontOp(20,"berlin").render("Rule 12",True,(255,255,255))
        self.textRule13 = self.fontOp(20,"berlin").render("Rule 13",True,(255,255,255))
        self.textRule14 = self.fontOp(20,"berlin").render("Rule 14",True,(255,255,255))
        self.textRule15 = self.fontOp(20,"berlin").render("Rule 15",True,(255,255,255))
        self.textRule16 = self.fontOp(20,"berlin").render("Rule 16",True,(255,255,255))
        self.textRule17 = self.fontOp(20,"berlin").render("Rule 17",True,(255,255,255))
        self.textRule18 = self.fontOp(20,"berlin").render("Rule 18",True,(255,255,255))
        self.textRule19 = self.fontOp(20,"berlin").render("Rule 19",True,(255,255,255))
        self.textRule20 = self.fontOp(20,"berlin").render("Rule 20",True,(255,255,255))

        self.rulesIndex = [self.textIntro, self.textObjective, self.textGeneral, self.textRule1,
                                self.textRule2, self.textRule3, self.textRule4, self.textRule5,
                                self.textRule6, self.textRule7, self.textRule8, self.textRule9,
                                self.textRule10, self.textRule11, self.textRule12, self.textRule13,
                                self.textRule14, self.textRule15, self.textRule16, self.textRule17,
                                self.textRule18, self.textRule19, self.textRule20]
            
        rulesExit = False
        
        while not rulesExit:
            self.screen.blit(pygame.transform.scale(self.imgMenuBG,(self.screen.get_width(),\
                            int(self.screen.get_height()-(2*self.yOffset)))),(0,self.yOffset))

            self.textHeader = self.fontOp(50,"berlin").render(self.rulesHeader,True,(255,255,255))
            self.screen.blit(self.textHeader,(self.screen.get_width()/2-0.5*self.textHeader.get_width(),self.screen.get_height()/50+self.yOffset))

            #Rules rects
            pygame.draw.rect(self.screen,(255,255,255),Rect((self.screen.get_width()/2-300,self.screen.get_height()/8+self.yOffset),\
                                                            (600,365)))
            pygame.draw.rect(self.screen,(0,0,0),Rect((self.screen.get_width()/2-300,self.screen.get_height()/8+self.yOffset),\
                                                      (600,365)),2)

            #Page number / exit button
            self.screen.blit(self.textExitRules,(self.screen.get_width()/2+198,self.screen.get_height()/8+self.yOffset))
            self.screen.blit(self.fontOp(22,"berlin").render(str(self.rulesPage)+" of "+\
                                str(self.rulesCount),True,(220,146,40)),(self.screen.get_width()/2-294,self.screen.get_height()/8+self.yOffset))

            #Draw red line
            pygame.draw.line(self.screen, (242,107,122), (self.screen.get_width()/2-298,150+self.yOffset),\
                             (self.screen.get_width()/2+298,150+self.yOffset), 1)
            #Draw blue lines
            for line in range(11): 
                pygame.draw.line(self.screen, (209,229,240), (self.screen.get_width()/2-298,175+self.yOffset+line*25),\
                                 (self.screen.get_width()/2+297,175+self.yOffset+line*25), 1)

            #Rules index rects
            pygame.draw.rect(self.screen,(220,146,40),Rect((self.screen.get_width()/2-400,self.screen.get_height()/8+self.yOffset+375),\
                                                            (800,90)))
            pygame.draw.rect(self.screen,(255,255,255),Rect((self.screen.get_width()/2-400,self.screen.get_height()/8+self.yOffset+375),\
                                                            (800,90)),2)
            
            #Display rules index
            spacer = 0
            for text in range(len(self.rulesIndex)):
                if text >= 0 and text <= 2:
                    self.screen.blit(self.rulesIndex[text],((self.screen.get_width()/2-162)+spacer,self.screen.get_height()/8+self.yOffset+380))
                    spacer += self.rulesIndex[text].get_width() + 15
                    if text == 2:
                        spacer = 0
                elif text >= 3 and text <= 12:
                    self.screen.blit(self.rulesIndex[text],((self.screen.get_width()/2-390)+spacer,self.screen.get_height()/8+self.yOffset+405))
                    spacer += self.rulesIndex[text].get_width() + 15
                    if text == 12:
                        spacer = 0
                elif text >= 13 and text <= 22:
                    self.screen.blit(self.rulesIndex[text],((self.screen.get_width()/2-390)+spacer,self.screen.get_height()/8+self.yOffset+430))
                    spacer += self.rulesIndex[text].get_width() + 15
                    
            #Next/Prev rule arrows
            if self.rulesPage < self.rulesCount:
                self.screen.blit(self.imgArrow,(self.screen.get_width()/2+250,self.screen.get_height()/8+self.yOffset+340))
            if self.rulesPage > 1:
                self.screen.blit(self.imgArrowLeft,(self.screen.get_width()/2-315,self.screen.get_height()/8+self.yOffset+340))

            #Display rules on page  
            for text in range(len(self.rulesWords)): 
                textOut = self.fontOp(18,"helvetica").render(self.rulesWords[text],True,(35,35,35))
                self.screen.blit(textOut,(self.screen.get_width()/2-250,156+self.yOffset+text*25))
                
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        rulesExit = True
                        break
                elif event.type == MOUSEBUTTONDOWN: 
                    if not self.buttonClick():
                        rulesExit = True
                        break
                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
            pygame.display.update()
        return "start"
