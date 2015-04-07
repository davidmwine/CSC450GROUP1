import pygame, sys, os
from pygame.locals import *
from Player import Player
import Colors
from ChatBoxCopy import ChatBox
from RadioButton import RadioGroup
from Controls import Button
from TextWrap import *
from EntryBox import EntryBoxSet
from Network import *


class Lobby():

    def __init__(self, font_op ,parent ,scale = 1):
        '''Screen for the lobby before game start.  Takes font_op, parent, and scale attributes'''

        #Screen Attributes
        self.width = int(scale*1920)
        self.height = int(scale*1080)
        self.font_op = font_op
        self.scale = scale
        self.parent = parent
        self.screen = pygame.Surface((self.width, self.height))

        #list for determining which screen to draw
        self.gameType = [self.hostDraw,self.lfgDraw, self.localGameDraw]
        self.gameOpt = 0

        #booleans
        self.enterForm = False

        #return on exit
        self.nextScreen = ''


    def load(self, gameOpt):
        '''Loads the images and text needed for the base screen to draw on takes game option code
to determine the inital screen'''
        self.bg = pygame.image.load(os.path.join("img","menu_bg4.png"))

        #Lists of screen description texts and widths
        self.text_list = []
        self.text_list.append(self.font_op(20, 'berlin').render("Host a game.", 1, (0,0,0)))
        self.text_list.append(self.font_op(20, 'berlin').render("Join a game.",1,(0,0,0)))
        self.text_list.append(self.font_op(20, 'berlin').render("Start a local game.",1,(0,0,0)))
        self.width_list = [i.get_width() for i in self.text_list] #for bliting in loop
        self.width_less_radio = self.width - sum(self.width_list)

        #radio buttons to determine screen to show and game type
        self.gameTypeRadio = RadioGroup(self.screen)
        
        self.gameTypeRadio.newButton(self.width_less_radio/2, self.height/8+15, 5)
        self.gameTypeRadio.newButton(self.width_less_radio/2+ self.width_list[0] +32, self.height/8+15, 5)
        self.gameTypeRadio.newButton(self.width_less_radio/2+ sum(self.width_list[:2]) +50, self.height/8+15, 5)
        self.gameTypeRadio.setCurrent(gameOpt)

        #Start Game button
        buttonRect= Rect(0 , self.height -80*self.scale, 300*self.scale, 80*self.scale)
        self.startButton = Button(self.screen, buttonRect, "Start Game")
        buttonRect= Rect(300*self.scale , self.height -80*self.scale, 300*self.scale, 80*self.scale)
        self.backButton = Button(self.screen, buttonRect, "Back")
        buttonRect= Rect(600*self.scale , self.height -80*self.scale, 300*self.scale, 80*self.scale)
        self.optButton = Button(self.screen, buttonRect, "Options")
        
        #init screens
        self.hostScreen = self.screen.subsurface(self.width/10, self.height/3,self.width*8/10, self.height/3)
        offset1 = [self.width/10, self.height/3]
        self.lfgScreen = self.screen.subsurface(self.width/10, self.height/3,self.width*5/8, self.height*2/3-self.height/10)
        self.localScreen = self.screen.subsurface(self.width/10, self.height/3,self.width*8/10, self.height/3)
        offset3 = [self.width/10, self.height/3]
        
        #chat Box
        rect = pygame.Rect((1440*self.scale, 810*self.scale),
                           (480*self.scale, 270*self.scale))
        self.chatBox = ChatBox(self.scale, self.screen, rect)

        #Host form fields
        self.hostAttributes = EntryBoxSet(self.scale)
        boxRect = Rect(self.hostScreen.get_width()/3+200*self.scale, self.hostScreen.get_height()/4,40*self.scale,30*self.scale)
        self.hostAttributes.createNew(self.hostScreen,1 ,boxRect, self.font_op, offset1, '1')
        boxRect = Rect(self.hostScreen.get_width()/3+200*self.scale, self.hostScreen.get_height()/4+30*self.scale,40*self.scale,30*self.scale)
        self.hostAttributes.createNew(self.hostScreen,15, boxRect, self.font_op , offset1, "Mastering MSU")
        boxRect = Rect(self.hostScreen.get_width()/3+200*self.scale, self.hostScreen.get_height()/4+60*self.scale,40*self.scale,30*self.scale)
        self.hostAttributes.createNew(self.hostScreen,15 ,boxRect, self.font_op, offset1, "Player 1")

        #LFG form Fields
        self.lfgAttributes = EntryBoxSet(self.scale)

        #Local Form Fields
        self.localAttributes = EntryBoxSet(self.scale)
        boxRect = Rect(self.localScreen.get_width()/3+200*self.scale, self.localScreen.get_height()/4,40*self.scale,30*self.scale)
        self.localAttributes.createNew(self.localScreen,1 ,boxRect, self.font_op, offset3, '1')
        self.localAttributes.getBox('0').setMaxChar(1)
        
        #Render Text
        self.hostText = self.font_op(40*self.scale, 'berlin').render("Please select game attributes.",1,(0,0,0))
        self.lfgText = self.font_op(40*self.scale, 'berlin').render("Please select a game to join.",1,(0,0,0))
        self.playersNumText = self.font_op(20*self.scale, 'berlin').render("Number of Players",1,(0,0,0))
        self.gameNameText = self.font_op(20*self.scale, 'berlin').render("Name of Game",1,(0,0,0))
        self.hostNameText = self.font_op(20*self.scale, 'berlin').render("Name of Host",1,(0,0,0))

        #For changing entry box sets
        self.entBoxes = [self.hostAttributes, self.lfgAttributes, self.localAttributes]


        


    def buttonClick(self):
        '''determine what happens when the mouse is clicked'''
        #Takes action if a button is clicked
        mouseX, mouseY = pygame.mouse.get_pos() 
        if self.gameTypeRadio.checkButton(mouseX, mouseY):
            self.gameOpt = self.gameTypeRadio.getCurrent()
            return
        if self.startButton.wasClicked(mouseX, mouseY):
            self.gameExit = True
            self.nextScreen = 'game'
            return
        if self.backButton.wasClicked(mouseX, mouseY):
            self.gameExit = True
            self.nextScreen = 'start'
            return
        if self.gameOpt == 2 and self.localAttributes.isClicked(mouseX, mouseY):
            self.enterForm = True
        if self.gameOpt == 1 and self.lfgAttributes.isClicked(mouseX, mouseY):
            self.enterForm = True
        if self.gameOpt == 0 and self.hostAttributes.isClicked(mouseX, mouseY):
            self.enterForm = True
            
    def alwaysDraw(self):
        '''Screen that is always drawn no matter which radio button is selected should be run before other draw functions'''

        #draws background and radio buttons
        self.screen.blit(self.bg, (0,0))
        for i in range(len(self.text_list)):
            self.screen.blit(self.text_list[i], (self.width_less_radio/2 +20*(i+1) + sum(self.width_list[:i]),
                                                 self.height/8,self.width_list[i],self.text_list[i].get_height()))
        self.gameTypeRadio.draw()
        self.startButton.redraw()
        self.backButton.redraw()
        self.optButton.redraw()
        self.chatBox.redraw()
        
        
        


    def hostDraw(self):
        '''Host game screen for entering inital game attributes, only drawn if radio button 1 is selected'''

        
        self.hostScreen.fill((255,255,255))
        
        #draws the text on the screen
        textRect = (((self.hostScreen.get_width() - self.hostText.get_width())/2, self.hostScreen.get_height()/10))
        self.hostScreen.blit(self.hostText, textRect)

        textRect = textRect = ((self.hostScreen.get_width()/3, self.hostScreen.get_height()/4))
        self.hostScreen.blit(self.playersNumText, textRect)
        textRect = textRect = ((self.hostScreen.get_width()/3, self.hostScreen.get_height()/4+15))
        self.hostScreen.blit(self.gameNameText, textRect)
        textRect = textRect = ((self.hostScreen.get_width()/3, self.hostScreen.get_height()/4+30))
        self.hostScreen.blit(self.hostNameText, textRect)

        self.hostAttributes.draw()


    def lfgDraw(self):
        '''Screen for looking for a game only drawn if radio button 2 is selected'''
        
        self.lfgScreen.fill((255,255,255))
        textRect = (((self.lfgScreen.get_width() - self.lfgText.get_width())/2, self.lfgScreen.get_height()/10))
        self.lfgScreen.blit(self.lfgText, textRect)
        


    def localGameDraw(self):
        '''Screen for local game only drawn if radio button 3 is selected'''
        
        self.localScreen.fill((255,255,255))
        
        textRect = (((self.localScreen.get_width() - self.hostText.get_width())/2, self.localScreen.get_height()/10))
        self.localScreen.blit(self.hostText, textRect)

        textRect = textRect = ((self.localScreen.get_width()/3, self.localScreen.get_height()/4))
        self.localScreen.blit(self.playersNumText, textRect)

        self.localAttributes.draw()

    def enteringForm(self, event):
        CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789-=[];\'\\,./`'
        CHARSCAPS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ)!@#$%^&*(_+{}:"|<>?~'
        
        if event.key == K_ESCAPE:
            self.enterForm = False
        elif event.key == K_BACKSPACE:
            self.entBoxes[self.gameOpt].getFocused().deleteText()
        elif event.key <= 127 and event.key >= 32 and (self.entBoxes[self.gameOpt].getFocused().getMaxChar() == -1 or\
             len(self.entBoxes[self.gameOpt].getFocused().getText()) < self.entBoxes[self.gameOpt].getFocused().getMaxChar()): #Only accept regular ascii characters (ignoring certain special characters)
            checkCaps = pygame.key.get_pressed()
            if checkCaps[K_RSHIFT] or checkCaps[K_LSHIFT] and chr(event.key) in CHARS:
                index = CHARS.index(chr(event.key))
                currText = self.entBoxes[self.gameOpt].getFocused().getText()
                self.entBoxes[self.gameOpt].getFocused().setText(currText+CHARSCAPS[index])
            elif checkCaps[K_CAPSLOCK] and chr(event.key) in CHARS:
                index = CHARS.index(chr(event.key))
                if index < 26: #Only caps lock regular alphabet
                    currText = self.entBoxes[self.gameOpt].getFocused().getText()
                    self.entBoxes[self.gameOpt].getFocused().setText(currText+CHARSCAPS[index])
                else:
                    currText = self.entBoxes[self.gameOpt].getFocused().getText()
                    self.entBoxes[self.gameOpt].getFocused().setText(currText+chr(event.key))
            else:
                currText = self.entBoxes[self.gameOpt].getFocused().getText()
                self.entBoxes[self.gameOpt].getFocused().setText(currText+chr(event.key))



    
    def run(self):
        '''Draw lobby and handle lobby events'''
        CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789-=[];\'\\,./`'
        CHARSCAPS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ)!@#$%^&*(_+{}:"|<>?~'
        self.load(0)
        self.gameExit = False
        server = gameClient()
        result = cmdList.get()
        while not self.gameExit:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    self.buttonClick()
                if event.type == KEYDOWN:
                    if self.enterForm:
                        self.enteringForm(event)
                    if event.key == K_ESCAPE and not self.enterForm:
                        pygame.quit()
                        sys.exit()
                        break
            self.alwaysDraw()
            self.gameType[self.gameOpt]()
            self.parent.blit(self.screen, (0,0))
            pygame.display.update()
        #remove these when integrating
        return self.nextScreen  
            

        

    
