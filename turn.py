import random
from player import Player
from buildings import Buildings


class Turn(object):

    def __init__(self, player):
        self.player = player


    def trade(self):
        pass

    def rollDice(self):
        # This should integrate (through the network?) with the Dice class...
        r1 = random.randint(1, 6)
        r2 = random.randint(1, 6)
        return r1 + r2

    def moveToken(self, spaces):
        self.player.increasePosition(spaces)

    def chargeFees(self, owner, fees):
        """If building is already owned, fees are paid to owner."""
        self.player.subtractDollars(fees)
        owner.addDollars(fees)

    def displayFeeMsg(self, ownerName, fees):
        # This should eventually display a message on the game board
        # or in a pop-up.
        print("You just paid $" + str(fees) + " to " + ownerName)

    def displayChoiceToBuy(self, buildingName):
        """If building is unowned, give player a choice to buy it."""
        # This should eventually show up on the game board or in a pop-up.
        return input("Would you like to buy " + buildingName + "? (y/n) ")

    def buy(self, building):
        self.player.subtractDollars(building.getPrice())
        self.player.addBuilding(building)
        building.setOwner(self.player)
        building.setColor(self.player.getColor())



def main():
    p1 = Player("player1", "Education")
    p2 = Player("player2", "Arts and Letters")
    p3 = Player("player3", "Natural and Applied Sciences")

    players = [p1, p2, p3]

    buildings = Buildings().getBuildingList()

    numTurns = int(input("How many turns would you like to play? "))
    for i in range(numTurns):
        player = players[i % len(players)]
        turn = Turn(player)
        roll = turn.rollDice()
        turn.moveToken(roll)
        position = player.getPosition()
        currentBuilding = buildings[position]
        
        print("---------------------------------------------------------------")
        print(player.getName())
        print(roll)
        print(position)
        print(currentBuilding.getName())

        purpose = currentBuilding.getPurpose()
        owner = currentBuilding.getOwner()
        if purpose != "special":
            if owner == "Unowned":
                choice = turn.displayChoiceToBuy(currentBuilding.getName())
                if choice == "y":
                    turn.buy(currentBuilding)
            elif owner != player:
                fees = currentBuilding.getFeeAmount()
                turn.chargeFees(owner, fees)
                turn.displayFeeMsg(owner.getName(), fees)

    for i in range(len(players)):
        print("===============================================================")
        print(players[i].getName())
        print('$' + str(players[i].getDollars()))
        print(players[i].getBuildingNames())
    

if __name__ == '__main__':
    main() 
