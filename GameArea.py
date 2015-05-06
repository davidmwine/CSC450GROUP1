import pygame
from pygame.locals import *
import os
import sys
from Player import Player
from Building import *
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
from MessageBox import * # contains displayMsg(), displayMsgOK(), displayMsgYN()


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
        self.winSoundPlayed = False

        self.roundsBeforePriceIncrease = 3      # inflation

        self.rulesPage = 1 #initialize rules page to start at 1
        
        self.click = pygame.mixer.Sound(os.path.join('sound','click.wav'))        #Generic click
        self.btsound = pygame.mixer.Sound(os.path.join('sound','button.wav'))     #Screen resolution option button
        self.diceSound = pygame.mixer.Sound(os.path.join('sound','dice.wav'))     #Dice roll
        self.flipSound = pygame.mixer.Sound(os.path.join('sound','flip.wav'))     #Card click
        self.sonarSound = pygame.mixer.Sound(os.path.join('sound','sonar.wav'))   #Sound option button
        self.bubbleSound = pygame.mixer.Sound(os.path.join('sound','bubble.wav')) #Player moving 
        self.booSound = pygame.mixer.Sound(os.path.join('sound','boo.wav'))       #Game lost
        self.winSound = pygame.mixer.Sound(os.path.join('sound','winner.wav'))    #Game won
        self.typeSound = pygame.mixer.Sound(os.path.join('sound','typing.wav'))   #Chat typing
        
        
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
                self.click.play()
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
                self.diceSound.play()
                self.diceRolled = True
                self.turn.ableToRoll = False
                self.rollDice()

            # Trade Button
            if mouseX > self.controls.getWidth() / 2 \
            and mouseX < 3 * self.controls.getWidth() / 4 \
            and mouseY > self.height - self.controls.getHeight():
                self.click.play()
                self.turn.showTradeOptions()

            # Upgrade Button
            if mouseX > 3 * self.controls.getWidth() / 4 \
            and mouseX < self.controls.getWidth() \
            and mouseY > self.height - self.controls.getHeight():
                self.click.play()
                self.turn.firstUpgradeLine = 0
                self.turn.showUpgradeOptions()

            # Cards
            if (mouseX > self.cards.getXPosition()
            and mouseX < self.cards.getXPosition() + self.cards.getWidth()
            and mouseY > self.cards.getYPosition()
            and mouseY < self.cards.getYPosition() + self.cards.getHeight()):
                if self.turn.cardDraw:  # player landed on card space
                    self.flipSound.play()
                    self.turn.cardDraw = False
                    self.cardDisplayed = True
                    self.currentCard = self.cards.drawCard(self.scale, self.player)
                    (size, msgBox) = displayMsg(Turn.scale, Turn.smallMsgRect,
                        Turn.msgRect, Turn.font,
                        "Click cards again to take this action.")
                    Turn.smallMsgSurface.blit(msgBox, (0, 0))
                    self.turn.cardLandingMsgDisplayed = False
                elif self.cardDisplayed:    # card is face up
                    self.cardDisplayed = False
                    self.cards.performAction(self.currentCard, self.player)
                    if self.cards.feeCard:
                        self.cards.feeCard = False
                        self.checkBankruptcy()
                    elif self.cards.movementCard:
                        self.player.removeToken()   
                        self.updatePlayerPosition()
                        self.refreshGameBoard()
                        # Update $ displayed in case player passed Carrington.
                        self.playersDisplay.selectPlayer(self.playerIndex)
                        self.refreshPlayersDisplay()
                        self.cards.movementCard = False
                        self.turn.handleLanding()
                    else:    
                        self.endTurn()

            # Dice
            if (self.turn.ableToRoll and not self.turn.upgradeDisplayed and not self.turn.tradeDisplayed
            and mouseX > self.dice.getXPosition()
            and mouseX < self.dice.getXPosition() + self.dice.getWidth()
            and mouseY > self.dice.getYPosition()
            and mouseY < self.dice.getYPosition() + self.dice.getHeight()):
                # Update player's $ before they have to make a decision.
                self.playersDisplay.selectPlayer(self.playerIndex)
                self.refreshPlayersDisplay()
                self.roll = (1,0)
                self.diceSound.play()
                self.diceRolled = True
                self.turn.ableToRoll = False
                self.rollDice()
    
            # OK Button in Message Box
            if self.turn.okMsgDisplayed:
                okRect = pygame.Rect(Turn.msgRect.x + self.turn.okRect.x,
                                 Turn.msgRect.y + self.turn.okRect.y,
                                 self.turn.okRect.width, self.turn.okRect.height)
                if okRect.collidepoint(pygame.mouse.get_pos()):
                    self.turn.okMsgDisplayed = False
                    self.refreshGameBoard()
                    self.click.play()

                    #If Game was won go back to start
                    if Turn.gameOver:
                        self.gameExit = True
                    
                    # If player just passed Accreditation Review...
                    if (self.player.inAccreditationReview
                    and self.turn.roll % 2 == 0
                    and not self.turn.landed):
                        self.player.inAccreditationReview = False
                        self.move()
                    elif self.player.passedCarrington:
                        self.player.passedCarrington = False
                        self.turn.handleLanding()
                    else:    
                        # If applicable, charge fees and update playersDisplay.
                        if self.turn.feeMsgDisplayed:
                            self.turn.chargeFees()
                            if self.turn.owner != None:
                                self.playersDisplay.updatePlayer(
                                    self.players.index(self.turn.owner))
                            self.turn.feeMsgDisplayed = False
                            self.checkBankruptcy()
                        else:
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
                    self.click.play()
                    if self.turn.building.getPurpose() == "stealable":
                        self.turn.steal()
                    else:    
                        self.turn.buy()
                    self.gameBoard.colorBuilding(self.turn.building)
                    self.turn.buyMsgDisplayed = False
                    self.checkBankruptcy()
                elif noRect.collidepoint(pygame.mouse.get_pos()):
                    self.click.play()
                    self.turn.buyMsgDisplayed = False
                    self.endTurn()

            # Upgrade Message Box (checkboxes and OK button)
            if self.turn.upgradeDisplayed:
                # Make checkboxes look checked when clicked.
                self.turn.checkUpgrades(mouseX, mouseY)

                # Scrolling
                if event.button == 4:
                    if self.turn.firstUpgradeLine > 0:
                        self.turn.firstUpgradeLine -= 1
                    self.turn.showUpgradeOptions()
                elif event.button == 5:
                    if (self.turn.firstUpgradeLine + Turn.upgradeLinesToDisplay
                        < self.turn.upgradeLineCount):
                        self.turn.firstUpgradeLine += 1
                    self.turn.showUpgradeOptions()
                
                okUpgradeRect = pygame.Rect(Turn.upgradeRect.x + self.turn.okUpgradeRect.x,
                                 Turn.upgradeRect.y + self.turn.okUpgradeRect.y,
                                 self.turn.okUpgradeRect.width, self.turn.okUpgradeRect.height)
                if okUpgradeRect.collidepoint(pygame.mouse.get_pos()):
                    self.click.play()
                    # Once the player clicks OK, complete desired upgrades and update display.
                    self.turn.upgrade()
                    self.playersDisplay.selectPlayer(Turn.count % len(self.players))
                    self.refreshPlayersDisplay()
                    self.gameBoard.addPlayerGradIcons(self.player)
                    self.checkBankruptcy()
                    self.turn.upgradeDisplayed = False

            # Trade Box
            if self.turn.tradeDisplayed:
                self.turn.selectPlayerTrade(mouseX, mouseY)
                if self.turn.traderSelected:
                    self.turn.checkTradeBuildings(mouseX, mouseY)
                    self.turn.setTradeMoney(mouseX, mouseY)
                if self.turn.cancelTrade(mouseX, mouseY):
                    self.resumeTurn()
                    self.turn.tradeDisplayed = False
                finished = self.turn.finishTrade(mouseX, mouseY)
                if finished != None:
                    for building in finished:
                        self.gameBoard.colorBuilding(building)
                    self.resumeTurn()
                    self.refreshPlayersDisplay()
                    self.refreshGameBoard()
                    self.turn.tradeDisplayed = False
                
                                        
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
                            self.click.play()
                            self.popupMenu.setPopupActive(False)
                            self.resumeTurn()
                        
                        # game rules
                        if mouseX > self.boardArea.get_width() / 2 - 100 \
                        and mouseX < self.boardArea.get_width() / 2 + 100 \
                        and mouseY > self.boardArea.get_height() / 2 - 40 \
                        and mouseY < self.boardArea.get_height() / 2 - 10:
                            self.click.play()
                            self.popupMenu.setRulesActive(True)
                            self.popupMenu.rules(self.rulesPage)
                        # game options
                        if mouseX > self.boardArea.get_width() / 2 - 100 \
                        and mouseX < self.boardArea.get_width() / 2 + 100 \
                        and mouseY > self.boardArea.get_height() / 2 \
                        and mouseY < self.boardArea.get_height() / 2 + 30:
                            self.click.play()
                            self.popupMenu.setOptionsActive(True)
                            self.popupMenu.gameOptions()
                        # exit game
                        if mouseX > self.boardArea.get_width() / 2 - 100 \
                        and mouseX < self.boardArea.get_width() / 2 + 100 \
                        and mouseY > self.boardArea.get_height() / 2 + 40 \
                        and mouseY < self.boardArea.get_height() / 2 + 70:
                            self.click.play()
                            self.popupMenu.setExitCheckActive(True)
                            self.popupMenu.exitCheck()

                    # In rules menu
                    else:
                        # back
                        if mouseX > self.boardArea.get_width() / 2 - 50 \
                        and mouseX < self.boardArea.get_width() / 2 + 50 \
                        and mouseY > self.boardArea.get_height() / 2 + 95 \
                        and mouseY < self.boardArea.get_height() / 2 + 125:
                            self.click.play()
                            self.popupMenu.setRulesActive(False)
                            self.popupMenu.makePopupMenu()
                        # next rule
                        if mouseX > self.boardArea.get_width() / 2 + 100 \
                        and mouseX < self.boardArea.get_width() / 2 + 160 \
                        and mouseY > self.boardArea.get_height() / 2 + 95 \
                        and mouseY < self.boardArea.get_height() / 2 + 115 \
                        and self.rulesPage < 17:
                            self.click.play()
                            self.rulesPage += 1
                            self.popupMenu.rules(self.rulesPage)
                        # previous rule
                        if mouseX > self.boardArea.get_width() / 2 - 160 \
                        and mouseX < self.boardArea.get_width() / 2 - 100 \
                        and mouseY > self.boardArea.get_height() / 2 + 95 \
                        and mouseY < self.boardArea.get_height() / 2 + 115 \
                        and self.rulesPage > 1:
                            self.click.play()
                            self.rulesPage -= 1
                            self.popupMenu.rules(self.rulesPage)
                        
                # exiting game - double check
                else:
                    # yes - exit
                    if mouseX > self.boardArea.get_width() / 2 - 100 \
                    and mouseX < self.boardArea.get_width() / 2 + 100 \
                    and mouseY > self.boardArea.get_height() / 2 - 60 \
                    and mouseY < self.boardArea.get_height() / 2 - 30:
                        self.click.play()
                        self.popupMenu.setPopupActive(False)
                        self.gameExit = True
                    # no - go back to menu
                    if mouseX > self.boardArea.get_width() / 2 - 100 \
                    and mouseX < self.boardArea.get_width() / 2 + 100 \
                    and mouseY > self.boardArea.get_height() / 2 - 20*2 \
                    and mouseY < self.boardArea.get_height() / 2 + 10*2:
                        self.click.play()
                        self.popupMenu.setExitCheckActive(False)
                        self.popupMenu.makePopupMenu()

            # in game options
            else:
                # change resolution
                change = self.popupMenu.changeResolution(mouseX, mouseY)
                if change != None:
                    self.btsound.play()
                    self.resizeScreen(change)

                # Change sound
                if mouseX > self.boardArea.get_width()/2 - 22 \
                and mouseX < self.boardArea.get_width()/2 + 22 \
                and mouseY > self.boardArea.get_height()/2 + 168*self.scale \
                and mouseY < self.boardArea.get_height()/2 + 230*self.scale:
                    self.popupMenu.soundChange()
                    self.sonarSound.play()
                    
                # back to menu
                if mouseX > self.boardArea.get_width() / 2 - 100 \
                and mouseX < self.boardArea.get_width() / 2 + 100 \
                and mouseY > self.boardArea.get_height() / 2 - 80 \
                and mouseY < self.boardArea.get_height() / 2 - 50:
                    self.click.play()
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
            self.turn.beginTurn(self.extraOrLost, False)
        # If the player just rolled to see if they passed Accreditation Review    
        elif (self.player.inAccreditationReview and not self.turn.landed):
            self.turn.checkAccreditation()
        elif (self.turn.buyMsgDisplayed or self.turn.okMsgDisplayed
        or self.turn.cardLandingMsgDisplayed):
            self.turn.handleLanding()
        elif self.cardDisplayed:    # card is face up
            self.cards.displayCard(self.currentCard, self.scale)
            (size, msgBox) = displayMsg(Turn.scale, Turn.smallMsgRect,
                            Turn.msgRect, Turn.font,
                            "Click cards again to take this action.")
            Turn.smallMsgSurface.blit(msgBox, (0, 0))


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
        self.gameBoard.restoreOwnerColors()
        for player in self.players:
            player.createToken(self.gameBoard.getGB(), self.scale)
            player.startToken()     # These undo each other, but are needed
            player.removeToken()    # to initialize instance variables.
            self.gameBoard.addPlayerGradIcons(player)
        self.updatePlayerPosition()
        self.refreshGameBoard()
        
        self.playersDisplay = PlayersDisplay(self.players, self.scale, True)
        self.playersDisplay.selectPlayer(self.playerIndex)
        self.refreshPlayersDisplay()
        
        Turn.setStaticVariables(self.scale, self.area, self.buildingsObj, len(self.players), self.players)
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
        if not self.player.inAccreditationReview:
            self.move()


    def move(self):
        if Turn.gameOver:
            return
        
        count = 0
        self.midRoll = True
        self.players[self.playerIndex].startToken()
        self.refreshDisplay()
        self.updatePlayerPosition()
        self.refreshGameBoard()
        while count < self.roll[1] + self.roll[2]:
            self.clock.tick(30)
            self.player.increasePosition(1)
            self.bubbleSound.play()
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
            # Update $ displayed if player passes Carrington.
            self.playersDisplay.selectPlayer(self.playerIndex)
            self.refreshPlayersDisplay()
            if count < self.roll[1] + self.roll[2]:
                pygame.time.wait(250)
            else:
                self.bubbleSound.play()
                pygame.time.wait(1000)       
        self.players[self.playerIndex].removeToken()
        self.refreshDisplay()
        self.updatePlayerPosition()
        self.refreshGameBoard()
        # Check game ending here so player gets winning message
        # rather than landing message.
        Turn.gameOver = self.checkGameEnding()
        self.turn.handleLanding()


    def updatePlayerPosition(self):
        '''updatePlayerPosition() determines the number of players
        at a given position and displays a circle of each player
        at that position'''        
        pos = {}    # Keys: board positions, Values: number of players at each position
        loc = {}    # Keys: board positions, Values: indices of players at each position

        for player in self.activePlayers:
            if not (player == self.player and self.midRoll):
                if player.getPosition() not in pos:
                    pos[player.getPosition()] = 1
                    loc[player.getPosition()] = 0
                else:
                    pos[player.getPosition()] += 1
        for player in self.activePlayers:
            if not (player == self.player and self.midRoll):
                player.displayWheel(1/pos[player.getPosition()], loc[player.getPosition()])
                loc[player.getPosition()] += 1
        
        
    def endTurn(self):
        print("End of turn")
        self.midTurn = False
        self.diceRolled = False
        self.refreshPlayersDisplay()
        self.refreshGameBoard()

    
    def checkBankruptcy(self):
        """
        During or just after a player's turn, checks whether this player
        has gone bankrupt.  If so, a message is displayed and the player is
        eliminated from the game.
        """
        if self.player.getDollars() <= 0:
            
            self.player.isBankrupt = True
            Turn.extraAndLostTurns[self.playerIndex] = 0

            if self.player in self.activePlayers:
                self.activePlayers.remove(self.player)

            self.playersDisplay = PlayersDisplay(self.players, self.scale, True)
            self.refreshPlayersDisplay()

            for building in self.player.getBuildings():
                if building.getPurpose() == "academic":
                    building.setDegreeLvl("Associate")
                building.setOwner(None)
                building.setColor(building.getInitialColor())

            self.gameBoard = GameBoard(self.scale, self.buildings, True)
            self.gameBoard.restoreOwnerColors()
            for player in self.activePlayers:
                player.createToken(self.gameBoard.getGB(), self.scale)
                self.gameBoard.addPlayerGradIcons(player)
            self.updatePlayerPosition()
            self.refreshGameBoard()    

            (msgBox, self.turn.okRect) = displayMsgOK(Turn.scale, Turn.msgRect,
                Turn.font, self.player.getName() + " has gone bankrupt and "
                                        + "been eliminated from the game.")
            Turn.msgSurface.blit(msgBox, (0, 0))
            self.booSound.play()
            self.turn.okMsgDisplayed = True    
            
        elif self.turn.upgradeDisplayed:
            self.resumeTurn()    
        else:
            self.endTurn()
    

    def checkGameEnding(self):
        """
        Checks whether the game is over, either by all players except one
        going bankrupt or by a player earning more than 50 Graduate Points.
        If so, displays an appropriate message.
        """
        if len(self.activePlayers) == 1:
            winner = self.activePlayers[0].getName()
            (msgBox, self.turn.okRect) = displayMsgOK(Turn.scale, Turn.msgRect,
                Turn.font, winner + " is the winner! All other players have"
                                                      + " gone bankrupt.")
            Turn.msgSurface.blit(msgBox, (0, 0))
            if not self.winSoundPlayed:
                self.winSoundPlayed = True
                self.winSound.play()
            self.turn.okMsgDisplayed = True
            return True

        else:
            for player in self.activePlayers:
                if player.getPoints() >= 50:
                    (msgBox, self.turn.okRect) = displayMsgOK(Turn.scale, Turn.msgRect,
                        Turn.font, player.getName() + " earned "
                        + str(player.getPoints())
                        + " Graduate Points and wins the game!")
                    Turn.msgSurface.blit(msgBox, (0, 0))
                    if not self.winSoundPlayed:
                        self.winSoundPlayed = True
                        self.winSound.play()
                    self.turn.okMsgDisplayed = True
                    return True

            return False
            

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
            self.typeSound.play()
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
            print("NUMBER OF PLAYERS IS: ", GameInfo.PLAYERNUM)
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
        #print(self.players)

        # Copy self.players; we'll remove players when they go bankrupt.
        self.activePlayers = [player for player in self.players]

        # Players Display
        self.playersDisplay = PlayersDisplay(self.players, self.scale, True)
        self.refreshPlayersDisplay()
        self.refreshDisplay()
        
        # This needs to come after the game board is created, as creation of
        # the game board sets the rect attribute of the buildings.
        Turn.setStaticVariables(self.scale, self.area, self.buildingsObj, len(self.players), self.players)
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
                if event.type == KEYDOWN and self.typing:
                    self.chatting(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    return 0

                
            if not self.midTurn:    # If it's a new player's turn...

                # If the game is over and the player has clicked OK,
                # go back to the Start Menu.
                if Turn.gameOver:
                    break

                # If the previous player has an extra turn... 
                if Turn.extraAndLostTurns[self.playerIndex] > 0:
                    self.playersDisplay.selectPlayer(self.playerIndex)
                    self.refreshPlayersDisplay()
                    Turn.extraAndLostTurns[self.playerIndex] -= 1
                    self.extraOrLost = 1

                else:
                    self.extraOrLost = 0
                    if Turn.count > -1 and not self.player.isBankrupt:
                        self.playersDisplay.updatePlayer(Turn.count % len(self.players))

                    # Skip all players who are bankrupt.
                    while True:
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

                        if not self.player.isBankrupt:
                            break
                    
                    self.playersDisplay.selectPlayer(self.playerIndex)
                    self.refreshPlayersDisplay()
                    self.updatePlayerPosition()
                    
                self.refreshGameBoard()
                self.midTurn = True
                self.turn = Turn(self.player, self.playerIndex)

                #Turn.gameOver = self.checkGameEnding()
                
                self.turn.beginTurn(self.extraOrLost)       
                
            Turn.gameOver = self.checkGameEnding()
            self.refreshDisplay()
            
        return "start"
        


def main():
    pygame.init()
    screen = GameArea(pygame.display.Info(), False, 0.5)
    screen.play()



if __name__ == "__main__":
    main()
