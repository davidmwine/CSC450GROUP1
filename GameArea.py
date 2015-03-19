import pygame
from pygame.locals import *
import sys
from Player import Player
from Buildings import Buildings
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
        self.rolltime = 500 #Interval between dice roll updates in mS
        
        self.players = []       # List of players will be added in play()
        self.buildings = None   # List of buildings will be added in play()
        self.player = None      # Holds player whose turn it is
        self.building = None    # Holds building space that was landed on
                
        self.typing = False     # True if user is typing in chat box
        self.midturn = False    # True if it's the middle of a player's turn
        self.gameexit = False
        self.carddraw = False
        self.dicerolled = False
        
        if self.parent:
            self.area = pygame.Surface((self.width, self.height))
        else:
            pygame.init()
            self.area = pygame.display.set_mode((self.width, self.height))

        self.font = pygame.font.Font(None, int(50*self.scale))    
        
        # Game Board Area
        rect = pygame.Rect((0, 0), (1440*self.scale, 1020*self.scale))
        self.boardarea = self.area.subsurface(rect)
        self.boardarea.fill(Colors.MAROON) 
        
        # Chat Box
        rect = pygame.Rect((1440*self.scale, 810*self.scale),
                           (480*self.scale, 270*self.scale))
        self.chatbox = ChatBox(self.scale,self.area, rect)
        
        # Controls
        rect = pygame.Rect((0, 1020*self.scale),
                           (1440*self.scale, 60*self.scale))
        self.controls = Controls(self.area, rect)

        # Dice
        self.dice = Dice(self.boardarea)

        # Popup options menu
        self.popupMenu = PopupMenu(self.boardarea)

        #Cards
        self.cards = Cards(self.boardarea)

        # Message Rectangle
        self.msgrect = pygame.Rect(440*self.scale, 314*self.scale,
                                   560*self.scale, 392*self.scale)


    def getArea(self):
        return self.area


    def getScale(self):
        return self.scale


    def mouseClick(self):
        """Takes action based on when and where mouse has been clicked"""
        mousex,mousey = pygame.mouse.get_pos()

        # menu not open
        if not self.popupmenu.getPopupActive():             
            #Chatbox
            if mousex > self.chatbox.getLeft() and mousex < self.chatbox.getRight()\
            and mousey > self.chatbox.getTopType()\
            and mousey < self.chatbox.getBottomType():
                self.typing = True
            else:
                self.typing = False

            # Menu Button
            if mousex > 0 and mousex < self.controls.get_width() / 4 \
            and mousey > self.height - self.controls.get_height():
                self.popupmenu.setPopupActive(True)
                self.popupmenu.makePopupMenu()

            # Roll Button
            if mousex > self.controls.get_width()/4\
            and mousex < self.controls.get_width()/2\
            and mousey > self.height-self.controls.get_height():
                self.roll = (1,0)
                self.dicerolled = True
                self.rollDice()

            # OK Button in Message Box
            if self.turn.okmsgdisplayed:
                okrect = pygame.Rect(Turn.msgrect.x + self.turn.okrect.x,
                                 Turn.msgrect.y + self.turn.okrect.y,
                                 self.turn.okrect.width, self.turn.okrect.height)
                if okrect.collidepoint(pygame.mouse.get_pos()):
                    # If applicable, charge fees and update playersDisplay.
                    if self.turn.feemsgdisplayed:
                        self.turn.chargeFees()
                        self.playersdisplay.updatePlayer(
                            self.players.index(self.turn.owner))
                        self.turn.feemsgdisplayed = False
                    self.turn.okmsgdisplayed = False
                    self.endTurn()

            # Yes/No Button in Message Box
            if self.turn.buymsgdisplayed:
                yesrect = pygame.Rect(Turn.msgrect.x + self.turn.yesrect.x,
                                     Turn.msgrect.y + self.turn.yesrect.y,
                                     self.turn.yesrect.width, self.turn.yesrect.height)
                norect = pygame.Rect(Turn.msgrect.x + self.turn.norect.x,
                                     Turn.msgrect.y + self.turn.norect.y,
                                     self.turn.norect.width, self.turn.norect.height)
                if yesrect.collidepoint(pygame.mouse.get_pos()):
                    self.turn.buy()
                    self.gameboard.colorBuilding(self.turn.building)
                    self.turn.buymsgdisplayed = False
                    self.endTurn()
                elif norect.collidepoint(pygame.mouse.get_pos()):
                    self.turn.buymsgdisplayed = False
                    self.endTurn()
            if mousex > 0 and mousex < self.controls.get_width() / 4 and mousey > self.height - self.controls.get_height() and not self.dicerolled:
                self.popupmenu.setPopupActive(True)
                self.popupmenu.makePopupMenu()

        # menu open
        else:
            # not in game options
            if not self.popupmenu.getOptionsActive():
                # not exiting game
                if not self.popupmenu.getExitCheckActive():
                    # resume game
                    if mousex > self.boardarea.get_width() / 2 - 100 \
                    and mousex < self.boardarea.get_width() / 2 + 100 \
                    and mousey > self.boardarea.get_height() / 2 - 80 \
                    and mousey < self.boardarea.get_height() / 2 - 50:
                        self.popupmenu.setPopupActive(False)
                        self.refreshGameBoard()
                        if not self.dicerolled:
                            self.turn.beginTurn()
                        elif self.turn.buymsgdisplayed or self.turn.okmsgdisplayed:
                            self.turn.handleLanding()
                        
                    # save game
                    if mousex > self.boardarea.get_width() / 2 - 100 \
                    and mousex < self.boardarea.get_width() / 2 + 100 \
                    and mousey > self.boardarea.get_height() / 2 - 40 \
                    and mousey < self.boardarea.get_height() / 2 - 10:
                        pass # NEED TO IMPLEMENT
                    # game options
                    if mousex > self.boardarea.get_width() / 2 - 100 \
                    and mousex < self.boardarea.get_width() / 2 + 100 \
                    and mousey > self.boardarea.get_height() / 2 \
                    and mousey < self.boardarea.get_height() / 2 + 30:
                        self.popupmenu.setOptionsActive(True)
                        self.popupmenu.gameOptions()
                    # exit game
                    if mousex > self.boardarea.get_width() / 2 - 100 \
                    and mousex < self.boardarea.get_width() / 2 + 100 \
                    and mousey > self.boardarea.get_height() / 2 + 40 \
                    and mousey < self.boardarea.get_height() / 2 + 70:
                        self.popupmenu.setExitCheckActive(True)
                        self.popupmenu.exitCheck()
                # exit double check
                else:
                    # yes - exit
                    if mousex > self.boardarea.get_width() / 2 - 100 \
                    and mousex < self.boardarea.get_width() / 2 + 100 \
                    and mousey > self.boardarea.get_height() / 2 - 60 \
                    and mousey < self.boardarea.get_height() / 2 - 30:
                        pygame.quit()
                        sys.exit()
                    # no - go back to menu
                    if mousex > self.boardarea.get_width() / 2 - 100 \
                    and mousex < self.boardarea.get_width() / 2 + 100 \
                    and mousey > self.boardarea.get_height() / 2 - 20 \
                    and mousey < self.boardarea.get_height() / 2 + 10:
                        self.popupmenu.setExitCheckActive(False)
                        self.popupmenu.makePopupMenu()

            # in game options
            else:
                # change resolution (NOT WORKING)
                # problem is either
                #   1. Program not recognizing the radio button being checked
                #   2. Not changing resolution with the returned value
                change = self.popupmenu.changeResolution(mousex, mousey)
                if change != None:
                    self.area = pygame.display.set_mode(change)
                    self.popupmenu.loadButtons()
                # back to menu
                if mousex > self.boardarea.get_width() / 2 - 100 \
                and mousex < self.boardarea.get_width() / 2 + 100 \
                and mousey > self.boardarea.get_height() / 2 - 80 \
                and mousey < self.boardarea.get_height() / 2 - 50:
                    self.popupmenu.setOptionsActive(False)
                    self.popupmenu.makePopupMenu()

    def refreshGameBoard(self):
        rect = pygame.Rect((20*self.scale, 20*self.scale),
                           (1400*self.scale, 980*self.scale))
        self.area.blit(self.gameboard.getGB(), rect)


    def refreshPlayersDisplay(self):
        rect = pygame.Rect((1440*self.scale, 0),
                           (480*self.scale, 810*self.scale))
        self.area.blit(self.playersdisplay.getPD(), rect)


    def refreshDisplay(self):
        if self.parent:    
            self.parent.blit(self.area, (0,0))
        pygame.display.update()


    def rollDice(self):
        while self.roll[0]>0:
            self.clock.tick(30)
            self.rolltime += self.clock.get_time()
            if self.rolltime>250:
                self.roll = self.dice.roll()
                self.rolltime = 0
                self.refreshDisplay()
        self.turn.setDiceRoll(self.roll[1])
        
        
    def endTurn(self):
        print("End of turn")
        self.midturn = False
        self.dicerolled = False
        self.refreshPlayersDisplay()
        self.refreshGameBoard()
        
     
    def displayMsgOK(self, msg):
        """Displays msg with OK button in the center of the game board."""        
        # Create message box as a surface and display text.
        msgbox = pygame.Surface((560*self.scale, 392*self.scale))
        msgbox.fill(Colors.LIGHTGRAY)
        lines = wrapline(msg, self.font, 440*self.scale)
        i = 0
        for line in lines:
            lineypos = 50*i*self.scale + 2
            line = self.font.render(line, True, Color("black"))
            msgbox.blit(line, (2, lineypos))
            i += 1

        # Create and position OK button.
        okbutton = pygame.Surface((100*self.scale, 50*self.scale))
        self.okrect = okbutton.get_rect()
        okbutton.fill(Colors.MEDGRAY)
        text = self.font.render("OK", True, Color("black"))
        textpos = text.get_rect()
        textpos.center = self.okrect.center
        okbutton.blit(text, textpos)
        self.okrect.bottom = msgbox.get_rect().height - 10
        self.okrect.centerx = msgbox.get_rect().centerx
        msgBox.blit(okbutton, self.okrect)
        
        # Position message box on the screen.
        self.msgrect = pygame.Rect(440*self.scale, 314*self.scale,
                        560*self.scale, 392*self.scale)
        self.area.blit(msgbox, self.msgrect) 

    def chatting(self, event):
        CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789-=[];\'\\,./`'
        CHARSCAPS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ)!@#$%^&*(_+{}:"|<>?~'
        
        if event.key == K_ESCAPE:
            self.typing = False
            self.gameexit = True
        elif event.key == K_RETURN:
            self.chatbox.submitText()
        elif event.key == K_BACKSPACE:
            self.chatbox.deleteText()
        elif event.key <= 127 and event.key >= 32: #Only accept regular ascii characters (ignoring certain special characters)
            #self.chatbox.typeText(pygame.key.name(event.key))
            #self.chatbox.typeText(chr(event.key))
            checkcaps = pygame.key.get_pressed()
            if checkcaps[K_RSHIFT] or checkcaps[K_LSHIFT] and chr(event.key) in CHARS:
                index = CHARS.index(chr(event.key))
                if CHARSCAPS[index] not in ['{', '}']:
                    self.chatbox.typeText(CHARSCAPS[index])
                else:
                    self.chatbox.typeText(CHARSCAPS[index] + CHARSCAPS[index])
            elif checkcaps[K_CAPSLOCK]:
                index = CHARS.index(chr(event.key))
                if index < 26: #Only caps lock regular alphabet
                    self.chatbox.typeText(CHARSCAPS[index])
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
        self.playersdisplay = PlayersDisplay(self.players, self.scale, True)
        self.refreshPlayersDisplay()
        self.refreshDisplay()

        self.buildings = Buildings().getBuildingList()

        # Game Board
        self.gameboard = GameBoard(self.scale, self.buildings, True)
        self.refreshGameBoard()
        self.refreshDisplay()
        # This needs to come after the game board is created, as creation of
        # the game board sets the rect attribute of the buildings.
        Turn.setStaticVariables(self.scale, self.area, self.buildings)
        pygame.key.set_repeat(75, 75)
        self.gameexit = False #Must be reset each time play is
        
        while not self.gameexit:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    self.mouseClick()
                if event.type == KEYDOWN and not self.typing: #TEMPORARY, will later replace with proper game exit
                    if event.key == K_ESCAPE:
                        self.gameexit = True
                        break
                    ###Cards demo - Remove Later ###
                    if event.key == K_c:
                        self.carddraw = True
                        self.currentcard = self.cards.drawCard(self.scale)
                    ################################    
                if event.type == KEYDOWN and self.typing:
                    self.chatting(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    return 0

            if self.carddraw == False and not self.popupmenu.getPopupActive():
                self.cards.displayCard("back", self.scale)
            elif not self.popupmenu.getPopupActive():
                self.cards.displayCard(self.currentcard, self.scale)
                
            if not self.midturn:    # If it's a new player's turn...
                self.playersdisplay.updatePlayer(Turn.count % len(self.players))
                Turn.count += 1
                playerindex = Turn.count % len(self.players)
                self.player = self.players[playerindex]
                self.playersdisplay.selectPlayer(playerindex)
                self.refreshPlayersDisplay()
                self.midturn = True
                self.turn = Turn(self.player)
                self.turn.beginTurn()        
                
            self.rolltime += self.clock.get_time()
            if self.roll[0] and self.rolltime>250:
                self.roll = self.dice.roll()
                self.rolltime = 0
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
