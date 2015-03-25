import pygame
from pygame.locals import *
from messageBox import * # contains displayMsg(), displayMsgOK(), displayMsgYN()


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


    @staticmethod
    def setStaticVariables(scale, parent, buildings):
        """
        These variables are used by and related to the other methods in this
        class, but are not closely related to individual players' turns
        (i.e., Turn instances).
        """
        Turn.count = -1     # This will be incremented to 0 for the first turn.
        Turn.scale = scale
        Turn.parent = parent
        Turn.buildings = buildings
        Turn.font = pygame.font.Font(None, int(50*scale))
        Turn.msgRect = pygame.Rect(440*scale, 250*scale,
                                   560*scale, 400*scale)
        Turn.smallMsgRect = pygame.Rect(440*scale, 250*scale,
                                   560*scale, 105*scale)
        Turn.msgSurface = parent.subsurface(Turn.msgRect)
        Turn.smallMsgSurface = parent.subsurface(Turn.smallMsgRect)


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
        Turn class.  Passes to moving the token.
        """
        print("Dice Rolled:", roll)
        self.roll = roll
        self.moveToken()


    def moveToken(self):
        """Advances the token.  Called after the dice roll.""" 
        pygame.time.wait(1000)
        self.player.increasePosition(self.roll)
        position = self.player.getPosition()
        self.building = Turn.buildings[position]
        print("Token landed on", self.building.getName())
        self.handleLanding()


    def handleLanding(self):
        """
        This method handles what comes next after a player lands on a space,
        (e.g., buying the building or paying fees to another player).
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
        

