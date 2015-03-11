import pygame
from pygame.locals import *
from messageBox import * # contains displayMsg(), displayMsgOK(), displayMsgYN()


class Turn(object):
    """Contains most of the methods related to the game logic of a player's turn."""

    @staticmethod
    def setStaticVariables(scale, parent, buildings):
        Turn.count = -1
        Turn.scale = scale
        Turn.parent = parent
        Turn.buildings = buildings
        Turn.font = pygame.font.Font(None, int(50*scale))
        Turn.msgRect = pygame.Rect(440*scale, 314*scale,
                                   560*scale, 392*scale)
        Turn.msgSurface = parent.subsurface(Turn.msgRect)
        

    def __init__(self, player):
        self.player = player
        self.roll = 0
        self.building = None    # Will hold building space that is landed on
        self.owner = None   # Will hold the owner of the building landed on
        self.buyMsgDisplayed = False
        self.okMsgDisplayed = False     # True if any OK message is displayed
        

    def beginTurn(self):
        print("------- " + self.player.getName() + "'s turn -------")
        msgBox = displayMsg(Turn.scale, Turn.msgRect, Turn.font,
                   self.player.getName() + "'s turn. Click 'Roll'")
        Turn.msgSurface.blit(msgBox, (0, 0))

        
    def setDiceRoll(self, roll):
        print("Dice Rolled:", roll)
        self.roll = roll
        self.moveToken()


    def moveToken(self):
        pygame.time.wait(1000)
        self.player.increasePosition(self.roll)
        position = self.player.getPosition()
        self.building = Turn.buildings[position]
        print("Token landed on", self.building.getName())
        self.handleLanding()


    def handleLanding(self):
        """
        This method handles what comes next after a player lands on a space,
        (e.g., buying the building or paying fees to another player)
        """
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
                self.chargeFees()


    def buy(self):
        """Takes care of bookkeeping once player clicked Yes to buy building"""
        self.player.subtractDollars(self.building.getPrice())
        self.player.addBuilding(self.building)
        self.building.setOwner(self.player)
        self.building.setColor(self.player.getColor())


    def chargeFees(self):
        """If building is already owned, fees are paid to owner."""
        feeAmt = self.building.getFeeAmount()
        self.player.subtractDollars(feeAmt)
        self.owner.addDollars(feeAmt)
        (msgBox, self.okRect) = displayMsgOK(Turn.scale, Turn.msgRect,
            Turn.font, "You pay $" + str(feeAmt) + " to " + self.owner.getName() + ".")
        Turn.msgSurface.blit(msgBox, (0, 0))
        self.okMsgDisplayed = True

