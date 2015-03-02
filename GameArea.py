import pygame, sys
from pygame.locals import *
from player import Player
from buildings import Buildings
from globals import Globals
from playersDisplay import PlayersDisplay
from board import GameBoard
from Controls import Controls
from ChatBox import chatBox
from Dice import Dice
from textWrap import *


class GameArea(object):


    def __init__(self, parent=False, scale=1):

        self.width = int(scale*1920)
        self.height = int(scale*1080)
        self.scale = scale
        self.parent = parent
        self.clock = pygame.time.Clock()
        self.roll = (0,0)   # self.roll[1] is the value of the roll
        self.roll_time = 501
        
        self.sequence = self.turnSequence()
        self.players = []       # List of players will be added in play()
        self.buildings = None   # List of buildings will be added in play()
        self.player = None      # Holds player whose turn it is
        self.building = None    # Holds building space that was landed on
                
        self.typing = False     # True if user is typing in chat box
        self.midTurn = False    # True if it's the middle of a player's turn
        self.rollingDice = False
        self.buyMsgDisplayed = False
        self.okMsgDisplayed = False     # True if any OK message is displayed
        self.clickedButton = False      # True if OK or Yes or No has been clicked
        self.gameExit = False
        self.typing = False
        self.roll = (0,0)
        self.roll_time = 501
        if self.parent:
            self.area = pygame.Surface((self.width, self.height))
        else:
            pygame.init()
            self.area = pygame.display.set_mode((self.width, self.height))

        self.font = pygame.font.Font(None, int(50*self.scale))    
        
        # Game Board Area
        rect = pygame.Rect((0, 0), (1440*self.scale, 1020*self.scale))
        self.boardArea = self.area.subsurface(rect)
        self.boardArea.fill(Globals.maroon) 
        
        # Chat Box
        rect = pygame.Rect((1440*self.scale, 810*self.scale),
                           (480*self.scale, 270*self.scale))
        self.chatbox = chatBox(self.scale,self.area, rect)
        
        # Controls
        rect = pygame.Rect((0, 1020*self.scale),
                           (1440*self.scale, 60*self.scale))
        self.controls = Controls(self.area, rect)

        #Dice
        self.dice = Dice(self.boardArea)


    def getArea(self):
        return self.area


    def getScale(self):
        return self.scale

    def mouseClick(self):
        mouseX,mouseY = pygame.mouse.get_pos()
        if mouseX > self.controls.get_width()/4\
        and mouseX < self.controls.get_width()/2\
        and mouseY > self.height-self.controls.get_height():
            self.roll = (1,0)
        if mouseX > self.chatbox.getLeft() and mouseX < self.chatbox.getRight()\
           and mouseY > self.chatbox.getTopType()\
           and mouseY < self.chatbox.getBottomType():
            self.typing = True
        
        

    def refreshGameBoard(self):
        rect = pygame.Rect((20*self.scale, 20*self.scale),
                           (1400*self.scale, 980*self.scale))
        self.area.blit(self.gameBoard.getGB(), rect)

    def refreshPlayersDisplay(self):
        rect = pygame.Rect((1440*self.scale, 0),
                           (480*self.scale, 810*self.scale))
        self.area.blit(self.playersDisplay.getPD(), rect)
        

    def refreshDisplay(self):
        if self.parent:    
            self.parent.blit(self.area, (0,0))
        pygame.display.update()


    def mouseClick(self):
        """Takes action based on when and where mouse has been clicked"""
        mouseX,mouseY = pygame.mouse.get_pos()
        if mouseX > self.controls.get_width()/4\
        and mouseX < self.controls.get_width()/2\
        and mouseY > self.height-self.controls.get_height():
            self.roll = (1,0)
            self.area.blit(self.gameBoard.getGB(),
                               (20*self.scale, 20*self.scale))  # redraw board
            self.rollingDice = True     # triggers self.rollDice()
            
        if mouseX > self.chatbox.getLeft() and mouseX < self.chatbox.getRight()\
           and mouseY > self.chatbox.getTopType()\
           and mouseY < self.chatbox.getBottomType():
            self.typing = True

        if self.okMsgDisplayed:
            okRect = pygame.Rect(self.msgRect.x + self.okRect.x,
                                 self.msgRect.y + self.okRect.y,
                                 self.okRect.width, self.okRect.height)
            if okRect.collidepoint(pygame.mouse.get_pos()):
                self.okMsgDisplayed = False
                self.clickedButton = True
                self.area.blit(self.gameBoard.getGB(),
                               (20*self.scale, 20*self.scale))  # redraw board

        if self.buyMsgDisplayed:
            yesRect = pygame.Rect(self.msgRect.x + self.yesRect.x,
                                 self.msgRect.y + self.yesRect.y,
                                 self.yesRect.width, self.yesRect.height)
            noRect = pygame.Rect(self.msgRect.x + self.noRect.x,
                                 self.msgRect.y + self.noRect.y,
                                 self.noRect.width, self.noRect.height)
            if yesRect.collidepoint(pygame.mouse.get_pos()):
                self.buy()
                self.buyMsgDisplayed = False
                self.clickedButton = True
                self.area.blit(self.gameBoard.getGB(),
                               (20*self.scale, 20*self.scale))  # redraw board
            elif noRect.collidepoint(pygame.mouse.get_pos()):
                self.buyMsgDisplayed = False
                self.clickedButton = True
                self.area.blit(self.gameBoard.getGB(),
                               (20*self.scale, 20*self.scale))  # redraw board



    def turnSequence(self):
        """A generator for the sequence of events during a player's turn."""
        yield self.beginTurn()
        yield self.rollDice()
        yield self.moveToken()
        yield self.handleLanding()


    def beginTurn(self):
        print("------- " + self.player.getName() + "'s turn -------")
        self.displayMsg(self.player.getName() + "'s turn. Click 'Roll'")
        # Wait for user to click the Roll Dice button
        while not self.rollingDice:
            event = pygame.event.wait()
            if event.type == MOUSEBUTTONDOWN:
                self.mouseClick()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()    


    def rollDice(self):
        while self.roll[0]>0:
            self.clock.tick(30)
            self.roll_time += self.clock.get_time()
            if self.roll_time>250:
                self.roll = self.dice.roll()
                self.roll_time = 0
                self.refreshDisplay()
        print("Dice Rolled:", self.roll[1])
        self.rollingDice = False


    def moveToken(self):
        pygame.time.wait(1000)
        self.player.increasePosition(self.roll[1])
        position = self.player.getPosition()
        self.building = self.buildings[position]
        print("Token landed on", self.building.getName())


    def handleLanding(self):
        """
        This method handles what comes next after a player lands on a space,
        (e.g., buying the building or paying fees to another player)
        """
        if self.building.getPurpose() == "special":
            self.displayMsgOK("Special message about " + self.building.getName())
            self.okMsgDisplayed = True
        else:    
            owner = self.building.getOwner()
            if owner == self.player:
                self.displayMsgOK("You already own " + self.building.getName() + ".")
                self.okMsgDisplayed = True
            elif owner == None:
                choice = self.displayBuyChoice()  
            elif owner != self.player:
                self.chargeFees(owner)

        self.refreshDisplay()        
                
        # Wait for user to click a button.
        while not self.clickedButton:
            event = pygame.event.wait()
            if event.type == MOUSEBUTTONDOWN:
                self.mouseClick()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        print("End of turn")
        self.clickedButton = False
        self.midTurn = False
        self.refreshPlayersDisplay()
        self.refreshGameBoard()


    def displayMsg(self, msg):
        """Displays msg in the center of the game board."""        
        # Create message box as a surface and display text.
        msgBox = pygame.Surface((560*self.scale, 392*self.scale))
        msgBox.fill(Globals.lightGray)
        lines = wrapline(msg, self.font, 440*self.scale)
        i = 0
        for line in lines:
            lineYpos = 50*i*self.scale + 2
            line = self.font.render(line, True, Color("black"))
            msgBox.blit(line, (2, lineYpos))
            i += 1

        # Position message box on the screen.
        self.msgRect = pygame.Rect(440*self.scale, 314*self.scale,
                        560*self.scale, 392*self.scale)
        self.area.blit(msgBox, self.msgRect)
        self.refreshDisplay()


    def displayMsgYN(self, msg):
        """Displays msg with Yes and No buttons in the center of the game board."""        
        # Create message box as a surface and display text.
        msgBox = pygame.Surface((560*self.scale, 392*self.scale))
        msgBox.fill(Globals.lightGray)
        lines = wrapline(msg, self.font, 440*self.scale)
        i = 0
        for line in lines:
            lineYpos = 50*i*self.scale + 2
            line = self.font.render(line, True, Color("black"))
            msgBox.blit(line, (2, lineYpos))
            i += 1
    
        # Create and position Yes and No buttons.
        yesButton = pygame.Surface((100*self.scale, 50*self.scale))
        yesButton.fill(Globals.medGray)
        self.yesRect = yesButton.get_rect()
        text = self.font.render("Yes", True, Color("black"))
        textPos = text.get_rect()
        textPos.center = self.yesRect.center
        yesButton.blit(text, textPos)
        self.yesRect.bottom = msgBox.get_rect().height - 10
        self.yesRect.left = 125*self.scale
        msgBox.blit(yesButton, self.yesRect)

        noButton = pygame.Surface((100*self.scale, 50*self.scale))
        noButton.fill(Globals.medGray)
        self.noRect = noButton.get_rect()
        text = self.font.render("No", True, Color("black"))
        textPos = text.get_rect()
        textPos.center = self.noRect.center
        noButton.blit(text, textPos)
        self.noRect.bottom = msgBox.get_rect().height - 10
        self.noRect.right = msgBox.get_rect().width - 125*self.scale
        msgBox.blit(noButton, self.noRect)
        
        # Position message box on the screen.
        self.msgRect = pygame.Rect(440*self.scale, 314*self.scale,
                        560*self.scale, 392*self.scale)
        self.area.blit(msgBox, self.msgRect)
        
     
    def displayMsgOK(self, msg):
        """Displays msg with OK button in the center of the game board."""        
        # Create message box as a surface and display text.
        msgBox = pygame.Surface((560*self.scale, 392*self.scale))
        msgBox.fill(Globals.lightGray)
        lines = wrapline(msg, self.font, 440*self.scale)
        i = 0
        for line in lines:
            lineYpos = 50*i*self.scale + 2
            line = self.font.render(line, True, Color("black"))
            msgBox.blit(line, (2, lineYpos))
            i += 1

        # Create and position OK button.
        okButton = pygame.Surface((100*self.scale, 50*self.scale))
        self.okRect = okButton.get_rect()
        okButton.fill(Globals.medGray)
        text = self.font.render("OK", True, Color("black"))
        textPos = text.get_rect()
        textPos.center = self.okRect.center
        okButton.blit(text, textPos)
        self.okRect.bottom = msgBox.get_rect().height - 10
        self.okRect.centerx = msgBox.get_rect().centerx
        msgBox.blit(okButton, self.okRect)
        
        # Position message box on the screen.
        self.msgRect = pygame.Rect(440*self.scale, 314*self.scale,
                        560*self.scale, 392*self.scale)
        self.area.blit(msgBox, self.msgRect)    


    def displayBuyChoice(self):
        """Gives player the choice whether to buy the building he/she landed on"""
        self.buyMsgDisplayed = True
        self.displayMsgYN("Do you want to buy " + self.building.getName() + "?")


    def buy(self):
        """Takes care of bookkeeping once player clicked Yes to buy building"""
        self.player.subtractDollars(self.building.getPrice())
        self.player.addBuilding(self.building)
        self.building.setOwner(self.player)
        self.building.setColor(self.player.getColor())
        self.gameBoard.colorBuilding(self.building)


    def chargeFees(self, owner):
        """If building is already owned, fees are paid to owner."""
        self.okMsgDisplayed = True
        feeAmt = self.building.getFeeAmount()
        self.player.subtractDollars(feeAmt)
        owner.addDollars(feeAmt)
        self.displayMsgOK("You pay $" + str(feeAmt) + " to " + owner.getName() + ".")
        # Update owner's dollars in playersDisplay.
        self.playersDisplay.unselectPlayer(self.players.index(owner))

    def chatting(self, event):
        if event.key == K_ESCAPE:
            self.typing = False
        elif event.key == K_RETURN:
            self.chatbox.submitText()
        elif event.key == K_BACKSPACE:
            self.chatbox.deleteText()
        elif event.key <= 127 and event.key >= 32: #Only accept regular ascii characters (ignoring certain special characters)
            #self.chatbox.typeText(pygame.key.name(event.key))
            #self.chatbox.typeText(chr(event.key))
            checkCaps = pygame.key.get_pressed()
            if checkCaps[K_RSHIFT] or checkCaps[K_LSHIFT] and chr(event.key) in self.chars:
                index = self.chars.index(chr(event.key))
                if self.charsCaps[index] not in ['{', '}']:
                    self.chatbox.typeText(self.charsCaps[index])
                else:
                    self.chatbox.typeText(self.charsCaps[index] + self.charsCaps[index])
            elif checkCaps[K_CAPSLOCK]:
                index = self.chars.index(chr(event.key))
                if index < 26: #Only caps lock regular alphabet
                    self.chatbox.typeText(self.charsCaps[index])
                else:
                    self.chatbox.typeText(chr(event.key))
            else:
                self.chatbox.typeText(chr(event.key))

    def play(self):

        # This data will eventually be obtained from the lobby / setup menu.
        p1 = Player("player1", "Agriculture")
        p2 = Player("player2", "Arts and Letters")
        p3 = Player("player3", "Natural and Applied Sciences")
        p4 = Player("player4", "Education")
        p5 = Player("player5", "Health and Human Services")
        p6 = Player("player6", "Humanities and Public Affairs")

        self.players = [p1, p2, p3, p4, p5, p6]

        # Players Display
        self.playersDisplay = PlayersDisplay(self.players, self.scale, True)
        self.refreshPlayersDisplay()
        self.refreshDisplay()

        self.buildings = Buildings().getBuildingList()

        # Game Board
        self.gameBoard = GameBoard(self.scale, self.buildings, True)
        self.refreshGameBoard()
        self.refreshDisplay()

        #turn = -1   # This will be incremented to reference player 0.
        self.gameExit = False #Must be reset each time play is
        self.chars = 'abcdefghijklmnopqrstuvwxyz0123456789-=[];\'\\,./`'
        self.charsCaps = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ)!@#$%^&*(_+{}:"|<>?~'
        pygame.key.set_repeat(75, 75)
        while not self.gameExit:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    self.mouseClick()
                if event.type == KEYDOWN and not self.typing: #TEMPORARY, will later replace with proper game exit
                    if event.key == K_ESCAPE:
                        self.gameExit = True
                        break
                if event.type == KEYDOWN and self.typing:
                    self.chatting(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    return 0
            '''if not self.midTurn:    # If it's a new player's turn...
                self.playersDisplay.unselectPlayer(turn % len(self.players))
                turn += 1
                playerIndex = turn % len(self.players)
                self.player = self.players[playerIndex]
                self.playersDisplay.selectPlayer(playerIndex)
                self.refreshPlayersDisplay()
                self.refreshDisplay()
                self.sequence = self.turnSequence()
                self.midTurn = True
            self.roll_time += self.clock.get_time()
            if self.roll[0] and self.roll_time>250:
                self.roll = self.dice.roll()
                self.roll_time = 0
            if self.parent:
                self.parent.blit(self.area, (0,0))'''
            pygame.display.update()
            #next(self.sequence)     # Perform next action in player's turn       
            self.refreshDisplay()
            
        return "start"
        


def main():
    screen = GameArea(False, 0.6)
    screen.play()



if __name__ == "__main__":
    main()








        
        
            
