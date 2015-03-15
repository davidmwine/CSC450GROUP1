import pygame
from pygame.locals import *
import sys
from player import Player
from buildings import Buildings
from globals import Globals
from playersDisplay import PlayersDisplay
from board import GameBoard
from Controls import Controls
from ChatBox import chatBox
from Dice import Dice
from popupMenu import popupMenu
from cards import Cards
from turn import Turn


class GameArea(object):


    def __init__(self, parent=False, scale=1):

        self.width = int(scale*1920)
        self.height = int(scale*1080)
        self.scale = scale
        self.parent = parent
        self.clock = pygame.time.Clock()
        self.roll = (0,0)   # self.roll[1] is the value of the roll
        self.roll_time = 501
        
        self.players = []       # List of players will be added in play()
        self.buildings = None   # List of buildings will be added in play()
        self.player = None      # Holds player whose turn it is
        self.building = None    # Holds building space that was landed on
                
        self.typing = False     # True if user is typing in chat box
        self.midTurn = False    # True if it's the middle of a player's turn
        self.gameExit = False
        self.card_draw = False
        self.diceRolled = False
        if self.parent:
            self.area = pygame.Surface((self.width, self.height))
        else:
            pygame.init()
            self.area = pygame.display.set_mode((self.width, self.height))

        self.font = pygame.font.Font(None, int(50*self.scale))    
        
        # Game Board Area
        rect = pygame.Rect((0, 0), (1440*self.scale, 1020*self.scale))
        self.boardArea = self.area.subsurface(rect)
        self.boardArea.fill(Globals.maroon) 
        
        # Chat Box
        rect = pygame.Rect((1440*self.scale, 810*self.scale),
                           (480*self.scale, 270*self.scale))
        self.chatbox = chatBox(self.scale,self.area, rect)
        
        # Controls
        rect = pygame.Rect((0, 1020*self.scale),
                           (1440*self.scale, 60*self.scale))
        self.controls = Controls(self.area, rect)

        # Dice
        self.dice = Dice(self.boardArea)

        # Popup options menu
        self.popupMenu = popupMenu(self.boardArea)

        #Cards
        self.cards = Cards(self.boardArea)

        # Message Rectangle
        self.msgRect = pygame.Rect(440*self.scale, 314*self.scale,
                                   560*self.scale, 392*self.scale)


    def getArea(self):
        return self.area


    def getScale(self):
        return self.scale


    def mouseClick(self):
        """Takes action based on when and where mouse has been clicked"""
        mouseX,mouseY = pygame.mouse.get_pos()

        # menu not open
        if not self.popupMenu.getPopupActive():             
            if mouseX > self.controls.get_width()/4\
            and mouseX < self.controls.get_width()/2\
            and mouseY > self.height-self.controls.get_height():
                self.roll = (1,0)
                self.diceRolled = True
                #self.redrawBoard()
                self.rollDice()
            #Chatbox
            if mouseX > self.chatbox.getLeft() and mouseX < self.chatbox.getRight()\
            and mouseY > self.chatbox.getTopType()\
            and mouseY < self.chatbox.getBottomType():
                self.typing = True
            else:
                self.typing = False

            # Menu Button
            if mouseX > 0 and mouseX < self.controls.get_width() / 4 \
            and mouseY > self.height - self.controls.get_height():
                self.popupMenu.setPopupActive(True)
                self.popupMenu.make_popup_menu()

            # Roll Button
            if mouseX > self.controls.get_width()/4\
            and mouseX < self.controls.get_width()/2\
            and mouseY > self.height-self.controls.get_height():
                self.roll = (1,0)
                self.diceRolled = True
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
                    self.turn.buy()
                    self.gameBoard.colorBuilding(self.turn.building)
                    self.turn.buyMsgDisplayed = False
                    self.endTurn()
                elif noRect.collidepoint(pygame.mouse.get_pos()):
                    self.turn.buyMsgDisplayed = False
                    self.redrawBoard()
                    self.endTurn()
            if mouseX > 0 and mouseX < self.controls.get_width() / 4 and mouseY > self.height - self.controls.get_height() and not self.diceRolled:
                self.popupMenu.setPopupActive(True)
                self.popupMenu.make_popup_menu()
            if self.okMsgDisplayed:
                okRect = pygame.Rect(self.msgRect.x + self.okRect.x,
                                 self.msgRect.y + self.okRect.y,
                                 self.okRect.width, self.okRect.height)
                if okRect.collidepoint(pygame.mouse.get_pos()):
                    self.okMsgDisplayed = False
                    self.redrawBoard()
                    self.endTurn()

        # menu open
        else:
            # not in game options
            if not self.popupMenu.getOptionsActive():
                # not exiting game
                if not self.popupMenu.getExitCheckActive():
                    # resume game
                    if mouseX > self.boardArea.get_width() / 2 - 100 \
                    and mouseX < self.boardArea.get_width() / 2 + 100 \
                    and mouseY > self.boardArea.get_height() / 2 - 80 \
                    and mouseY < self.boardArea.get_height() / 2 - 50:
                        self.popupMenu.setPopupActive(False)
                        self.refreshGameBoard()
                        if not self.diceRolled:
                            self.turn.beginTurn()
                        elif self.turn.buyMsgDisplayed or self.turn.okMsgDisplayed:
                            self.turn.handleLanding()
                        
                    # save game
                    if mouseX > self.boardArea.get_width() / 2 - 100 \
                    and mouseX < self.boardArea.get_width() / 2 + 100 \
                    and mouseY > self.boardArea.get_height() / 2 - 40 \
                    and mouseY < self.boardArea.get_height() / 2 - 10:
                        pass # NEED TO IMPLEMENT
                    # game options
                    if mouseX > self.boardArea.get_width() / 2 - 100 \
                    and mouseX < self.boardArea.get_width() / 2 + 100 \
                    and mouseY > self.boardArea.get_height() / 2 \
                    and mouseY < self.boardArea.get_height() / 2 + 30:
                        self.popupMenu.setOptionsActive(True)
                        self.popupMenu.game_options()
                    # exit game
                    if mouseX > self.boardArea.get_width() / 2 - 100 \
                    and mouseX < self.boardArea.get_width() / 2 + 100 \
                    and mouseY > self.boardArea.get_height() / 2 + 40 \
                    and mouseY < self.boardArea.get_height() / 2 + 70:
                        self.popupMenu.setExitCheckActive(True)
                        self.popupMenu.exit_check()
                # exit double check
                else:
                    # yes - exit
                    if mouseX > self.boardArea.get_width() / 2 - 100 \
                    and mouseX < self.boardArea.get_width() / 2 + 100 \
                    and mouseY > self.boardArea.get_height() / 2 - 60 \
                    and mouseY < self.boardArea.get_height() / 2 - 30:
                        pygame.quit()
                        sys.exit()
                    # no - go back to menu
                    if mouseX > self.boardArea.get_width() / 2 - 100 \
                    and mouseX < self.boardArea.get_width() / 2 + 100 \
                    and mouseY > self.boardArea.get_height() / 2 - 20 \
                    and mouseY < self.boardArea.get_height() / 2 + 10:
                        self.popupMenu.setExitCheckActive(False)
                        self.popupMenu.make_popup_menu()

            # in game options
            else:
                # change resolution (NOT WORKING)
                # problem is either
                #   1. Program not recognizing the radio button being checked
                #   2. Not changing resolution with the returned value
                change = self.popupMenu.change_resolution(mouseX, mouseY)
                if change != None:
                    self.area = pygame.display.set_mode(change)
                    self.popupMenu.load_buttons()
                # back to menu
                if mouseX > self.boardArea.get_width() / 2 - 100 \
                and mouseX < self.boardArea.get_width() / 2 + 100 \
                and mouseY > self.boardArea.get_height() / 2 - 80 \
                and mouseY < self.boardArea.get_height() / 2 - 50:
                    self.popupMenu.setOptionsActive(False)
                    self.popupMenu.make_popup_menu()

    def refreshGameBoard(self):
        rect = pygame.Rect((20*self.scale, 20*self.scale),
                           (1400*self.scale, 980*self.scale))
        self.area.blit(self.gameBoard.getGB(), rect)


    def refreshPlayersDisplay(self):
        rect = pygame.Rect((1440*self.scale, 0),
                           (480*self.scale, 810*self.scale))
        self.area.blit(self.playersDisplay.getPD(), rect)


    def refreshDisplay(self):
        if self.parent:    
            self.parent.blit(self.area, (0,0))
        pygame.display.update()

    '''def beginTurn(self):
        print("------- " + self.player.getName() + "'s turn -------")
        self.displayMsg(self.player.getName() + "'s turn. Click 'Roll'")'''


    def rollDice(self):
        while self.roll[0]>0:
            self.clock.tick(30)
            self.roll_time += self.clock.get_time()
            if self.roll_time>250:
                self.roll = self.dice.roll()
                self.roll_time = 0
                self.refreshDisplay()
        self.turn.setDiceRoll(self.roll[1])
        
        
    '''def endTurn(self):
        print("End of turn")
        self.midTurn = False
        self.diceRolled = False
        self.refreshPlayersDisplay()
        self.refreshGameBoard()

        # Create and position Yes and No buttons.
        yesButton = pygame.Surface((100*self.scale, 50*self.scale))
        yesButton.fill(Globals.medGray)
        self.yesRect = yesButton.get_rect()
        text = self.font.render("Yes", True, Color("black"))
        textPos = text.get_rect()
        textPos.center = self.yesRect.center
        yesButton.blit(text, textPos)
        self.yesRect.bottom = msgBox.get_rect().height - 10
        self.yesRect.left = 125*self.scale
        msgBox.blit(yesButton, self.yesRect)

        noButton = pygame.Surface((100*self.scale, 50*self.scale))
        noButton.fill(Globals.medGray)
        self.noRect = noButton.get_rect()
        text = self.font.render("No", True, Color("black"))
        textPos = text.get_rect()
        textPos.center = self.noRect.center
        noButton.blit(text, textPos)
        self.noRect.bottom = msgBox.get_rect().height - 10
        self.noRect.right = msgBox.get_rect().width - 125*self.scale
        msgBox.blit(noButton, self.noRect)
        
        # Position message box on the screen.
        self.msgRect = pygame.Rect(440*self.scale, 314*self.scale,
                        560*self.scale, 392*self.scale)
        self.area.blit(msgBox, self.msgRect)'''
        
     
    def displayMsgOK(self, msg):
        """Displays msg with OK button in the center of the game board."""        
        # Create message box as a surface and display text.
        msgBox = pygame.Surface((560*self.scale, 392*self.scale))
        msgBox.fill(Globals.lightGray)
        lines = wrapline(msg, self.font, 440*self.scale)
        i = 0
        for line in lines:
            lineYpos = 50*i*self.scale + 2
            line = self.font.render(line, True, Color("black"))
            msgBox.blit(line, (2, lineYpos))
            i += 1

        # Create and position OK button.
        okButton = pygame.Surface((100*self.scale, 50*self.scale))
        self.okRect = okButton.get_rect()
        okButton.fill(Globals.medGray)
        text = self.font.render("OK", True, Color("black"))
        textPos = text.get_rect()
        textPos.center = self.okRect.center
        okButton.blit(text, textPos)
        self.okRect.bottom = msgBox.get_rect().height - 10
        self.okRect.centerx = msgBox.get_rect().centerx
        msgBox.blit(okButton, self.okRect)
        
        # Position message box on the screen.
        self.msgRect = pygame.Rect(440*self.scale, 314*self.scale,
                        560*self.scale, 392*self.scale)
        self.area.blit(msgBox, self.msgRect) 

    def chatting(self, event):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789-=[];\'\\,./`'
        charsCaps = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ)!@#$%^&*(_+{}:"|<>?~'
        
        if event.key == K_ESCAPE:
            self.typing = False
            self.gameExit = True
        elif event.key == K_RETURN:
            self.chatbox.submitText()
        elif event.key == K_BACKSPACE:
            self.chatbox.deleteText()
        elif event.key <= 127 and event.key >= 32: #Only accept regular ascii characters (ignoring certain special characters)
            #self.chatbox.typeText(pygame.key.name(event.key))
            #self.chatbox.typeText(chr(event.key))
            checkCaps = pygame.key.get_pressed()
            if checkCaps[K_RSHIFT] or checkCaps[K_LSHIFT] and chr(event.key) in chars:
                index = chars.index(chr(event.key))
                if charsCaps[index] not in ['{', '}']:
                    self.chatbox.typeText(charsCaps[index])
                else:
                    self.chatbox.typeText(charsCaps[index] + charsCaps[index])
            elif checkCaps[K_CAPSLOCK]:
                index = chars.index(chr(event.key))
                if index < 26: #Only caps lock regular alphabet
                    self.chatbox.typeText(charsCaps[index])
                else:
                    self.chatbox.typeText(chr(event.key))
            else:
                self.chatbox.typeText(chr(event.key))

    def play(self):

        # This data will eventually be obtained from the lobby / setup menu.
        p1 = Player("player1", "Agriculture")
        p2 = Player("player2", "Arts and Letters")
        p3 = Player("player3", "Natural and Applied Sciences")
        p4 = Player("player4", "Education")
        p5 = Player("player5", "Health and Human Services")
        p6 = Player("player6", "Humanities and Public Affairs")

        self.players = [p1, p2, p3, p4, p5, p6]

        # Players Display
        self.playersDisplay = PlayersDisplay(self.players, self.scale, True)
        self.refreshPlayersDisplay()
        self.refreshDisplay()

        self.buildings = Buildings().getBuildingList()

        # Game Board
        self.gameBoard = GameBoard(self.scale, self.buildings, True)
        self.refreshGameBoard()
        self.refreshDisplay()
        # This needs to come after the game board is created, as creation of
        # the game board sets the rect attribute of the buildings.
        Turn.setStaticVariables(self.scale, self.area, self.buildings)
        pygame.key.set_repeat(75, 75)
        self.gameExit = False #Must be reset each time play is
        
        while not self.gameExit:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    self.mouseClick()
                if event.type == KEYDOWN and not self.typing: #TEMPORARY, will later replace with proper game exit
                    if event.key == K_ESCAPE:
                        self.gameExit = True
                        break
                    ###Cards demo - Remove Later ###
                    if event.key == K_c:
                        self.card_draw = True
                        self.current_card = self.cards.draw_card(self.scale)
                    ################################    
                if event.type == KEYDOWN and self.typing:
                    self.chatting(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    return 0

            if self.card_draw == False and not self.popupMenu.getPopupActive():
                self.cards.display_card("back", self.scale)
            elif not self.popupMenu.getPopupActive():
                self.cards.display_card(self.current_card, self.scale)
                
            if not self.midTurn:    # If it's a new player's turn...
                self.playersDisplay.updatePlayer(Turn.count % len(self.players))
                Turn.count += 1
                playerIndex = Turn.count % len(self.players)
                self.player = self.players[playerIndex]
                self.playersDisplay.selectPlayer(playerIndex)
                self.refreshPlayersDisplay()
                self.midTurn = True
                self.turn = Turn(self.player)
                self.turn.beginTurn()        
                
            self.roll_time += self.clock.get_time()
            if self.roll[0] and self.roll_time>250:
                self.roll = self.dice.roll()
                self.roll_time = 0
            if self.parent:
                self.parent.blit(self.area, (0,0))
                
            pygame.display.update()
            #next(self.sequence)     # Perform next action in player's turn       
            self.refreshDisplay()
            
        return "start"
        


def main():
    screen = GameArea(False, 0.5)
    screen.play()



if __name__ == "__main__":
    main()
