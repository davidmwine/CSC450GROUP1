import pygame
from pygame.locals import *
import os
import sys
import random

class Start(object):
    def __init__(self, screen, fontOp, yOffset):
        self.screen = screen
        self.fontOp = fontOp
        self.yOffset = yOffset
        self.gameActive = 0  #Is the game running or not
        self.percentOfMax = self.screen.get_height()/1080
        #self.quitGame = False
        self.soundRunning = 0
        self.loadImages()
        self.loadSounds()
        self.menuOn = True
        self.rulesOn = False
        self.optionsOn = False
        self.clock = pygame.time.Clock()
        self.extraPad = self.screen.get_height()/16

    def backToStart(self):
        self.rulesOn = False
        self.optionsOn = False
        self.gameOn = False
        self.menuOn = True

    def loadImages(self):
        self.imgLogo = pygame.image.load(os.path.join("img","logo.png")).convert_alpha()
        self.imgMenuBG = pygame.image.load(os.path.join("img","menu_bg4.png")).convert()
        self.imgIconStart = pygame.image.load(os.path.join("img","Dice2b.png")).convert_alpha()
        self.imgIconResume = pygame.image.load(os.path.join("img","thumb_up2.png")).convert_alpha()
        self.imgIconRules = pygame.image.load(os.path.join("img","book-brownb.png")).convert_alpha()
        self.imgIconOptions = pygame.image.load(os.path.join("img","Gear_01b.png")).convert_alpha()
        self.imgIconExit = pygame.image.load(os.path.join("img","Exitb.png")).convert_alpha() #Game exit

    def loadSounds(self): 
        self.soundIntro = pygame.mixer.Sound(os.path.join('sound','radio.wav'))
        self.soundStartMenu = pygame.mixer.Sound(os.path.join('sound','start_menu.wav'))

    def splash(self):           
        soundTime = pygame.time.get_ticks()/1000.0
        textColor = [0,0,0]
        circleCoordinate = 200
        circleThickness = 50
        circleColor = (94,0,9)
        circleColorSelect = 1

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.leaveGame()
                    
            self.clock.tick(30)
            self.screen.fill((0,0,0))
            time = pygame.time.get_ticks()/1000. - soundTime
            
            if time > 1 and time < 6:
                try:
                    pygame.draw.circle(self.screen, circleColor, (int(self.screen.get_width()/2), int(self.screen.get_height()/2) ), circleCoordinate, circleThickness)
                except ValueError:
                    pass
                circleThickness += 4
                
                if circleCoordinate >= self.screen.get_width():
                    circleCoordinate = 200
                    circleThickness = 50
                    if circleColorSelect == -1:
                        circleColor = (94,0,9)
                    else:
                        circleColor = (255,255,255)
                    circleColorSelect = -circleColorSelect
                else:
                    circleCoordinate += 15
                    
                for i in range(3):
                    if textColor[i] < 255:
                        textColor[i] += 1.3
                textTitle = self.fontOp(118,"berlin").render("Mastering MSU",True,textColor)
                #text_team1 = fontOp(24,"helvetica").render("a Team 1 game",True,textColor)
             
                self.screen.blit(self.imgLogo,(self.screen.get_width()/2-0.5*self.imgLogo.get_width(),\
                                                (self.screen.get_height()/2)-self.imgLogo.get_height()+self.yOffset))
                
                self.screen.blit(textTitle,(self.screen.get_width()/2-0.5*textTitle.get_width(),\
                                             (self.screen.get_height()/2)-0.5*self.imgLogo.get_height()+self.yOffset+60))
                #self.screen.blit(text_team1,(self.screen.get_width()/2-0.5*text_team1.get_width(),\
                                             #(self.screen.get_height()/2)-0.5*self.imgLogo.get_height()+self.yOffset+60))
            if time > 1 and self.soundRunning == 0:
                self.soundIntro.play()
                self.soundIntro.fadeout(6000)
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
           and mouseX < self.screen.get_width()/2-52+self.textStart.get_width()\
           and mouseY > (self.screen.get_height()/4+self.yOffset-5)+self.extraPad \
           and mouseY < (self.screen.get_height()/4+self.yOffset+self.textStart.get_height()+5)+self.extraPad:
            self.textStart = self.fontOp(32,"berlin").render("Start Game",True,(255,255,255))
        elif self.gameActive == 1:
            self.textStart = self.fontOp(32,"berlin").render("Start Game",True,(220,146,40))  
            if mouseX > self.screen.get_width()/2-117\
               and mouseX < self.screen.get_width()/2-52+self.textResume.get_width()\
               and mouseY > (70+self.screen.get_height()/4+self.yOffset)+self.extraPad and \
               mouseY < (80+self.screen.get_height()/4+self.yOffset+self.textResume.get_height())+self.extraPad:
                self.textResume = self.fontOp(32,"berlin").render("Resume Game",True,(255,255,255))
            else:
                self.textResume = self.fontOp(32,"berlin").render("Resume Game",True,(220,146,40))
        else:
            self.textStart = self.fontOp(32,"berlin").render("Start Game",True,(220,146,40))    
        if mouseX > self.screen.get_width()/2-117\
           and mouseX < self.screen.get_width()/2-52+self.textRules.get_width()\
           and mouseY > (70+self.screen.get_height()/4+self.yOffset+75*self.gameActive)+self.extraPad\
           and mouseY < (80+self.screen.get_height()/4+self.yOffset+self.textRules.get_height()+75*self.gameActive)+self.extraPad:
            self.textRules = self.fontOp(32,"berlin").render("Rules",True,(255,255,255))
        else:
            self.textRules = self.fontOp(32,"berlin").render("Rules",True,(220,146,40))
        if mouseX > self.screen.get_width()/2-117\
           and mouseX < self.screen.get_width()/2-52+self.textOptions.get_width()\
           and mouseY > (145+self.screen.get_height()/4+self.yOffset+75*self.gameActive)+self.extraPad\
           and mouseY < (155+self.screen.get_height()/4+self.yOffset+self.textOptions.get_height()+75*self.gameActive)+self.extraPad:
            self.textOptions = self.fontOp(32,"berlin").render("Options",True,(255,255,255))
        else:
            self.textOptions = self.fontOp(32,"berlin").render("Options",True,(220,146,40))       
        if mouseX > self.screen.get_width()/2-117\
           and mouseX < self.screen.get_width()/2-52+self.textExit.get_width()\
           and mouseY > (220+self.screen.get_height()/4+self.yOffset+75*self.gameActive)+self.extraPad\
           and mouseY < (230+self.screen.get_height()/4+self.yOffset+self.textExit.get_height()+75*self.gameActive)+self.extraPad:
            self.textExit = self.fontOp(32,"berlin").render("Exit",True,(255,255,255))
        else:
            self.textExit = self.fontOp(32,"berlin").render("Exit",True,(220,146,40))

    def buttonClick(self):
        mouseX,mouseY = pygame.mouse.get_pos()
        #Rules
        if mouseX > self.screen.get_width()/2-117\
           and mouseX < self.screen.get_width()/2-52+self.textRules.get_width()\
           and mouseY > (70+self.screen.get_height()/4+self.yOffset+75*self.gameActive)+self.extraPad\
           and mouseY < (80+self.screen.get_height()/4+self.yOffset+self.textRules.get_height()+75*self.gameActive)+self.extraPad:
            self.menuOn = False
            self.gameOn = False
            self.optionsOn = False
            self.rulesOn = True
        #Options
        if mouseX > self.screen.get_width()/2-117\
           and mouseX < self.screen.get_width()/2-52+self.textOptions.get_width()\
           and mouseY > (145+self.screen.get_height()/4+self.yOffset+75*self.gameActive)+self.extraPad\
           and mouseY < (155+self.screen.get_height()/4+self.yOffset+self.textOptions.get_height()+75*self.gameActive)+self.extraPad:
            self.menuOn = False
            self.rulesOn = False
            self.gameOn = False
            self.optionsOn = True
        #Game
        if mouseX > self.screen.get_width()/2-117\
           and mouseX < self.screen.get_width()/2-52+self.textStart.get_width()\
           and mouseY > (self.screen.get_height()/4+self.yOffset-5)+self.extraPad \
           and mouseY < (self.screen.get_height()/4+self.yOffset+self.textStart.get_height()+5)+self.extraPad:
            self.menuOn = False
            self.rulesOn = False
            self.optionsOn = False
            self.gameOn = True
        #Exit
        if mouseX > self.screen.get_width()/2-117\
           and mouseX < self.screen.get_width()/2-52+self.textExit.get_width()\
           and mouseY > (220+self.screen.get_height()/4+self.yOffset+75*self.gameActive)+self.extraPad\
           and mouseY < (230+self.screen.get_height()/4+self.yOffset+self.textExit.get_height()+75*self.gameActive)+self.extraPad:
            self.leaveGame()
        

    def imageDisplay(self):
        self.screen.fill((0,0,0))
        self.screen.blit(pygame.transform.scale(self.imgMenuBG,(self.screen.get_width(),\
                        int(self.screen.get_height()-(2*self.yOffset)))),(0,self.yOffset))
        
        self.screen.blit(self.textHeaderBG,(self.screen.get_width()/2-3-0.5*self.textHeaderBG.get_width()+4,(4+self.screen.get_height()/30+self.yOffset)+self.extraPad))
        self.screen.blit(self.textHeader,(self.screen.get_width()/2-3-0.5*self.textHeader.get_width(),(self.screen.get_height()/30+self.yOffset)+self.extraPad))

        self.screen.blit(self.textStartBG,(self.screen.get_width()/2-55,(2+self.screen.get_height()/4+self.yOffset)+self.extraPad))
        self.screen.blit(self.textStart,(self.screen.get_width()/2-57,(self.screen.get_height()/4+self.yOffset)+self.extraPad)) 
        self.screen.blit(self.textRulesBG,(self.screen.get_width()/2-55,(77+self.screen.get_height()/4+self.yOffset+75*self.gameActive)+self.extraPad))
        self.screen.blit(self.textRules,(self.screen.get_width()/2-57,(75+self.screen.get_height()/4+self.yOffset+75*self.gameActive)+self.extraPad))
        self.screen.blit(self.textOptionsBG,(self.screen.get_width()/2-55,(152+self.screen.get_height()/4+self.yOffset+75*self.gameActive)+self.extraPad))
        self.screen.blit(self.textOptions,(self.screen.get_width()/2-57,(150+self.screen.get_height()/4+self.yOffset+75*self.gameActive)+self.extraPad))
        self.screen.blit(self.textExitBG,(self.screen.get_width()/2-55,(227+self.screen.get_height()/4+self.yOffset+75*self.gameActive)+self.extraPad))
        self.screen.blit(self.textExit,(self.screen.get_width()/2-57,(225+self.screen.get_height()/4+self.yOffset+75*self.gameActive)+self.extraPad))

        self.screen.blit(self.imgIconStart,(self.screen.get_width()/2-112,(self.screen.get_height()/4+self.yOffset-5)+self.extraPad))
        self.screen.blit(self.imgIconRules,(self.screen.get_width()/2-112,(70+self.screen.get_height()/4+self.yOffset+75*self.gameActive)+self.extraPad))
        self.screen.blit(self.imgIconOptions,(self.screen.get_width()/2-112,(145+self.screen.get_height()/4+self.yOffset+75*self.gameActive)+self.extraPad))
        self.screen.blit(self.imgIconExit,(self.screen.get_width()/2-112,(220+self.screen.get_height()/4+self.yOffset+75*self.gameActive)+self.extraPad))

    def menu(self):
        self.backToStart()
        self.textHeader = self.fontOp(90,"berlin").render("Mastering MSU",True,(255,255,255))
        self.textHeaderBG = self.fontOp(90,"berlin").render("Mastering MSU",True,(0,0,0))
        self.textStart = self.fontOp(32,"berlin").render("Start Game",True,(220,146,40))
        self.textStartBG = self.fontOp(32,"berlin").render("Start Game",True,(0,0,0))
        self.textResume = self.fontOp(32,"berlin").render("Resume Game",True,(220,146,40))
        self.textResumeBG = self.fontOp(32,"berlin").render("Resume Game",True,(0,0,0))
        self.textRules = self.fontOp(32,"berlin").render("Rules",True,(220,146,40))
        self.textRulesBG = self.fontOp(32,"berlin").render("Rules",True,(0,0,0))
        self.textOptions = self.fontOp(32,"berlin").render("Options",True,(220,146,40))
        self.textOptionsBG = self.fontOp(32,"berlin").render("Options",True,(0,0,0))
        self.textExit = self.fontOp(32,"berlin").render("Exit",True,(220,146,40))
        self.textExitBG = self.fontOp(32,"berlin").render("Exit",True,(0,0,0))

        #menu = True
        #rulesActive = False

        while self.menuOn:
            self.clock.tick(30)
            #self.screen.fill((240,240,240))

            if self.soundRunning == 0:
                self.soundStartMenu.play(-1) 
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
                self.screen.blit(self.textResumeBG,(self.screen.get_width()/2-55,(77+self.screen.get_height()/4+self.yOffset)+self.extraPad))
                self.screen.blit(self.textResume,(self.screen.get_width()/2-57,(75+self.screen.get_height()/4+self.yOffset)+self.extraPad))
                self.screen.blit(self.imgIconResume,(self.screen.get_width()/2-112,(70+self.screen.get_height()/4+self.yOffset)+self.extraPad))
            
            pygame.display.update()
        if self.rulesOn:
            return "rules"
        if self.optionsOn:
            return "options"
        if self.gameOn:
            return "game"
