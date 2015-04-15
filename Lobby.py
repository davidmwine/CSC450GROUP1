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
from CheckBox import CheckBox


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
        self.offset1 = [self.width/10, self.height/3]
        self.lfgScreen = self.screen.subsurface(self.width/10, self.height/3,self.width*5/8, self.height*2/3-self.height/10)
        self.localScreen = self.screen.subsurface(self.width/10, self.height/3,self.width*8/10, self.height/3)
        self.offset3 = [self.width/10, self.height/3]
        
        #chat Box
        rect = pygame.Rect((1440*self.scale, 810*self.scale),
                           (480*self.scale, 270*self.scale))
        self.chatBox = ChatBox(self.scale, self.screen, rect)

        #Host form fields
        self.hostAttributes = EntryBoxSet(self.scale)
        boxRect = Rect(self.hostScreen.get_width()/3+200*self.scale, self.hostScreen.get_height()/4,40*self.scale,30*self.scale)
        self.hostAttributes.createNew(self.hostScreen,1 ,boxRect, self.font_op, self.offset1, '1')
        boxRect = Rect(self.hostScreen.get_width()/3+200*self.scale, self.hostScreen.get_height()/4+30*self.scale,40*self.scale,30*self.scale)
        self.hostAttributes.createNew(self.hostScreen,15, boxRect, self.font_op , self.offset1, "Mastering MSU")
        boxRect = Rect(self.hostScreen.get_width()/3+200*self.scale, self.hostScreen.get_height()/4+60*self.scale,40*self.scale,30*self.scale)
        self.hostAttributes.createNew(self.hostScreen,15 ,boxRect, self.font_op, self.offset1, "Player 1")

        #LFG form Fields
        self.lfgAttributes = EntryBoxSet(self.scale)

        #Local Form Fields
        self.localAttributes = EntryBoxSet(self.scale)
        currHeight = self.localScreen.get_height()/24
        boxRect = Rect(self.localScreen.get_width()/7, currHeight,50*self.scale,30*self.scale)
        self.localAttributes.newDropDown(self.localScreen, boxRect, self.font_op, self.scale, self.offset3, ['2', '3', '4', '5', '6'])
        #self.localAttributes.getBox('0').setMaxChar(1)
        for i in range(6):
            currHeight += self.localScreen.get_height()/7
            boxRect = Rect(self.localScreen.get_width()/7, currHeight,160*self.scale,30*self.scale)
            self.localAttributes.createNew(self.localScreen, 8,boxRect, self.font_op, self.offset3, 'Player ' + str(i+1))
            self.localAttributes.getBox(str(i+1)).setMaxChar(8)

        #Boxes for Dean Selection
        self.boxNum = 6
        currPos = [self.localScreen.get_width()/4 + self.localScreen.get_width()/20,\
                             self.localScreen.get_height()/4]
        width = self.localScreen.get_width()/4 - self.localScreen.get_width()/16
        height = self.localScreen.get_height()/4
        rect1 = Rect(currPos[0], currPos[1], width, height)
        currPos[0] += self.localScreen.get_width()/4
        rect2 = Rect(currPos[0], currPos[1], width, height)
        currPos[0] += self.localScreen.get_width()/4
        rect3 = Rect(currPos[0], currPos[1], width, height)
        currPos[0] = self.localScreen.get_width()/4 + self.localScreen.get_width()/20
        currPos[1] += self.localScreen.get_height()/2 - self.localScreen.get_height()/6
        rect4 = Rect(currPos[0], currPos[1], width, height)
        currPos[0] += self.localScreen.get_width()/4
        rect5 = Rect(currPos[0], currPos[1], width, height)
        currPos[0] += self.localScreen.get_width()/4
        rect6 = Rect(currPos[0], currPos[1], width, height)
        currPos[0] += self.localScreen.get_width()/4
        self.deanBoxes = DeanBoxes(self.localScreen, self.font_op, self.scale, self.offset3, width, height)
        default1 = 'Arts and Letters'
        default2 = 'Business'
        default3 = 'Education'
        default4 = 'Health and Human Services'
        default5 = 'Humanities and Public Affairs'
        default6 = 'Agriculture'
        self.deanBoxes.newBox(rect1, default1)
        self.deanBoxes.newBox(rect2, default2)
        self.deanBoxes.newBox(rect3, default3)
        self.deanBoxes.newBox(rect4, default4)
        self.deanBoxes.newBox(rect5, default5)
        self.deanBoxes.newBox(rect6, default6)

        #CheckBoxes for dean selection
        self.checkBoxes = []
        for i in range(6):
            rect = self.deanBoxes.getBox(i).getRect()
            x = rect.left - self.scale*60
            y = rect.top + rect.height/2 - self.scale*20
            w = self.scale*40
            self.checkBoxes.append(CheckBox(self.localScreen, x, y, w))
        
        #Render Text
        self.hostText = self.font_op(40*self.scale, 'berlin').render("Please select game attributes.",1,(0,0,0))
        self.lfgText = self.font_op(40*self.scale, 'berlin').render("Please select a game to join.",1,(0,0,0))
        self.CheckBoxText = self.font_op(40*self.scale, 'berlin').render("Click on Checkboxes to Select or Deselect Dean",1,(0,0,0))
        self.playersNumText = self.font_op(20*self.scale, 'berlin').render("Number of Players",1,(0,0,0))
        self.player1Text = self.font_op(20*self.scale, 'berlin').render("Player 1 Name",1,(0,0,0))
        self.player2Text = self.font_op(20*self.scale, 'berlin').render("Player 2 Name",1,(0,0,0))
        self.player3Text = self.font_op(20*self.scale, 'berlin').render("Player 3 Name",1,(0,0,0))
        self.player4Text = self.font_op(20*self.scale, 'berlin').render("Player 4 Name",1,(0,0,0))
        self.player5Text = self.font_op(20*self.scale, 'berlin').render("Player 5 Name",1,(0,0,0))
        self.player6Text = self.font_op(20*self.scale, 'berlin').render("Player 6 Name",1,(0,0,0))
        self.playerTextList = [self.player1Text, self.player2Text, self.player3Text, self.player4Text, self.player5Text, self.player6Text]
        self.gameNameText = self.font_op(20*self.scale, 'berlin').render("Name of Game",1,(0,0,0))
        self.hostNameText = self.font_op(20*self.scale, 'berlin').render("Name of Host",1,(0,0,0))

        #For changing entry box sets
        self.entBoxes = [self.hostAttributes, self.lfgAttributes, self.localAttributes]


        


    def buttonClick(self):
        '''determine what happens when the mouse is clicked'''
        #Takes action if a button is clicked
        mouseX, mouseY = pygame.mouse.get_pos()
        for i in range(len(self.checkBoxes)):
            if i <= self.boxNum: #If box is displayed check it
                if self.checkBoxes[i].setChecked(mouseX - self.offset3[0], mouseY - self.offset3[1]):
                    self.deanBoxes.lock(i)
                    currInd = self.deanBoxes.getBox(i).getCurrIndex()
                    currLock = self.deanBoxes.getBox(i).getIsLocked()
                    self.deanBoxes.updateLocks(currInd, currLock)
            #else:
                #currInd = self.deanBoxes.getBox(i).getCurrIndex()
                #currLock = not self.deanBoxes.getBox(i).getIsLocked()
                #self.deanBoxes.updateLocks(currInd, currLock)
                #self.deanBoxes.getBox(i).setLocks(self.deanBoxes.getBox(0).getLocks()) #Make sure undisplayed boxes have up to date locks
        for i in range(self.boxNum):
            self.deanBoxes.getBox(i).isClicked(mouseX - self.offset3[0], mouseY - self.offset3[1])
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
        if self.gameOpt == 2 and self.localAttributes.isClicked(mouseX, mouseY, '0'):
            if not self.localAttributes.getBox('0').hasFocus(): #If a drop down, has special interaction
                self.enterForm = True
        elif self.gameOpt == 1 and self.lfgAttributes.isClicked(mouseX, mouseY):
            self.enterForm = True
        elif self.gameOpt == 0 and self.hostAttributes.isClicked(mouseX, mouseY):
            self.enterForm = True
        else:
            self.enterForm = False

    def checkMousePos(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        self.localAttributes.getBox('0').setIfHovered(mouseX - self.offset3[0], mouseY - self.offset3[1])
        
            
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
        
        textRect = (((self.localScreen.get_width() - (6*self.CheckBoxText.get_width()/5)), self.localScreen.get_height()/24))
        self.localScreen.blit(self.CheckBoxText, textRect)

        textRect = ((self.localScreen.get_width()/100, self.localScreen.get_height()/24))
        self.localScreen.blit(self.playersNumText, textRect)

        self.boxNum = int(self.localAttributes.getBox('0').getText())
        self.deanBoxes.drawBoxes(self.boxNum)
        for i in range(self.boxNum): #Display only boxes for number of players
            textRect = ((self.localScreen.get_width()/100, self.localScreen.get_height()/24 + (i+1)*self.localScreen.get_height()/7))
            self.localScreen.blit(self.playerTextList[i], textRect)
            self.checkBoxes[i].draw()
        if self.boxNum < 6:
            for i in range (self.boxNum, 6):
                self.checkBoxes[i].undoChecked()
                self.deanBoxes.unlock(i)
                self.localAttributes.getBox(str(i+1)).setText("Player " + str(i+1))
                currInd = self.deanBoxes.getBox(i).getCurrIndex()
                currLock = self.deanBoxes.getBox(i).getIsLocked()
                self.deanBoxes.updateLocks(currInd, currLock)
        self.localAttributes.draw(self.boxNum+1, '0')

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
        #server = gameClient()
        #result = cmdList.get()
        pygame.key.set_repeat(75, 75)
        while not self.gameExit:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    self.buttonClick()
                if event.type == KEYDOWN:
                    if self.enterForm:
                        self.enteringForm(event)
                    if event.key == K_ESCAPE and not self.enterForm:
                        return "start"
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    return 0
            self.checkMousePos()
            self.alwaysDraw()
            self.gameType[self.gameOpt]()
            self.parent.blit(self.screen, (0,0))
            pygame.display.update()
        #remove these when integrating
        return self.nextScreen  
            

        

    
