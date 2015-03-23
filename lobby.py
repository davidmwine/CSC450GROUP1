import pygame, sys, os
from pygame.locals import *
from player import Player
import Colors
from ChatBox import ChatBox
from RadioButton import RadioGroup
from Controls import Button
from textWrap import *
from EntryBox import EntryBoxSet


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
        buttonRect= Rect(0 , self.height -40, 150, 40)
        self.startButton = Button(self.screen, buttonRect, "Start Game")

        #init screens
        self.hostScreen = self.screen.subsurface(self.width/10, self.height/3,self.width*8/10, self.height/3)
        self.lfgScreen = self.screen.subsurface(self.width/10, self.height/3,self.width*2/3, self.height*2/3-self.height/10)
        self.localScreen = self.screen.subsurface(self.width/10, self.height/3,self.width*8/10, self.height/3)
        
        #chat Box
        rect = pygame.Rect((1440*self.scale, 810*self.scale),
                           (480*self.scale, 270*self.scale))
        self.chatBox = ChatBox(self.scale, self.screen, rect)

        #form fields
        self.hostAttributes = EntryBoxSet()
        boxRect = Rect(self.hostScreen.get_width()/3-10, self.hostScreen.get_height()/4,20,15)
        self.hostAttributes.createNew(self.hostScreen,1 ,boxRect, self.font_op ,'1')
        boxRect = Rect(self.hostScreen.get_width()/3-10, self.hostScreen.get_height()/4+15,20,15)
        self.hostAttributes.createNew(self.hostScreen,15, boxRect, self.font_op ,"Mastering MSU")
        boxRect = Rect(self.hostScreen.get_width()/3-10, self.hostScreen.get_height()/4+30,20,15)
        self.hostAttributes.createNew(self.hostScreen,15 ,boxRect, self.font_op ,"Player 1")
        self.lfgAttributes = EntryBoxSet()
        self.localAttributes = EntryBoxSet()

        
        #Render Text
        self.hostText = self.font_op(20, 'berlin').render("Please select game attributes.",1,(0,0,0))
        self.lfgText = self.font_op(20, 'berlin').render("Please select a game to join.",1,(0,0,0))
        self.playersNumText = self.font_op(10, 'berlin').render("Number of Players",1,(0,0,0))
        self.gameNameText = self.font_op(10, 'berlin').render("Name of Game",1,(0,0,0))
        self.hostNameText = self.font_op(10, 'berlin').render("Name of Host",1,(0,0,0))


        


    def buttonClick(self):
        '''determine what happens when the mouse is clicked'''
        #Takes action if a button is clicked
        mouseX, mouseY = pygame.mouse.get_pos()
        if self.gameTypeRadio.checkButton(mouseX, mouseY):
            self.gameOpt = self.gameTypeRadio.getCurrent()
        if self.startButton.wasClicked(mouseX, mouseY):
            self.gameExit = True
            self.nextScreen = 'Start'
            
    def alwaysDraw(self):
        '''Screen that is always drawn no matter which radio button is selected should be run before other draw functions'''

        #draws background and radio buttons
        self.screen.blit(self.bg, (0,0))
        for i in range(len(self.text_list)):
            self.screen.blit(self.text_list[i], (self.width_less_radio/2 +20*(i+1) + sum(self.width_list[:i]),
                                                 self.height/8,self.width_list[i],self.text_list[i].get_height()))
        self.gameTypeRadio.draw()
        self.startButton.redraw()
        
        
        


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
        


    
    def run(self):
        '''Draw lobby and handle lobby events'''
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
            self.gameType[self.gameOpt]()
            self.parent.blit(self.screen, (0,0))
            pygame.display.update()
        return self.nextScreen  
            

        

    
