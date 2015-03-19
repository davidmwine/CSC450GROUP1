import pygame, sys, random, os

class Cards():
    def __init__(self, parent):
        self.parent = parent
        self.width = self.parent.get_width()//7
        self.height = self.parent.get_height()//4
        self.area = parent.subsurface((self.parent.get_width()//7), 
                (self.parent.get_height()//2 - self.height//2), self.width, self.height)
        self.carddeck = []
        self.cardsindeck = 6  #Number of cards in the deck
        self.cardpos = 0  #Card position(index) in the deck
        self.initDeck()
        self.loadImages()
        
    def initDeck(self):
        for card in range(self.cardsindeck):
            self.carddeck.append(card)
        random.shuffle(self.carddeck)
        
    def fontOp(self, size, fontname):  #Duplicated from msu_game.py
        if fontname == "helvetica":
            fontsized = pygame.font.Font(os.path.join("font","helvetica.otf"),size)
        elif fontname == "berlin":
            fontsized = pygame.font.Font(os.path.join("font","berlin.ttf"),size)
        return fontsized

    def loadImages(self):
        self.imgcard = pygame.image.load(os.path.join("img","card.png")).convert_alpha()
        self.imgcardback = pygame.image.load(os.path.join("img","card_back.png")).convert_alpha()

    def cardDescription(self, card):
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
        return text

    def displayCard(self, card, scale):
        if card == "back":
            self.area.blit(pygame.transform.scale(self.imgcardback,(self.width,
                        self.height)),(0,0))
        else:
            #Get the card text
            self.cardtext = self.cardDescription(card) 

            self.area.blit(pygame.transform.scale(self.imgcard,(self.width,
                        self.height)),(0,0))
            
            #Print text on cards   
            linetext=""
            word = ""
            textedge = 15 #Text boundary on card -> right side 
            charactercounter = 0 
            fontsize = int(27*scale)
            padding = 0
            paddingincrement = int(30*scale)
            margin = 7
            textcolor = (35,35,35)
            for character in self.cardtext:
                charactercounter += 1
                if charactercounter == len(self.cardtext):
                    if len(linetext + word + character) >= textedge:
                        textout = self.fontOp(fontsize, "berlin").render(linetext, True, textcolor)
                        self.area.blit(textout,(margin,margin + padding))
                        linetext = word + character
                        padding += paddingincrement
                        textout = self.fontOp(fontsize, "berlin").render(linetext, True, textcolor)
                        self.area.blit(textout,(margin,margin + padding))
                    else:
                        linetext += word + character
                        textout = self.fontOp(fontsize, "berlin").render(linetext, True, textcolor)
                        self.area.blit(textout,(margin,margin + padding))
                if character != " ":
                    word += character
                if character == " ":
                    if len(linetext + word + character) >= textedge:
                        textout = self.fontOp(fontsize, "berlin").render(linetext, True, textcolor)
                        self.area.blit(textout,(margin,margin + padding))
                        linetext = word + character
                        padding += paddingincrement
                    else:
                        linetext += word + character
                    word = ""
    
    def draw_card(self, scale):
        if self.cardpos == len(self.carddeck):
            random.shuffle(self.carddeck)
            self.cardpos = 0
        card = self.carddeck[self.cardpos]
        self.cardpos += 1
        self.displayCard(card, scale)
        return card
        
