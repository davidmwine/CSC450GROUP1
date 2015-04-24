import pygame, sys, random, os
from Building import Buildings

class Cards():
    def __init__(self, parent):
        self.parent = parent
        self.width = self.parent.get_width()//7
        self.height = self.parent.get_height()//4
        self.area = parent.subsurface((self.parent.get_width()//2 - self.width//2), 
                (self.parent.get_height()//2 - self.height//2), self.width, self.height)
        self.cardDeck = []
        self.cardsInDeck = 2  #Number of cards in the deck
        self.cardPos = 0  #Card position(index) in the deck
        self.initDeck()
        self.loadImages()

        self.movementCard = False

    def getXPosition(self):
        return self.area.get_offset()[0]

    def getYPosition(self):
        return self.area.get_offset()[1]

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height
        
    def initDeck(self):
        for card in range(self.cardsInDeck):
            self.cardDeck.append(card)
        random.shuffle(self.cardDeck)
        
    def fontOp(self, size, fontName):  #Duplicated from msu_game.py
        if fontName == "helvetica":
            fontAndSize = pygame.font.Font(os.path.join("font","helvetica.otf"),size)
        elif fontName == "berlin":
            fontAndSize = pygame.font.Font(os.path.join("font","berlin.ttf"),size)
        return fontAndSize

    def loadImages(self):
        self.imgCard = pygame.image.load(os.path.join("img","card.png")).convert_alpha()
        self.imgCardBack = pygame.image.load(os.path.join("img","card_back.png")).convert_alpha()

    def cardDescription(self, card):
        if card == 0:
            text = "Go to Accreditation Review."
        if card == 1:
            text = "Go enjoy a baseball game at Hammons Field."
            
        '''
        if card == 0:
            text = "Move back 3 spaces and stuff. You are going the wrong way."
        if card == 1:
            text = "Here's a nice puppy to play with."
        if card == 2:
            text = "Another place holder. Really is."
        if card == 3:
            text = "More card stuff with fancy people words."
        if card == 4:    
            text = "Proceed to the dump."
        if card == 5:
            text = "Get abducted by aliens... again."
        '''    
        return text


    def performAction(self, card, player):
        """Performs the action printed on the card that was drawn."""
        self.player = player    # the player who drew the card
        if card == 0:
            self.goToSpace("Accreditation Review")
        if card == 1:
            self.goToSpace("Hammons Field")


    def displayCard(self, card, scale):
        if card == "back":
            self.area.blit(pygame.transform.scale(self.imgCardBack,(self.width,
                        self.height)),(0,0))
        else:
            #Get the card text
            self.cardText = self.cardDescription(card) 

            self.area.blit(pygame.transform.scale(self.imgCard,(self.width,
                        self.height)),(0,0))
            
            #Print text on cards   
            lineText=""
            word = ""
            textEdge = 15 #Text boundary on card -> right side 
            characterCounter = 0 
            fontSize = int(27*scale)
            padding = 0
            paddingIncrement = int(30*scale)
            margin = 7
            textColor = (35,35,35)
            for character in self.cardText:
                characterCounter += 1
                if characterCounter == len(self.cardText):
                    if len(lineText + word + character) >= textEdge:
                        textout = self.fontOp(fontSize, "berlin").render(lineText, True, textColor)
                        self.area.blit(textout,(margin,margin + padding))
                        lineText = word + character
                        padding += paddingIncrement
                        textout = self.fontOp(fontSize, "berlin").render(lineText, True, textColor)
                        self.area.blit(textout,(margin,margin + padding))
                    else:
                        lineText += word + character
                        textout = self.fontOp(fontSize, "berlin").render(lineText, True, textColor)
                        self.area.blit(textout,(margin,margin + padding))
                if character != " ":
                    word += character
                if character == " ":
                    if len(lineText + word + character) >= textEdge:
                        textout = self.fontOp(fontSize, "berlin").render(lineText, True, textColor)
                        self.area.blit(textout,(margin,margin + padding))
                        lineText = word + character
                        padding += paddingIncrement
                    else:
                        lineText += word + character
                    word = ""
    
    def drawCard(self, scale, player):
        self.player = player    # the player who drew this card
        
        if self.cardPos == len(self.cardDeck):
            random.shuffle(self.cardDeck)
            self.cardPos = 0
        card = self.cardDeck[self.cardPos]
        self.cardPos += 1
        self.displayCard(card, scale)
        return card


    # Methods for card actions
    
    def goToSpace(self, destination):
        """
        Moves player's token to destination. If player passes Carrington,
        he/she gets $200,000. Arranges for an action to be taken based on
        the destination space.
        """
        playerPosition = self.player.getPosition()
        destinationPosition = Buildings().getBuilding(destination).getSequence()
        if destinationPosition > playerPosition:
            spaces = destinationPosition - playerPosition
        else:
            spaces = Buildings().getNumBuildings() + destinationPosition - playerPosition
        self.player.increasePosition(spaces)
        self.movementCard = True
        

        
