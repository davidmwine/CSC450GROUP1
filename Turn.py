import pygame
from pygame.locals import *
from MessageBox import * # contains displayMsg(), displayMsgOK(), displayMsgYN()
from CheckBox import CheckBox


class Turn(object):
    """Contains most of the methods related to the game logic of a player's turn."""     

    def __init__(self, player):
        self.player = player
        self.roll = 0
        self.building = None    # Will hold building space that is landed on
        self.owner = None   # Will hold the owner of the building landed on
        self.feeAmt = None  # Will hold the fee for landing on a building
        self.buyMsgDisplayed = False
        self.okMsgDisplayed = False     # True if any OK message is displayed
        self.feeMsgDisplayed = False
        self.upgradeDisplayed = False   # True if upgrade screen is displayed


    @staticmethod
    def initializeTurnCount():
        Turn.count = -1     # This will be incremented to 0 for the first turn.


    @staticmethod
    def setStaticVariables(scale, parent, buildings):
        """
        These variables are used by and related to the other methods in this
        class, but are not closely related to individual players' turns
        (i.e., Turn instances).
        """
        Turn.scale = scale
        Turn.parent = parent
        Turn.buildings = buildings
        Turn.font = pygame.font.Font(None, int(50*scale))
        Turn.msgRect = pygame.Rect(440*scale, 250*scale,
                                   560*scale, 400*scale)
        Turn.smallMsgRect = pygame.Rect(440*scale, 250*scale,
                                   560*scale, 105*scale)
        Turn.upgradeRect = pygame.Rect(440*scale, 250*scale,
                                   560*scale, 540*scale)
        Turn.msgSurface = parent.subsurface(Turn.msgRect)
        Turn.smallMsgSurface = parent.subsurface(Turn.smallMsgRect)
        Turn.upgradeSurface = parent.subsurface(Turn.upgradeRect)


    def beginTurn(self):
        """
        Displays a message indicating which player's turn it is
        and giving instructions to roll the dice.
        """
        print("------- " + self.player.getName() + "'s turn -------")
        (size, msgBox) = displayMsg(Turn.scale, Turn.smallMsgRect, Turn.msgRect,
                Turn.font, self.player.getName() + "'s turn. Click 'Roll'")
        if (size == "small"):
            Turn.smallMsgSurface.blit(msgBox, (0, 0))
        else:    
            Turn.msgSurface.blit(msgBox, (0, 0))
            
        
    def setDiceRoll(self, roll):
        """
        Sets the value of the dice (as obtained from GameArea) for use in the
        Turn class.
        """
        print("Dice Rolled:", roll)
        self.roll = roll
        pygame.time.wait(1000)


    def handleLanding(self):
        """
        This method handles what comes next after a player lands on a space,
        (e.g., buying the building or paying fees to another player).
        """
        position = self.player.getPosition()
        self.building = Turn.buildings.getBuildingList()[position]
        print("Token landed on", self.building.getName())
        if self.building.getPurpose() == "special":
            (msgBox, self.okRect) = displayMsgOK(Turn.scale, Turn.msgRect,
                Turn.font, "Special message about " + self.building.getName())
            Turn.msgSurface.blit(msgBox, (0, 0))
            self.okMsgDisplayed = True
        else:    
            self.owner = self.building.getOwner()
            if self.owner == self.player:
                (msgBox, self.okRect) = displayMsgOK(Turn.scale, Turn.msgRect,
                    Turn.font, "You already own " + self.building.getName() + ".")
                Turn.msgSurface.blit(msgBox, (0, 0))
                self.okMsgDisplayed = True
            elif self.owner == None:
                (msgBox, self.yesRect, self.noRect) = displayMsgYN(
                    Turn.scale, Turn.msgRect, Turn.font,
                    "Do you want to buy " + self.building.getName() + "?")
                Turn.msgSurface.blit(msgBox, (0, 0))
                self.buyMsgDisplayed = True  
            elif self.owner != self.player:
                self.feeAmt = self.building.getFeeAmount()
                (msgBox, self.okRect) = displayMsgOK(Turn.scale, Turn.msgRect,
                    Turn.font, "You pay $" + str(self.feeAmt) + " to " +
                                self.owner.getName() + ".")
                Turn.msgSurface.blit(msgBox, (0, 0))
                self.okMsgDisplayed = True
                self.feeMsgDisplayed = True


    def buy(self):
        """Takes care of bookkeeping once player clicked Yes to buy building"""
        self.player.subtractDollars(self.building.getPrice())
        self.player.addBuilding(self.building)
        self.building.setOwner(self.player)
        self.building.setColor(self.player.getColor())


    def chargeFees(self):
        """If building is already owned, fees are paid to owner."""
        self.player.subtractDollars(self.feeAmt)
        self.owner.addDollars(self.feeAmt)


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
                building.setDegreeLvl("Bachelor")

        for i in range(len(self.masters)):
            if self.masterCheckboxes[i].getChecked():
                building = Turn.buildings.getBuilding(self.masters[i])
                if building.getDegreeLvl() == "Associate":
                    self.player.subtractDollars(250000)
                else:
                    self.player.subtractDollars(150000)
                building.setDegreeLvl("Master")

        for i in range(len(self.doctorates)):
            if self.doctorateCheckboxes[i].getChecked():
                building = Turn.buildings.getBuilding(self.doctorates[i])
                if building.getDegreeLvl() == "Associate":
                    self.player.subtractDollars(500000)
                elif building.getDegreeLvl() == "Bachelor":
                    self.player.subtractDollars(400000)
                else:
                    self.player.subtractDollars(250000)
                building.setDegreeLvl("Doctorate")
                
