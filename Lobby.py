import pygame, sys, os
from pygame.locals import *
from Player import Player
import Colors
from ChatBoxCopy import ChatBox
from RadioButton import RadioGroup
from Controls import Button
from TextWrap import *
from EntryBox import EntryBoxSet
from Client import *
from DeanBox import *


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



        #booleans
        self.enterForm = False

        #return on exit
        self.nextScreen = ''


    def load(self, gameOpt):
        '''Loads the images and text needed for the base screen to draw on takes game option code
to determine the inital screen'''
        self.bg = pygame.image.load(os.path.join("img","menu_bg4.png"))

  


        #Start Game button
        buttonRect= Rect(0 , self.height -80*self.scale, 300*self.scale, 80*self.scale)
        self.startButton = Button(self.screen, buttonRect, "Start Game")
        buttonRect= Rect(300*self.scale , self.height -80*self.scale, 300*self.scale, 80*self.scale)
        self.backButton = Button(self.screen, buttonRect, "Back")
        buttonRect= Rect(600*self.scale , self.height -80*self.scale, 300*self.scale, 80*self.scale)
        self.optButton = Button(self.screen, buttonRect, "Options")
        
        #init screen
        self.localScreen = self.screen.subsurface(self.width/10, self.height/3,self.width*8/10, self.height/3)
        offset3 = [self.width/10, self.height/3]
        
        #chat Box
        rect = pygame.Rect((1440*self.scale, 810*self.scale),
                           (480*self.scale, 270*self.scale))
        self.chatBox = ChatBox(self.scale, self.screen, rect)

        #Local Form Fields
        self.localAttributes = EntryBoxSet(self.scale)
        boxRect = Rect(self.localScreen.get_width()/3+200*self.scale, self.localScreen.get_height()/4,40*self.scale,30*self.scale)
        self.localAttributes.createNew(self.localScreen,1 ,boxRect, self.font_op, offset3, '6')
        self.localAttributes.getBox('0').setMaxChar(1)

        #Boxes for Dean Selection
        self.deanBoxes = DeanBoxes(self.localScreen, self.font_op, self.scale, offset3)
        self.deanBoxes.newBox()
        self.deanBoxes.newBox()
        self.deanBoxes.newBox()
        self.deanBoxes.newBox()
        self.deanBoxes.newBox()
        self.deanBoxes.newBox()
        
        #Render Text
    
        self.playersNumText = self.font_op(20*self.scale, 'berlin').render("Number of Players",1,(0,0,0))
        self.localText = self.font_op(40*self.scale, 'berlin').render("Please select game attributes.",1,(0,0,0))
        self.hostNameText = self.font_op(20*self.scale, 'berlin').render("Name of Host",1,(0,0,0))

        


        


    def buttonClick(self):
        '''determine what happens when the mouse is clicked'''
        #Takes action if a button is clicked
        mouseX, mouseY = pygame.mouse.get_pos() 
        if self.startButton.wasClicked(mouseX, mouseY):
            self.gameExit = True
            self.nextScreen = 'game'
            self.setFlags()
            return
        if self.backButton.wasClicked(mouseX, mouseY):
            self.gameExit = True
            self.nextScreen = 'start'
            return
        if self.localAttributes.isClicked(mouseX, mouseY):
            self.enterForm = True
        else:
            self.enterForm = False
            
    def alwaysDraw(self):
        '''Screen that is always drawn no matter which radio button is selected should be run before other draw functions'''

        #draws background and radio buttons
        self.screen.blit(self.bg, (0,0))
        self.startButton.redraw()
        self.backButton.redraw()
        self.optButton.redraw()
        self.chatBox.redraw()
        
        
        


   
        '''Screen for local game only drawn if radio button 3 is selected'''
        
        self.localScreen.fill((255,255,255))
        
        textRect = (((self.localScreen.get_width() - self.localText.get_width())/2, self.localScreen.get_height()/10))
        self.localScreen.blit(self.localText, textRect)

        textRect = textRect = ((self.localScreen.get_width()/3, self.localScreen.get_height()/4))
        self.localScreen.blit(self.playersNumText, textRect)

        self.localAttributes.draw()
        self.deanBoxes.drawBoxes()

    def enteringForm(self, event):
        CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789-=[];\'\\,./`'
        CHARSCAPS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ)!@#$%^&*(_+{}:"|<>?~'
        focusedBox = self.localAttributes.getFocused()
        if event.key == K_ESCAPE:
            self.enterForm = False
        elif event.key == K_BACKSPACE:
            focusedBox.deleteText()
        elif event.key <= 127 and event.key >= 32 and (focusedBox.getMaxChar() == -1 or\
             len(focusedBox.getText()) < focusedBox.getMaxChar()): #Only accept regular ascii characters (ignoring certain special characters)
            checkCaps = pygame.key.get_pressed()
            if checkCaps[K_RSHIFT] or checkCaps[K_LSHIFT] and chr(event.key) in CHARS:
                index = CHARS.index(chr(event.key))
                currText = focusedBox.getText()
                focusedBox.setText(currText+CHARSCAPS[index])
            elif checkCaps[K_CAPSLOCK] and chr(event.key) in CHARS:
                index = CHARS.index(chr(event.key))
                if index < 26: #Only caps lock regular alphabet
                    currText = focusedBox.getText()
                    focusedBox.setText(currText+CHARSCAPS[index])
                else:
                    currText = focusedBox.getText()
                    focusedBox.setText(currText+chr(event.key))
            else:
                currText = focusedBox.getText()
                focusedBox.setText(currText+chr(event.key))

    def setFlags(self):
        File = open('FlagFile.txt', 'w')
        File.write("Players:"+self.localAttributes.getBox('0').getText())
        File.close()
    
    def run(self):
        '''Draw lobby and handle lobby events'''
        CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789-=[];\'\\,./`'
        CHARSCAPS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ)!@#$%^&*(_+{}:"|<>?~'
        self.load(0)
        self.gameExit = False
        #server = gameClient()
        #result = cmdList.get()
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
            self.parent.blit(self.screen, (0,0))
            pygame.display.update()
        #remove these when integrating
        return self.nextScreen  
            

        

    
