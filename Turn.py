import pygame
from pygame.locals import *
from MessageBox import * # contains displayMsg(), displayMsgOK(), displayMsgYN()
from CheckBox import CheckBox
from EntryBox import EntryBox
from Building import *


class Turn(object):
    """Contains most of the methods related to the game logic of a player's turn."""     

    def __init__(self, player, playerIndex):
        self.player = player
        self.playerIndex = playerIndex
        self.roll = 0
        self.building = None    # Will hold building space that is landed on
        self.owner = None   # Will hold the owner of the building landed on
        self.feeAmt = None  # Will hold the fee for landing on a building
        self.buyMsgDisplayed = False
        self.okMsgDisplayed = False     # True if any OK message is displayed
        self.feeMsgDisplayed = False
        self.cardLandingMsgDisplayed = False    
        self.upgradeDisplayed = False   # True if upgrade screen is displayed
        self.tradeDisplayed = False     #True if trade screen is displayed
        self.cardDraw = False   # True if player landed on a card space
        self.ableToRoll = False # True only when a player is allowed to roll dice
        self.landed = False     # True if player has landed on a space for the turn
        

    @staticmethod
    def initializeTurnCount():
        Turn.count = -1     # This will be incremented to 0 for the first turn.
                            # Note that, in order to keep track of rounds, this
                            # variable doesn't count actual turns; for example,
                            # if a player loses a turn, this is still incremented.


    @staticmethod
    def setStaticVariables(scale, parent, buildings, playerCount, players):
        """
        These variables are used by and related to the other methods in this
        class, but are not closely related to individual players' turns
        (i.e., Turn instances).
        """
        Turn.scale = scale
        Turn.parent = parent
        Turn.buildings = buildings
        Turn.extraAndLostTurns = [0] * playerCount
        Turn.players = players
        Turn.font = pygame.font.Font(None, int(50*scale))
        Turn.msgRect = pygame.Rect(440*scale, 250*scale,
                                   560*scale, 400*scale)
        Turn.smallMsgRect = pygame.Rect(440*scale, 250*scale,
                                   560*scale, 105*scale)
        Turn.upgradeRect = pygame.Rect(440*scale, 250*scale,
                                   560*scale, 540*scale)
        Turn.tradeRect = pygame.Rect(440*scale, 250*scale,
                                     560*scale, 540*scale)
        Turn.msgSurface = parent.subsurface(Turn.msgRect)
        Turn.smallMsgSurface = parent.subsurface(Turn.smallMsgRect)
        Turn.upgradeSurface = parent.subsurface(Turn.upgradeRect)
        Turn.tradeSurface = parent.subsurface(Turn.tradeRect)
        Turn.gameOver = False


    def beginTurn(self, extraOrLost, begin = True):
        """
        Displays a message indicating which player's turn it is
        and giving instructions to roll the dice.  Also, displays messages
        regarding lost or extra turns.
        """
        # If a player has won, allow the appropriate message to be displayed.
        if Turn.gameOver:
            return

        # If a player has lost a turn, display this fact.
        if extraOrLost == -1:
            (msgBox, self.okRect) = displayMsgOK(Turn.scale, Turn.msgRect,
                    Turn.font, self.player.getName() + " has lost this turn.")
            Turn.msgSurface.blit(msgBox, (0, 0))
            self.okMsgDisplayed = True
            return
        
        print("------- " + self.player.getName() + "'s turn -------")
        # If a player owns a stealable building, add that turn's profit to their $.
        if begin: #Only update stealable buildings at beginning of turn, not on resume
            self.player.addDollars(50000 * self.player.getNumStealable())

        # If the player is in Accreditation Review, display appropriate message.
        if self.player.inAccreditationReview:
            (size, msgBox) = displayMsg(Turn.scale, Turn.smallMsgRect, Turn.msgRect,
                Turn.font, self.player.getName() + ", you're stuck in "
                    + "Accreditation Review. Roll dice to see if you pass.")

        # If this is a player's extra turn, indicate that.
        elif extraOrLost == 1:
            (size, msgBox) = displayMsg(Turn.scale, Turn.smallMsgRect, Turn.msgRect,
                Turn.font, self.player.getName() + "'s extra turn. Roll dice.")
        else:    
            (size, msgBox) = displayMsg(Turn.scale, Turn.smallMsgRect, Turn.msgRect,
                Turn.font, self.player.getName() + "'s turn. Roll dice.")

        self.ableToRoll = True    
            
        if (size == "small"):
            Turn.smallMsgSurface.blit(msgBox, (0, 0))
        else:    
            Turn.msgSurface.blit(msgBox, (0, 0))
            
        
    def setDiceRoll(self, roll1, roll2):
        """
        Sets the value of the dice (as obtained from GameArea) for use in the
        Turn class. Arranges to give the player an extra turn if doubles were
        rolled. If player is in Accreditation Review, arranges to have this roll
        check that result rather than moving the player.
        """
        self.roll = roll1 + roll2
        print("Dice Rolled:", self.roll)
        # Give the player an extra turn for rolling doubles.
        if roll1 == roll2:
            Turn.extraAndLostTurns[self.playerIndex] += 1
        if self.player.inAccreditationReview:
            self.checkAccreditation()
            

    def checkAccreditation(self):
        """
        Checks dice roll to determine whether player has passed
        Accreditation Review and displays appropriate message.
        """
        if self.roll % 2 == 0:
            (msgBox, self.okRect) = displayMsgOK(Turn.scale, Turn.msgRect,
                Turn.font, "You rolled an even number and passed "
                + "Accreditation Review! You're free to go!")
            Turn.msgSurface.blit(msgBox, (0, 0))
            self.okMsgDisplayed = True
        else:
            (msgBox, self.okRect) = displayMsgOK(Turn.scale, Turn.msgRect,
                Turn.font, "You rolled an odd number so you didn't pass "
                + "Accreditation Review. You must pay $100,000 to make "
                + "required improvements and try again next turn.")
            Turn.msgSurface.blit(msgBox, (0, 0))
            self.okMsgDisplayed = True
            self.feeMsgDisplayed = True
            self.feeAmt = 100000            


    def handleLanding(self):
        """
        This method handles what comes next after a player lands on a space,
        (e.g., buying the building or paying fees to another player).
        """
        # If a player has won, allow the appropriate message to be displayed.
        if Turn.gameOver:
            return
        
        self.landed = True
        position = self.player.getPosition()
        self.building = Turn.buildings.getBuildingList()[position]
        print("Token landed on", self.building.getName())

        if self.player.passedCarrington:
            (msgBox, self.okRect) = displayMsgOK(Turn.scale, Turn.msgRect,
                Turn.font, "You passed Carrington Hall and received "
                + "$200,000 and {} graduate {}!".format(
                self.player.getPointsPerRound(),
                "point" if self.player.getPointsPerRound() == 1 else "points"))
            Turn.msgSurface.blit(msgBox, (0, 0))
            self.okMsgDisplayed = True
        
        elif self.building.getPurpose() == "special":
            if self.building.getName() == "Carrington Hall":
                (msgBox, self.okRect) = displayMsgOK(Turn.scale, Turn.msgRect,
                    Turn.font, "Welcome to Carrington Hall!")
            elif self.building.getName() == "Bear Park North":
                (msgBox, self.okRect) = displayMsgOK(Turn.scale, Turn.msgRect,
                    Turn.font, "Welcome to Bear Park North!  Lose a turn!")
                Turn.extraAndLostTurns[self.playerIndex] -= 1
            elif self.building.getName() == "Bear Park South":
                (msgBox, self.okRect) = displayMsgOK(Turn.scale, Turn.msgRect,
                    Turn.font, "Welcome to Bear Park South! Take an extra turn!")
                Turn.extraAndLostTurns[self.playerIndex] += 1
            elif self.building.getName() == "Accreditation Review":
                (msgBox, self.okRect) = displayMsgOK(Turn.scale, Turn.msgRect,
                    Turn.font, "Welcome to Accreditation Review! On your next "
                            + "turn, you can roll to find out if you passed.")
                self.player.inAccreditationReview = True
            Turn.msgSurface.blit(msgBox, (0, 0))
            self.okMsgDisplayed = True
            
        elif self.building.getPurpose() == "card":
            self.cardDraw = True
            (size, msgBox) = displayMsg(Turn.scale, Turn.smallMsgRect, Turn.msgRect,
                Turn.font, "Welcome to " + self.building.getName() + "! Draw a card.")
            Turn.smallMsgSurface.blit(msgBox, (0, 0))
            self.cardLandingMsgDisplayed = True
                
        elif self.building.getPurpose() == "utility":
            if self.building.getName() == "Power House":
                self.feeAmt = 200000;
            elif self.building.getName() == "Central Stores & Maintenance":
                self.feeAmt = 50000 * self.player.getNumBuildings()
            (msgBox, self.okRect) = displayMsgOK(Turn.scale, Turn.msgRect,
                    Turn.font, "You pay ${:,.0f} to {}.".format(self.feeAmt,
                                                        self.building.getName()))
            Turn.msgSurface.blit(msgBox, (0, 0))
            self.okMsgDisplayed = True
            self.feeMsgDisplayed = True    
        
        else:    # ownable buildings
            self.owner = self.building.getOwner()
            if self.owner == self.player:
                (msgBox, self.okRect) = displayMsgOK(Turn.scale, Turn.msgRect,
                    Turn.font, "You already own " + self.building.getName() + ".")
                Turn.msgSurface.blit(msgBox, (0, 0))
                self.okMsgDisplayed = True
                
            elif self.owner == None:
                if self.building.getPurpose() == "stealable":
                    (msgBox, self.yesRect, self.noRect) = displayMsgYN(
                    Turn.scale, Turn.msgRect, Turn.font,
                    "Do you want to buy " + self.building.getName()
                    + "? It will generate $50,000 profit for you on each turn.")
                else:    
                    (msgBox, self.yesRect, self.noRect) = displayMsgYN(
                    Turn.scale, Turn.msgRect, Turn.font,
                    "Do you want to buy " + self.building.getName() + "?")
                Turn.msgSurface.blit(msgBox, (0, 0))
                self.buyMsgDisplayed = True
                
            elif self.owner != self.player:
                if self.building.getPurpose() == "stealable":
                    (msgBox, self.yesRect, self.noRect) = displayMsgYN(
                        Turn.scale, Turn.msgRect, Turn.font,
                        "Do you want to buy " + self.building.getName()
                        + " and steal it from " + self.owner.getName()
                        + "? It will generate $50,000 profit for you on each turn.")
                    Turn.msgSurface.blit(msgBox, (0, 0))
                    self.buyMsgDisplayed = True
                    return
            
                if self.building.getPurpose() == "academic":
                    self.feeAmt = self.building.getFeeAmount(Turn.buildings.getCurrentPrice())
                elif self.building.getPurpose() == "sports":
                    self.feeAmt = 1000 * self.player.getPoints()
                (msgBox, self.okRect) = displayMsgOK(Turn.scale, Turn.msgRect,
                    Turn.font, "Welcome to {}! You pay ${:,.0f} to {}.".format(
                        self.building.getName(), self.feeAmt, self.owner.getName()))
                Turn.msgSurface.blit(msgBox, (0, 0))
                self.okMsgDisplayed = True
                self.feeMsgDisplayed = True


    def buy(self):
        """Takes care of bookkeeping once player clicked Yes to buy building"""
        self.player.subtractDollars(Turn.buildings.getCurrentPrice())
        self.player.addBuilding(self.building)
        self.building.setOwner(self.player)
        self.building.setColor(self.player.getColor())
        if self.building.getPurpose() == 'academic':
            self.player.addPointsPerRound(1)


    def chargeFees(self):
        """If building is already owned, fees are paid to owner."""
        self.player.subtractDollars(self.feeAmt)
        if self.owner != None:
            self.owner.addDollars(self.feeAmt)


    def steal(self):
        """Takes care of bookkeeping when player buys a stealable building."""
        if self.owner != None:
            self.owner.removeBuilding(self.building)
            self.owner.removeStealable(self.building.getName())
        self.player.subtractDollars(Turn.buildings.getCurrentPrice())
        self.player.addBuilding(self.building)
        self.player.addStealable(self.building.getName())
        self.building.setOwner(self.player)
        self.building.setColor(self.player.getColor())

    # copy font op from msu_game for Entry box
    def fontOp(self, size, fontName):  #Pick font size and type
        if fontName == "helvetica":
            fontAndSize = pygame.font.Font(os.path.join("font","helvetica.otf"),int(size)) # "font" is directory for the font file
        elif fontName == "berlin":
            fontAndSize = pygame.font.Font(os.path.join("font","berlin.ttf"),int(size))
        return fontAndSize
        

    def showTradeOptions(self):
        """
        Displays a message box in which the player can select the player
        he/she wants to trade with and select what buildings/money
        he/she wants to trade.
        """
        # Create message box as a surface.
        padding = 5*Turn.scale
        font = pygame.font.Font(None, int(40*self.scale))
        self.tradeBox = pygame.Surface((Turn.tradeRect.width, Turn.tradeRect.height - 2*padding))
        self.tradeBox.fill(Colors.LIGHTGRAY)

        lineHeight = font.get_linesize()
        lineYpos = padding
        
        text = "Players to trade with: "
        text = font.render(text, True, Color("black"))
        self.tradeBox.blit(text, (padding, lineYpos))
        # Create buttons for each other player
        self.otherPlayers = Turn.players
        try:
            self.otherPlayers.remove(self.player)
        except:
            pass
        rectTop = padding + lineHeight
        rectLeft = padding
        font = pygame.font.Font(None, int(30*self.scale))
        self.playerRects = []
        for player in self.otherPlayers:
            playerButton = pygame.Surface((100*Turn.scale, 50*Turn.scale))
            self.playerButtonRect = playerButton.get_rect()
            playerButton.fill(player.getColor())
            text = player.getName()
            text = font.render(text, True, Color("black"))
            textPos = text.get_rect()
            textPos.center = self.playerButtonRect.center
            playerButton.blit(text, textPos)
            self.playerButtonRect.left = rectLeft
            self.playerButtonRect.top = rectTop
            self.playerRects.append(self.playerButtonRect)
            self.tradeBox.blit(playerButton, self.playerButtonRect)
            #rectTop += 30
            rectLeft += 55

        #Display your items for trade
        font = pygame.font.Font(None, int(30*self.scale))
        lineYpos += lineHeight + 60*self.scale
        text = "Your items for trade: "
        text = font.render(text, True, Color("black"))
        self.tradeBox.blit(text, (padding, lineYpos))
        lineYpos += lineHeight
        boxRect = Rect(padding, lineYpos, 50*self.scale, 30*self.scale)
        boxRect.left = padding
        boxRect.top = lineYpos
        moneyEntry = EntryBox(self.tradeBox, 20, boxRect,
                              self.fontOp, self.scale, None, start_text="$$$")
        moneyEntry.draw()
        self.theirBuildingCheckBoxes = []
        self.yourBuildingCheckBoxes = []
        lineYpos += padding
        for building in self.player.buildings:
            lineYpos += lineHeight
            checkbox = CheckBox(self.tradeBox, padding, lineYpos, 20*self.scale)
            self.yourBuildingCheckBoxes.append(checkbox)
            checkbox.draw()
            text = building.getName()
            text = font.render(text, True, Color("black"))
            self.tradeBox.blit(text, (padding + 25*self.scale, lineYpos))
            
        # Create and position OK button.
        okButton = pygame.Surface((100*Turn.scale, 50*Turn.scale))
        self.okTradeRect = okButton.get_rect()
        okButton.fill(Colors.MEDGRAY)
        text = Turn.font.render("OK", True, Color("black"))
        textPos = text.get_rect()
        textPos.center = self.okTradeRect.center
        okButton.blit(text, textPos)
        self.okTradeRect.bottom = self.tradeBox.get_rect().height - 10
        self.okTradeRect.centerx = self.tradeBox.get_rect().centerx
        self.tradeBox.blit(okButton, self.okTradeRect)

        # Display on game board.
        self.tradeDisplayed = True
        Turn.tradeSurface.blit(self.tradeBox, (0, 0))

    def selectPlayerTrade(self, x, y):
        """
        Within the trade display window, handles the selecting of players to
        trade with.  Displays other players properties.
        """
        for i, playerRect in enumerate(self.playerRects):
            if playerRect.collidepoint(x - Turn.tradeRect.x,
                                       y - Turn.tradeRect.y):
                self.showTradeOptions()
                player = self.otherPlayers[i]
                font = pygame.font.Font(None, int(40*self.scale))
                lineHeight = font.get_linesize()
                font = pygame.font.Font(None, int(30*self.scale))
                lineYpos = 95*self.scale
                padding = 285*self.scale
                text = player.getName() + "'s items for trade: "
                text = font.render(text, True, Color("black"))
                self.tradeBox.blit(text, (padding, lineYpos))
                lineYpos += lineHeight
                boxRect = Rect(padding, lineYpos, 50*self.scale, 30*self.scale)
                boxRect.left = padding
                boxRect.top = lineYpos
                moneyEntry = EntryBox(self.tradeBox, 20, boxRect,
                                      self.fontOp, self.scale, None, start_text="$$$")
                moneyEntry.draw()
                lineYpos += 5*self.scale
                for building in player.buildings:
                    lineYpos += lineHeight
                    checkbox = CheckBox(self.tradeBox, padding, lineYpos, 20*self.scale)
                    self.theirBuildingCheckBoxes.append(checkbox)
                    checkbox.draw()
                    text = building.getName()
                    text = font.render(text, True, Color("black"))
                    self.tradeBox.blit(text, (padding + 25*self.scale, lineYpos))

                Turn.tradeSurface.blit(self.tradeBox, (0, 0))

    def checkTradeBuildings(self, x, y):
        """
        Within the trade display window, handles the display of checkboxes
        (toggling between checked and unchecked) as the player clicks them.
        """
        for checkbox in (self.yourBuildingCheckBoxes):
            if checkbox.setChecked(x - Turn.tradeRect.x,
                                   y - Turn.tradeRect.y):
                checkbox.draw()
                Turn.tradeSurface.blit(self.tradeBox, (0, 0))
        for checkbox in (self.theirBuildingCheckBoxes):
            if checkbox.setChecked(x - Turn.tradeRect.x,
                                   y - Turn.tradeRect.y):
                checkbox.draw()
                Turn.tradeSurface.blit(self.tradeBox, (0, 0))
                
    def showUpgradeOptions(self):
        """
        Displays a message box in which the player can select the buildings
        he/she wants to upgrade and which level to upgrade to.
        """
        # Create message box as a surface.
        padding = 5*Turn.scale
        font = pygame.font.Font(None, int(40*self.scale))
        self.upgradeBox = pygame.Surface((Turn.upgradeRect.width, Turn.upgradeRect.height - 2*padding))
        self.upgradeBox.fill(Colors.LIGHTGRAY)

        # Display list of possible upgrades with checkboxes.
        lines = []
        self.bachelors = self.player.getPossibleUpgrades()[0]
        self.masters = self.player.getPossibleUpgrades()[1]
        self.doctorates = self.player.getPossibleUpgrades()[2]
        
        lineHeight = font.get_linesize()
        lineIndex = 0
        lineYpos = padding
        
        if len(self.bachelors) + len(self.masters) + len(self.doctorates) == 0:
            text = "No upgrades available."
            text = font.render(text, True, Color("black"))
            self.upgradeBox.blit(text, (padding, lineYpos))

        if len(self.bachelors) > 0:
            self.bachelorCheckboxes = []
            text = "Upgrade to Bachelors:"
            text = font.render(text, True, Color("black"))
            self.upgradeBox.blit(text, (padding, lineYpos))
            lineIndex += 1
            
            for i in range(len(self.bachelors)):
                lineYpos = 1.5 * lineIndex * lineHeight + padding   # 1.5 is line spacing
                self.bachelorCheckboxes.append(CheckBox(self.upgradeBox,
                                    20*self.scale, lineYpos, 20*self.scale))
                self.bachelorCheckboxes[i].draw()
                text = self.bachelors[i]
                text = font.render(text, True, Color("black"))
                self.upgradeBox.blit(text, (60*self.scale, lineYpos))

                text = "$100,000"
                text = font.render(text, True, Color("black"))
                self.upgradeBox.blit(text, (400*self.scale, lineYpos))
                lineIndex += 1

        if len(self.masters) > 0:
            self.masterCheckboxes = []
            lineYpos = 1.5 * lineIndex * lineHeight + padding
            text = "Upgrade to Masters:"
            text = font.render(text, True, Color("black"))
            self.upgradeBox.blit(text, (padding, lineYpos))
            lineIndex += 1
            
            for i in range(len(self.masters)):
                lineYpos = 1.5 * lineIndex * lineHeight + padding
                self.masterCheckboxes.append(CheckBox(self.upgradeBox,
                                    20*self.scale, lineYpos, 20*self.scale))
                self.masterCheckboxes[i].draw()
                text = self.masters[i]
                text = font.render(text, True, Color("black"))
                self.upgradeBox.blit(text, (60*self.scale, lineYpos))
                
                building = Turn.buildings.getBuilding(self.masters[i])
                if building.getDegreeLvl() == "Associate":
                    text = "$250,000"
                else:
                    text = "$150,000"
                text = font.render(text, True, Color("black"))
                self.upgradeBox.blit(text, (400*self.scale, lineYpos))
                lineIndex += 1

        if len(self.doctorates) > 0:
            self.doctorateCheckboxes = []
            lineYpos = 1.5 * lineIndex * lineHeight + padding
            text = "Upgrade to Doctorates:"
            text = font.render(text, True, Color("black"))
            self.upgradeBox.blit(text, (padding, lineYpos))
            lineIndex += 1
            
            for i in range(len(self.doctorates)):
                lineYpos = 1.5 * lineIndex * lineHeight + padding
                self.doctorateCheckboxes.append(CheckBox(self.upgradeBox,
                                    20*self.scale, lineYpos, 20*self.scale))
                self.doctorateCheckboxes[i].draw()
                text = self.doctorates[i]
                text = font.render(text, True, Color("black"))
                self.upgradeBox.blit(text, (60*self.scale, lineYpos))

                building = Turn.buildings.getBuilding(self.doctorates[i])
                if building.getDegreeLvl() == "Associate":
                    text = "$500,000"
                elif building.getDegreeLvl() == "Bachelor":
                    text = "$400,000"
                else:
                    text = "$250,000"
                text = font.render(text, True, Color("black"))
                self.upgradeBox.blit(text, (400*self.scale, lineYpos))
                lineIndex += 1    
        
        # Create and position OK button.
        okButton = pygame.Surface((100*Turn.scale, 50*Turn.scale))
        self.okUpgradeRect = okButton.get_rect()
        okButton.fill(Colors.MEDGRAY)
        text = Turn.font.render("OK", True, Color("black"))
        textPos = text.get_rect()
        textPos.center = self.okUpgradeRect.center
        okButton.blit(text, textPos)
        self.okUpgradeRect.bottom = self.upgradeBox.get_rect().height - 10
        self.okUpgradeRect.centerx = self.upgradeBox.get_rect().centerx
        self.upgradeBox.blit(okButton, self.okUpgradeRect)

        # Display on game board.
        self.upgradeDisplayed = True
        Turn.upgradeSurface.blit(self.upgradeBox, (0, 0))


    def checkUpgrades(self, x, y):
        """
        Within the upgrades display window, handles the display of checkboxes
        (toggling between checked and unchecked) as the player clicks them.
        """
        for i in range(len(self.bachelors)):
            if self.bachelorCheckboxes[i].setChecked(x - Turn.upgradeRect.x,
                                                     y - Turn.upgradeRect.y):
                self.bachelorCheckboxes[i].draw()
                Turn.upgradeSurface.blit(self.upgradeBox, (0, 0))
                
        for i in range(len(self.masters)):
            if self.masterCheckboxes[i].setChecked(x - Turn.upgradeRect.x,
                                                     y - Turn.upgradeRect.y):
                self.masterCheckboxes[i].draw()
                Turn.upgradeSurface.blit(self.upgradeBox, (0, 0))
                
        for i in range(len(self.doctorates)):
            if self.doctorateCheckboxes[i].setChecked(x - Turn.upgradeRect.x,
                                                     y - Turn.upgradeRect.y):
                self.doctorateCheckboxes[i].draw()
                Turn.upgradeSurface.blit(self.upgradeBox, (0, 0))                


    def upgrade(self):
        """
        This method is called when the player clicks OK in the upgrades
        window.  For any upgrades that are checked, it upgrades those buildings
        and charges the player the appropriate amount.
        """
        for i in range(len(self.bachelors)):
            if self.bachelorCheckboxes[i].getChecked():
                building = Turn.buildings.getBuilding(self.bachelors[i])
                self.player.subtractDollars(100000)
                self.player.addPointsPerRound(1)
                building.setDegreeLvl("Bachelor")

        for i in range(len(self.masters)):
            if self.masterCheckboxes[i].getChecked():
                building = Turn.buildings.getBuilding(self.masters[i])
                if building.getDegreeLvl() == "Associate":
                    self.player.subtractDollars(250000)
                    self.player.addPointsPerRound(2)
                else:
                    self.player.subtractDollars(150000)
                    self.player.addPointsPerRound(1)
                building.setDegreeLvl("Master")

        for i in range(len(self.doctorates)):
            if self.doctorateCheckboxes[i].getChecked():
                building = Turn.buildings.getBuilding(self.doctorates[i])
                if building.getDegreeLvl() == "Associate":
                    self.player.subtractDollars(500000)
                    self.player.addPointsPerRound(3)
                elif building.getDegreeLvl() == "Bachelor":
                    self.player.subtractDollars(400000)
                    self.player.addPointsPerRound(2)
                else:
                    self.player.subtractDollars(250000)
                    self.player.addPointsPerRound(1)
                building.setDegreeLvl("Doctorate")
     
