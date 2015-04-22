import pygame
from pygame.locals import *
import os
import sys
from Player import Player
from Building import Buildings
import Colors
import GameInfo
from PlayersDisplay import PlayersDisplay
from Board import GameBoard
from Controls import Controls
from ChatBox import ChatBox
from Dice import Dice
from PopupMenu import PopupMenu
from Cards import Cards
from Turn import Turn
from MessageBox import displayMsg


class GameArea(object):


    def __init__(self, screenInfo, parent=False, scale=1):
        """Overall function for the Game Area Screen.  Takes a parent surface
        and scale as optional paramaters.  If no parent is passed this will be
        the pygame screen, else it drawn on the main screen.  Scale defaults to
        one, and must be one or less and scales the screen accordingly where 1
        is a 1920x1080 screen.
        """

        self.parent = parent
        self.scale = scale
        self.width = int(self.scale*1920)
        self.height = int(self.scale*1080)
        self.infoScreen = screenInfo #For making fullscreen if fullscreen resolution
        
        self.clock = pygame.time.Clock()
        self.playerIndex = 0
        self.roll = (0,0,0)   # self.roll[1] and self.roll[2] are the numbers on the dice
        self.rollTime = 500 #Interval between dice roll updates in mS
        
        self.players = []       # List of players will be added in play()
        self.buildings = None   # List of buildings will be added in play()
        self.player = None      # Holds player whose turn it is
        self.building = None    # Holds building space that was landed on
                
        self.typing = False     # True if user is typing in chat box
        self.midTurn = False    # True if it's the middle of a player's turn
        self.gameExit = False
        self.cardDraw = False   # for demo; game uses self.turn.cardDraw
        self.cardDisplayed = False  # True if a card is face up
        self.diceRolled = False
        self.midRoll = False

        self.roundsBeforePriceIncrease = 3      # inflation

        self.rulesPage = 1 #initialize rules page to start at 1
        
        if self.parent:
            self.area = pygame.Surface((self.width, self.height))
        else:
            pygame.init()
            self.area = pygame.display.set_mode((self.width, self.height))

        self.font = pygame.font.Font(None, int(50*self.scale))

        self.initializeDisplay()


    def initializeDisplay(self):    
        # Game Board Area
        rect = pygame.Rect((0, 0), (1440*self.scale, 1020*self.scale))
        self.boardArea = self.area.subsurface(rect)
        self.boardArea.fill(Colors.MAROON) 
        
        # Chat Box
        rect = pygame.Rect((1440*self.scale, 810*self.scale),
                           (480*self.scale, 270*self.scale))
        self.chatBox = ChatBox(self.scale,self.area, rect)
        
        # Controls
        rect = pygame.Rect((0, 1020*self.scale),
                           (1440*self.scale, 60*self.scale))
        self.controls = Controls(self.area, rect)

        # Dice
        self.dice = Dice(self.boardArea)

        # Popup options menu
        self.popupMenu = PopupMenu(self.boardArea)

        # Cards
        self.cards = Cards(self.boardArea)

        # Message Rectangle
        self.msgRect = pygame.Rect(440*self.scale, 314*self.scale,
                                   560*self.scale, 392*self.scale)
        


    def getArea(self):
        return self.area


    def getScale(self):
        return self.scale


    def mouseClick(self, event):
        """Takes action based on when and where mouse has been clicked"""

        mouseX, mouseY = pygame.mouse.get_pos()
        #print(mouseX, mouseY)

        # menu not open
        if not self.popupMenu.getPopupActive():             
            #chatBox
            if mouseX > self.chatBox.getLeft() and mouseX < self.chatBox.getRight()\
            and mouseY > self.chatBox.getTopType()\
            and mouseY < self.chatBox.getBottomType():
                self.typing = True
            else:
                self.typing = False

            #Scrolling in chatBox
            if mouseX > self.chatBox.getLeft() and mouseX < self.chatBox.getRight()\
            and mouseY < self.chatBox.getTopType() and mouseY > self.chatBox.getTop():
                if event.button == 4:
                    self.chatBox.displayText(-1)
                elif event.button == 5:
                    self.chatBox.displayText(1)

            # Menu Button
            if mouseX > 0 and mouseX < self.controls.getWidth() / 4 \
            and mouseY > self.height - self.controls.getHeight():
                self.popupMenu.setPopupActive(True)
                self.popupMenu.makePopupMenu()

            # Roll Button
            if self.turn.ableToRoll and mouseX > self.controls.getWidth()/4\
            and mouseX < self.controls.getWidth()/2\
            and mouseY > self.height-self.controls.getHeight():
                # Update player's $ before they have to make a decision.
                self.playersDisplay.selectPlayer(self.playerIndex)
                self.refreshPlayersDisplay()
                self.roll = (1,0)
                self.diceRolled = True
                self.turn.ableToRoll = False
                self.rollDice()

            # Trade Button
            if mouseX > self.controls.getWidth() / 2 \
            and mouseX < 3 * self.controls.getWidth() / 4 \
            and mouseY > self.height - self.controls.getHeight():
                pass

            # Upgrade Button
            if mouseX > 3 * self.controls.getWidth() / 4 \
            and mouseX < self.controls.getWidth() \
            and mouseY > self.height - self.controls.getHeight():    
                self.turn.showUpgradeOptions()

            # Cards
            if (mouseX > self.cards.getXPosition()
            and mouseX < self.cards.getXPosition() + self.cards.getWidth()
            and mouseY > self.cards.getYPosition()
            and mouseY < self.cards.getYPosition() + self.cards.getHeight()):
                if self.turn.cardDraw:  # player landed on card space
                    self.turn.cardDraw = False
                    self.cardDisplayed = True
                    self.currentCard = self.cards.drawCard(self.scale)
                    (size, msgBox) = displayMsg(Turn.scale, Turn.smallMsgRect,
                        Turn.msgRect, Turn.font, "Click cards again to end turn.")
                    Turn.smallMsgSurface.blit(msgBox, (0, 0))
                    self.turn.cardLandingMsgDisplayed = False
                elif self.cardDisplayed:    # card is face up
                    self.cardDisplayed = False
                    self.endTurn()

            # Dice
            if (self.turn.ableToRoll and not self.turn.upgradeDisplayed
            and mouseX > self.dice.getXPosition()
            and mouseX < self.dice.getXPosition() + self.dice.getWidth()
            and mouseY > self.dice.getYPosition()
            and mouseY < self.dice.getYPosition() + self.dice.getHeight()):
                # Update player's $ before they have to make a decision.
                self.playersDisplay.selectPlayer(self.playerIndex)
                self.refreshPlayersDisplay()
                self.roll = (1,0)
                self.diceRolled = True
                self.turn.ableToRoll = False
                self.rollDice()
    
            # OK Button in Message Box
            if self.turn.okMsgDisplayed:
                okRect = pygame.Rect(Turn.msgRect.x + self.turn.okRect.x,
                                 Turn.msgRect.y + self.turn.okRect.y,
                                 self.turn.okRect.width, self.turn.okRect.height)
                if okRect.collidepoint(pygame.mouse.get_pos()):
                    # If applicable, charge fees and update playersDisplay.
                    if self.turn.feeMsgDisplayed:
                        self.turn.chargeFees()
                        if self.turn.owner != None:
                            self.playersDisplay.updatePlayer(
                                self.players.index(self.turn.owner))
                        self.turn.feeMsgDisplayed = False
                    self.turn.okMsgDisplayed = False    
                    self.endTurn()

            # Yes/No Button in Message Box
            if self.turn.buyMsgDisplayed:
                yesRect = pygame.Rect(Turn.msgRect.x + self.turn.yesRect.x,
                                     Turn.msgRect.y + self.turn.yesRect.y,
                                     self.turn.yesRect.width, self.turn.yesRect.height)
                noRect = pygame.Rect(Turn.msgRect.x + self.turn.noRect.x,
                                     Turn.msgRect.y + self.turn.noRect.y,
                                     self.turn.noRect.width, self.turn.noRect.height)
                if yesRect.collidepoint(pygame.mouse.get_pos()):
                    if self.turn.building.getPurpose() == "stealable":
                        self.turn.steal()
                    else:    
                        self.turn.buy()
                    self.gameBoard.colorBuilding(self.turn.building)
                    self.turn.buyMsgDisplayed = False
                    self.endTurn()
                elif noRect.collidepoint(pygame.mouse.get_pos()):
                    self.turn.buyMsgDisplayed = False
                    self.endTurn()

            # Upgrade Message Box (checkboxes and OK button)
            if self.turn.upgradeDisplayed:
                # Make checkboxes look checked when clicked.
                self.turn.checkUpgrades(mouseX, mouseY)
                
                okUpgradeRect = pygame.Rect(Turn.upgradeRect.x + self.turn.okUpgradeRect.x,
                                 Turn.upgradeRect.y + self.turn.okUpgradeRect.y,
                                 self.turn.okUpgradeRect.width, self.turn.okUpgradeRect.height)
                if okUpgradeRect.collidepoint(pygame.mouse.get_pos()):
                    # Once the player clicks OK, complete desired upgrades and update display.
                    self.turn.upgrade()
                    self.playersDisplay.selectPlayer(Turn.count % len(self.players))
                    self.refreshPlayersDisplay()
                    self.turn.upgradeDisplayed = False
                    self.resumeTurn()
                                        

        # menu open
        else:
            if not self.popupMenu.getOptionsActive():
                if not self.popupMenu.getExitCheckActive():
                    if not self.popupMenu.getRulesActive():
                        # resume game
                        if mouseX > self.boardArea.get_width() / 2 - 100 \
                        and mouseX < self.boardArea.get_width() / 2 + 100 \
                        and mouseY > self.boardArea.get_height() / 2 - 80 \
                        and mouseY < self.boardArea.get_height() / 2 - 50:
                            self.popupMenu.setPopupActive(False)
                            self.resumeTurn()
                        
                        # game rules
                        if mouseX > self.boardArea.get_width() / 2 - 100 \
                        and mouseX < self.boardArea.get_width() / 2 + 100 \
                        and mouseY > self.boardArea.get_height() / 2 - 40 \
                        and mouseY < self.boardArea.get_height() / 2 - 10:
                            self.popupMenu.setRulesActive(True)
                            self.popupMenu.rules(self.rulesPage)
                        # game options
                        if mouseX > self.boardArea.get_width() / 2 - 100 \
                        and mouseX < self.boardArea.get_width() / 2 + 100 \
                        and mouseY > self.boardArea.get_height() / 2 \
                        and mouseY < self.boardArea.get_height() / 2 + 30:
                            self.popupMenu.setOptionsActive(True)
                            self.popupMenu.gameOptions()
                        # exit game
                        if mouseX > self.boardArea.get_width() / 2 - 100 \
                        and mouseX < self.boardArea.get_width() / 2 + 100 \
                        and mouseY > self.boardArea.get_height() / 2 + 40 \
                        and mouseY < self.boardArea.get_height() / 2 + 70:
                            self.popupMenu.setExitCheckActive(True)
                            self.popupMenu.exitCheck()

                    # In rules menu
                    else:
                        # back
                        if mouseX > self.boardArea.get_width() / 2 - 50 \
                        and mouseX < self.boardArea.get_width() / 2 + 50 \
                        and mouseY > self.boardArea.get_height() / 2 + 95 \
                        and mouseY < self.boardArea.get_height() / 2 + 125:
                            self.popupMenu.setRulesActive(False)
                            self.popupMenu.makePopupMenu()
                        # next rule
                        if mouseX > self.boardArea.get_width() / 2 + 100 \
                        and mouseX < self.boardArea.get_width() / 2 + 160 \
                        and mouseY > self.boardArea.get_height() / 2 + 95 \
                        and mouseY < self.boardArea.get_height() / 2 + 115 \
                        and self.rulesPage < 17:
                            self.rulesPage += 1
                            self.popupMenu.rules(self.rulesPage)
                        # previous rule
                        if mouseX > self.boardArea.get_width() / 2 - 160 \
                        and mouseX < self.boardArea.get_width() / 2 - 100 \
                        and mouseY > self.boardArea.get_height() / 2 + 95 \
                        and mouseY < self.boardArea.get_height() / 2 + 115 \
                        and self.rulesPage > 1:
                            self.rulesPage -= 1
                            self.popupMenu.rules(self.rulesPage)
                        
                # exiting game - double check
                else:
                    # yes - exit
                    if mouseX > self.boardArea.get_width() / 2 - 100 \
                    and mouseX < self.boardArea.get_width() / 2 + 100 \
                    and mouseY > self.boardArea.get_height() / 2 - 60 \
                    and mouseY < self.boardArea.get_height() / 2 - 30:
                        self.popupMenu.setPopupActive(False)
                        self.gameExit = True
                    # no - go back to menu
                    if mouseX > self.boardArea.get_width() / 2 - 100 \
                    and mouseX < self.boardArea.get_width() / 2 + 100 \
                    and mouseY > self.boardArea.get_height() / 2 - 20*2 \
                    and mouseY < self.boardArea.get_height() / 2 + 10*2:
                        self.popupMenu.setExitCheckActive(False)
                        self.popupMenu.makePopupMenu()

            # in game options
            else:
                # change resolution
                change = self.popupMenu.changeResolution(mouseX, mouseY)
                if change != None:
                    self.resizeScreen(change)

                # Change sound
                if mouseX > self.boardArea.get_width()/2 - 22 \
                and mouseX < self.boardArea.get_width()/2 + 22 \
                and mouseY > self.boardArea.get_height()/2 + 168*self.scale \
                and mouseY < self.boardArea.get_height()/2 + 230*self.scale:
                    self.popupMenu.soundChange()
                    
                # back to menu
                if mouseX > self.boardArea.get_width() / 2 - 100 \
                and mouseX < self.boardArea.get_width() / 2 + 100 \
                and mouseY > self.boardArea.get_height() / 2 - 80 \
                and mouseY < self.boardArea.get_height() / 2 - 50:
                    self.popupMenu.setOptionsActive(False)
                    self.popupMenu.makePopupMenu()


    def refreshGameBoard(self):
        rect = pygame.Rect((20*self.scale, 20*self.scale),
                           (1400*self.scale, 980*self.scale))
        self.area.blit(self.gameBoard.getGB(), rect)
        self.cards.displayCard("back", self.scale)
        self.dice.displayDice(self.roll[1], self.roll[2])
        self.displayBuildingPrice()


    def refreshPlayersDisplay(self):
        rect = pygame.Rect((1440*self.scale, 0),
                           (480*self.scale, 810*self.scale))
        self.area.blit(self.playersDisplay.getPD(), rect)


    def refreshDisplay(self):
        if self.parent:    
            self.parent.blit(self.area, (0,0))
        pygame.display.update()


    def resumeTurn(self):
        """
        Used to resume a player's turn after they opened the menu
        or upgrade options.
        """
        self.refreshGameBoard()
        if not self.diceRolled:
            self.turn.beginTurn(self.extraOrLost)
        elif (self.turn.buyMsgDisplayed or self.turn.okMsgDisplayed
        or self.turn.cardLandingMsgDisplayed):
            self.turn.handleLanding()
        elif self.cardDisplayed:    # card is face up
            self.cardDisplayed = False
            self.endTurn()
            

    def resizeScreen(self, newSize):
        """
        Resizes the screen and redraws all the components at the new scale.
        Called when the user selects a new resolution option.
        """
        if self.infoScreen.current_h == newSize[1]\
           and self.infoScreen.current_w == newSize[0]:
            self.area = pygame.display.set_mode(newSize, pygame.FULLSCREEN)
        else:
            self.area = pygame.display.set_mode(newSize)
        self.scale = newSize[0] / 1920
        self.width = int(self.scale*1920)
        self.height = int(self.scale*1080)
        self.initializeDisplay()
        
        self.gameBoard = GameBoard(self.scale, self.buildings, True)
        for player in self.players:
            player.createToken(self.gameBoard.getGB(), self.scale)
        self.updatePlayerPosition()
        self.refreshGameBoard()
        
        self.playersDisplay = PlayersDisplay(self.players, self.scale, True)
        self.playersDisplay.selectPlayer(self.playerIndex)
        self.refreshPlayersDisplay()
        
        Turn.setStaticVariables(self.scale, self.area, self.buildingsObj, len(self.players))
        self.popupMenu.makePopupMenu()
        self.popupMenu.gameOptions()
        self.popupMenu.loadButtons()


    def rollDice(self):
        while self.roll[0]>0:
            self.clock.tick(30)
            self.rollTime += self.clock.get_time()
            if self.rollTime>250:
                self.roll = self.dice.roll()
                self.rollTime = 0
                self.refreshDisplay()
        self.turn.setDiceRoll(self.roll[1], self.roll[2])
        self.move()


    def move(self):
        count = 0
        self.midRoll = True
        self.players[self.playerIndex].startToken()
        self.refreshDisplay()
        self.updatePlayerPosition()
        self.refreshGameBoard()
        while count < self.roll[1] + self.roll[2]:
            self.clock.tick(30)
            self.player.increasePosition(1)
            count += 1
            if count == self.roll[1] + self.roll[2]:
                self.midRoll = False
                self.refreshDisplay()
                self.updatePlayerPosition()
                self.refreshGameBoard()
                pygame.time.wait(250)
                self.players[self.playerIndex].startToken()
            self.refreshDisplay()
            self.updatePlayerPosition()
            self.refreshGameBoard()
            if count < self.roll[1] + self.roll[2]:
                pygame.time.wait(250)
            else:
                pygame.time.wait(1000)
        self.players[self.playerIndex].removeToken()
        self.refreshDisplay()
        self.updatePlayerPosition()
        self.refreshGameBoard()
        self.turn.handleLanding()


    def updatePlayerPosition(self):
        '''updatePlayerPosition() determines the number of players
        at a given position and displays a circle of each player
        at that position'''
        pos = {}
        loc = {}
        for p in range(len(self.players)):
            if not (p == self.playerIndex and self.midRoll):
                if self.players[p].getPosition() not in pos:
                    pos[self.players[p].getPosition()] = 1
                    loc[self.players[p].getPosition()] = 0
                else:
                    pos[self.players[p].getPosition()] += 1
        for p in range(len(self.players)):
            if not (p == self.playerIndex and self.midRoll):
                self.players[p].displayWheel(1/pos[self.players[p].getPosition()], loc[self.players[p].getPosition()])
                loc[self.players[p].getPosition()] += 1
        
        
    def endTurn(self):
        print("End of turn")
        self.midTurn = False
        self.diceRolled = False
        self.refreshPlayersDisplay()
        self.refreshGameBoard()


    def displayBuildingPrice(self):
        """Displays on the game board the current price for all ownable buildings."""
        xPosition = 330 * self.scale
        yPosition = 680 * self.scale
        text = self.font.render("Building Price:", True, Colors.LIGHTGRAY)
        self.area.blit(text, (xPosition, yPosition))
        price = "${:,.0f}".format(self.buildingsObj.getCurrentPrice())
        price = self.font.render(price, True, Colors.LIGHTGRAY)
        yPosition += 1.5 * self.font.get_linesize()
        self.area.blit(price, (xPosition, yPosition))
        

    def chatting(self, event):
        CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789-=[];\'\\,./`'
        CHARSCAPS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ)!@#$%^&*(_+{}:"|<>?~'
        
        if event.key == K_ESCAPE:
            self.typing = False
            self.gameExit = True
        elif event.key == K_RETURN:
            self.chatBox.submitText()
        elif event.key == K_BACKSPACE:
            self.chatBox.deleteText()
        elif event.key <= 127 and event.key >= 32: #Only accept regular ascii characters (ignoring certain special characters)
            #self.chatBox.typeText(pygame.key.name(event.key))
            #self.chatBox.typeText(chr(event.key))
            checkCaps = pygame.key.get_pressed()
            if checkCaps[K_RSHIFT] or checkCaps[K_LSHIFT] and chr(event.key) in CHARS:
                index = CHARS.index(chr(event.key))
                if CHARSCAPS[index] not in ['{', '}']:
                    self.chatBox.typeText(CHARSCAPS[index])
                else:
                    self.chatBox.typeText(CHARSCAPS[index] + CHARSCAPS[index])
            elif checkCaps[K_CAPSLOCK] and chr(event.key) in CHARS:
                index = CHARS.index(chr(event.key))
                if index < 26: #Only caps lock regular alphabet
                    self.chatBox.typeText(CHARSCAPS[index])
                else:
                    self.chatBox.typeText(chr(event.key))
            else:
                self.chatBox.typeText(chr(event.key))


    def play(self):

        self.buildingsObj = Buildings()
        self.buildings = self.buildingsObj.getBuildingList()

        # Game Board
        self.gameBoard = GameBoard(self.scale, self.buildings, True)
        self.refreshGameBoard()
        self.refreshDisplay()

        # This data will eventually be obtained from the lobby / setup menu.
        self.players = []
        if not GameInfo.ONLINEGAME:
            for i in range(GameInfo.PLAYERNUM):
                p = Player(GameInfo.PLAYERS[i], GameInfo.PLAYERDEANS[i], self.gameBoard.getGB(), self.buildingsObj, self.scale)
                self.players.append(p)
        #p1 = Player("player1", "Agriculture", self.gameBoard.getGB(), self.buildingsObj, self.scale)
        #p2 = Player("player2", "Arts and Letters", self.gameBoard.getGB(), self.buildingsObj, self.scale)
    
        #p3 = Player("player3", "Natural and Applied Sciences", self.gameBoard.getGB(), self.buildingsObj, self.scale)
        #p4 = Player("player4", "Education", self.gameBoard.getGB(), self.buildingsObj, self.scale)
        #p5 = Player("player5", "Health and Human Services", self.gameBoard.getGB(), self.buildingsObj, self.scale)
        #p6 = Player("player6", "Humanities and Public Affairs", self.gameBoard.getGB(), self.buildingsObj, self.scale)
        #with open('FlagFile.txt') as flags:
        #    playercount = int(flags.readline().split(":"    )[1])
        

        #self.players = [p1, p2, p3, p4, p5, p6][0:playercount]
        print(self.players)

        # Players Display
        self.playersDisplay = PlayersDisplay(self.players, self.scale, True)
        self.refreshPlayersDisplay()
        self.refreshDisplay()
        
        # This needs to come after the game board is created, as creation of
        # the game board sets the rect attribute of the buildings.
        Turn.setStaticVariables(self.scale, self.area, self.buildingsObj, len(self.players))
        Turn.initializeTurnCount()
        
        pygame.key.set_repeat(75, 75)
        self.gameExit = False #Must be reset each time play is
        self.round = -1     # Will be incremented to start at round 0
        
        while not self.gameExit:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    self.mouseClick(event)
                if event.type == KEYDOWN and not self.typing: #TEMPORARY, will later replace with proper game exit
                    if event.key == K_ESCAPE:
                        self.gameExit = True
                        break
                    ###Cards demo - Remove Later ###
                    if event.key == K_c:
                        self.cardDraw = True
                        self.currentCard = self.cards.drawCard(self.scale)
                    ################################    
                if event.type == KEYDOWN and self.typing:
                    self.chatting(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    return 0

                
            if not self.midTurn:    # If it's a new player's turn...

                # If the previous player has an extra turn... 
                if Turn.extraAndLostTurns[self.playerIndex] > 0:
                    Turn.extraAndLostTurns[self.playerIndex] -= 1
                    self.extraOrLost = 1

                else:
                    self.extraOrLost = 0
                    self.playersDisplay.updatePlayer(Turn.count % len(self.players))
                    Turn.count += 1     # Note: this doesn't count actual turns;
                                        # it's still incremented for a lost turn.

                    # At the appropriate times, update the round number and
                    # the price of buildings.
                    if Turn.count % len(self.players) == 0:
                        self.round += 1
                        if (self.round > 0
                        and self.round % self.roundsBeforePriceIncrease == 0):
                            self.buildingsObj.increasePrice()
                            
                    self.playerIndex = Turn.count % len(self.players)

                    # If this player has lost a turn...
                    if Turn.extraAndLostTurns[self.playerIndex] < 0:
                        Turn.extraAndLostTurns[self.playerIndex] += 1
                        self.extraOrLost = -1

                    self.player = self.players[self.playerIndex]
                    self.playersDisplay.selectPlayer(self.playerIndex)
                    self.refreshPlayersDisplay()
                    self.updatePlayerPosition()
                    
                self.refreshGameBoard()
                self.midTurn = True
                self.turn = Turn(self.player, self.playerIndex)
                self.turn.beginTurn(self.extraOrLost)        
                
            self.refreshDisplay()
            
        return "start"
        


def main():
    pygame.init()
    screen = GameArea(pygame.display.Info(), False, 0.5)
    screen.play()



if __name__ == "__main__":
    main()
