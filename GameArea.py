import pygame
from pygame.locals import *
import sys
from Player import Player
from Building import Buildings
import Colors
from PlayersDisplay import PlayersDisplay
from Board import GameBoard
from Controls import Controls
from ChatBox import ChatBox
from Dice import Dice
from PopupMenu import PopupMenu
from Cards import Cards
from Turn import Turn


class GameArea(object):


    def __init__(self, parent=False, scale=1):
        '''Overall function for the Game Area Screen.  Takes a parent
surface and scale as optional paramaters.  If no parent is
passed this will be the pygame screen, else it drawn on the
main screen.  Scale defaults to one, and must be one or less
and scales the screen accordingly where 1 is a 1920x1080 screen'''


        self.width = int(scale*1920)
        self.height = int(scale*1080)
        self.scale = scale
        self.parent = parent
        
        self.clock = pygame.time.Clock()
        self.roll = (0,0)   # self.roll[1] is the value of the roll
        self.rollTime = 500 #Interval between dice roll updates in mS
        
        self.players = []       # List of players will be added in play()
        self.buildings = None   # List of buildings will be added in play()
        self.player = None      # Holds player whose turn it is
        self.building = None    # Holds building space that was landed on
                
        self.typing = False     # True if user is typing in chat box
        self.midTurn = False    # True if it's the middle of a player's turn
        self.gameExit = False
        self.cardDraw = False
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
        mouseX,mouseY= pygame.mouse.get_pos()

        # menu not open
        if not self.popupMenu.getPopupActive():             
            #chatBox
            if mouseX > self.chatBox.getLeft() and mouseX < self.chatBox.getRight()\
            and mouseY> self.chatBox.getTopType()\
            and mouseY< self.chatBox.getBottomType():
                self.typing = True
            else:
                self.typing = False

            # Menu Button
            if mouseX > 0 and mouseX < self.controls.getWidth() / 4 \
            and mouseY> self.height - self.controls.getHeight():
                self.popupMenu.setPopupActive(True)
                self.popupMenu.makePopupMenu()

            # Roll Button
            if mouseX > self.controls.getWidth()/4\
            and mouseX < self.controls.getWidth()/2\
            and mouseY> self.height-self.controls.getHeight():
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
                    and mouseY> self.boardArea.get_height() / 2 - 80 \
                    and mouseY< self.boardArea.get_height() / 2 - 50:
                        self.popupMenu.setPopupActive(False)
                        self.refreshGameBoard()
                        if not self.diceRolled:
                            self.turn.beginTurn()
                        elif self.turn.buyMsgDisplayed or self.turn.okMsgDisplayed:
                            self.turn.handleLanding()
                        
                    # save game
                    if mouseX > self.boardArea.get_width() / 2 - 100 \
                    and mouseX < self.boardArea.get_width() / 2 + 100 \
                    and mouseY> self.boardArea.get_height() / 2 - 40 \
                    and mouseY< self.boardArea.get_height() / 2 - 10:
                        pass # NEED TO IMPLEMENT
                    # game options
                    if mouseX > self.boardArea.get_width() / 2 - 100 \
                    and mouseX < self.boardArea.get_width() / 2 + 100 \
                    and mouseY> self.boardArea.get_height() / 2 \
                    and mouseY< self.boardArea.get_height() / 2 + 30:
                        self.popupMenu.setOptionsActive(True)
                        self.popupMenu.gameOptions()
                    # exit game
                    if mouseX > self.boardArea.get_width() / 2 - 100 \
                    and mouseX < self.boardArea.get_width() / 2 + 100 \
                    and mouseY> self.boardArea.get_height() / 2 + 40 \
                    and mouseY< self.boardArea.get_height() / 2 + 70:
                        self.popupMenu.setExitCheckActive(True)
                        self.popupMenu.exitCheck()
                # exit double check
                else:
                    # yes - exit
                    if mouseX > self.boardArea.get_width() / 2 - 100 \
                    and mouseX < self.boardArea.get_width() / 2 + 100 \
                    and mouseY> self.boardArea.get_height() / 2 - 60 \
                    and mouseY< self.boardArea.get_height() / 2 - 30:
                        pygame.quit()
                        sys.exit()
                    # no - go back to menu
                    if mouseX > self.boardArea.get_width() / 2 - 100 \
                    and mouseX < self.boardArea.get_width() / 2 + 100 \
                    and mouseY> self.boardArea.get_height() / 2 - 20 \
                    and mouseY< self.boardArea.get_height() / 2 + 10:
                        self.popupMenu.setExitCheckActive(False)
                        self.popupMenu.makePopupMenu()

            # in game options
            else:
                # change resolution (NOT WORKING)
                # problem is either
                #   1. Program not recognizing the radio button being checked
                #   2. Not changing resolution with the returned value
                change = self.popupMenu.changeResolution(mouseX, mouseY)
                if change != None:
                    self.area = pygame.display.set_mode(change)
                    self.popupMenu.loadButtons()
                # back to menu
                if mouseX > self.boardArea.get_width() / 2 - 100 \
                and mouseX < self.boardArea.get_width() / 2 + 100 \
                and mouseY> self.boardArea.get_height() / 2 - 80 \
                and mouseY< self.boardArea.get_height() / 2 - 50:
                    self.popupMenu.setOptionsActive(False)
                    self.popupMenu.makePopupMenu()


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


    def rollDice(self):
        while self.roll[0]>0:
            self.clock.tick(30)
            self.rollTime += self.clock.get_time()
            if self.rollTime>250:
                self.roll = self.dice.roll()
                self.rollTime = 0
                self.refreshDisplay()
        self.turn.setDiceRoll(self.roll[1])
        
        
    def endTurn(self):
        print("End of turn")
        self.midTurn = False
        self.diceRolled = False
        self.refreshPlayersDisplay()
        self.refreshGameBoard()
        

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
            checkCaps = pygame.key.get_pressed()
            if checkCaps[K_RSHIFT] or checkCaps[K_LSHIFT] and chr(event.key) in CHARS:
                index = CHARS.index(chr(event.key))
                if CHARSCAPS[index] not in ['{', '}']:
                    self.chatBox.typeText(CHARSCAPS[index])
                else:
                    self.chatBox.typeText(CHARSCAPS[index] + CHARSCAPS[index])
            elif checkCaps[K_CAPSLOCK]:
                index = CHARS.index(chr(event.key))
                if index < 26: #Only caps lock regular alphabet
                    self.chatBox.typeText(CHARSCAPS[index])
                else:
                    self.chatBox.typeText(chr(event.key))
            else:
                self.chatBox.typeText(chr(event.key))

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
                        self.cardDraw = True
                        self.currentCard = self.cards.drawCard(self.scale)
                    ################################    
                if event.type == KEYDOWN and self.typing:
                    self.chatting(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    return 0

            if self.cardDraw == False and not self.popupMenu.getPopupActive():
                self.cards.displayCard("back", self.scale)
            elif not self.popupMenu.getPopupActive():
                self.cards.displayCard(self.currentCard, self.scale)
                
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
                
            self.refreshDisplay()
            
        return "start"
        


def main():
    screen = GameArea(False, 2/3)
    screen.play()



if __name__ == "__main__":
    main()
