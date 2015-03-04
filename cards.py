import pygame, sys, random, os

class Cards():
    def __init__(self, parent):
        self.parent = parent
        self.width = self.parent.get_width()//7
        self.height = self.parent.get_height()//4
        self.area = parent.subsurface((self.parent.get_width()//5), 
                (self.parent.get_height()//5), self.width, self.height)
        self.card_deck = []
        self.cards_in_deck = 6  #Number of cards in the deck
        self.card_pos = 0  #Card position(index) in the deck
        self.init_deck()
        self.load_images()
        
    def init_deck(self):
        for card in range(self.cards_in_deck):
            self.card_deck.append(card)
        random.shuffle(self.card_deck)
        
    def font_op(self, size, fontName):  #Duplicated from msu_game.py
        if fontName == "helvetica":
            fontAndSize = pygame.font.Font(os.path.join("font","helvetica.otf"),size)
        elif fontName == "berlin":
            fontAndSize = pygame.font.Font(os.path.join("font","berlin.ttf"),size)
        return fontAndSize

    def load_images(self):
        self.img_card = pygame.image.load(os.path.join("img","card.png")).convert_alpha()
        self.img_card_back = pygame.image.load(os.path.join("img","card_back.png")).convert_alpha()

    def card_description(self, card):
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

    def display_card(self, card, scale):
        if card == "back":
            self.area.blit(pygame.transform.scale(self.img_card_back,(self.width,
                        self.height)),(0,0))
        else:
            #Get the card text
            self.card_text = self.card_description(card) 

            self.area.blit(pygame.transform.scale(self.img_card,(self.width,
                        self.height)),(0,0))
            
            #Print text on cards   
            line_text=""
            word = ""
            text_edge = 15 #Text boundary on card -> right side 
            character_counter = 0 
            font_size = int(27*scale)
            padding = 0
            padding_increment = int(30*scale)
            margin = 7
            text_color = (35,35,35)
            for character in self.card_text:
                character_counter += 1
                if character_counter == len(self.card_text):
                    if len(line_text + word + character) >= text_edge:
                        text_out = self.font_op(font_size, "berlin").render(line_text, True, text_color)
                        self.area.blit(text_out,(margin,margin + padding))
                        line_text = word + character
                        padding += padding_increment
                        text_out = self.font_op(font_size, "berlin").render(line_text, True, text_color)
                        self.area.blit(text_out,(margin,margin + padding))
                    else:
                        line_text += word + character
                        text_out = self.font_op(font_size, "berlin").render(line_text, True, text_color)
                        self.area.blit(text_out,(margin,margin + padding))
                if character != " ":
                    word += character
                if character == " ":
                    if len(line_text + word + character) >= text_edge:
                        text_out = self.font_op(font_size, "berlin").render(line_text, True, text_color)
                        self.area.blit(text_out,(margin,margin + padding))
                        line_text = word + character
                        padding += padding_increment
                    else:
                        line_text += word + character
                    word = ""
    
    def draw_card(self, scale):
        if self.card_pos == len(self.card_deck):
            random.shuffle(self.card_deck)
            self.card_pos = 0
        card = self.card_deck[self.card_pos]
        self.card_pos += 1
        self.display_card(card, scale)
        return card
        
