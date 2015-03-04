import pygame, sys
from pygame.locals import *
from player import Player
from building import Building
from globals import Globals
from playersDisplay import PlayersDisplay
from board import GameBoard
from Controls import Controls
from ChatBox import chatBox
from Dice import Dice
from popupMenu import popupMenu


class GameArea(object):


    def __init__(self, parent=False, scale=1):

        self.width = int(scale*1920)
        self.height = int(scale*1080)
        self.scale = scale
        self.parent = parent
        self.clock = pygame.time.Clock()
        self.typing = False
        self.roll = (0,0)
        self.roll_time = 501

        if self.parent:
            self.area = pygame.Surface((self.width, self.height))
        else:
            pygame.init()
            self.area = pygame.display.set_mode((self.width, self.height))

        # Game Board
        rect = pygame.Rect((0, 0), (1440*self.scale, 1020*self.scale))
        self.boardArea = self.area.subsurface(rect)
        self.boardArea.fill(Globals.maroon) 

        self.gameBoard = GameBoard(self.scale, True)
            
        # Players Display
        self.playerDis = PlayersDisplay(testplayers(), self.scale, True)

        # Chat Box
        rect = pygame.Rect((1440*self.scale, 810*self.scale),
                           (480*self.scale, 270*self.scale))
        self.chatbox = chatBox(self.scale,self.area, rect)
        
        # Controls
        rect = pygame.Rect((0, 1020*self.scale),
                           (1440*self.scale, 60*self.scale))
        self.controls = Controls(self.area, rect)

        #Dice
        self.dice = Dice(self.boardArea)

        # Popup options menu
        self.popupMenu = popupMenu(self.boardArea)


    def get_area(self):
        return self.area

    def getScale(self):
        return self.scale

    def mouseClick(self):
        mouseX,mouseY = pygame.mouse.get_pos()

        # menu not open
        if not self.popupMenu.getPopupActive():
            if mouseX > self.controls.get_width()/4\
            and mouseX < self.controls.get_width()/2\
            and mouseY > self.height-self.controls.get_height():
                self.roll = (1,0)
            if mouseX > self.chatbox.getLeft() and mouseX < self.chatbox.getRight()\
            and mouseY > self.chatbox.getTopType()\
            and mouseY < self.chatbox.getBottomType():
                self.typing = True
            if mouseX > 0 and mouseX < self.controls.get_width() / 4 and mouseY > self.height - self.controls.get_height():
                self.popupMenu.setPopupActive(True)
                self.popupMenu.make_popup_menu()

        # menu open
        else:
            # not in game options
            if not self.popupMenu.getOptionsActive():
                # not exiting game
                if not self.popupMenu.getExitCheckActive():
                    # resume game
                    if mouseX > self.boardArea.get_width() / 2 - 100 and mouseX < self.boardArea.get_width() / 2 + 100\
                        and mouseY > self.boardArea.get_height() / 2 - 80 and mouseY < self.boardArea.get_height() / 2 - 50:
                        self.popupMenu.setPopupActive(False)
                        rect = pygame.Rect((20*self.scale, 20*self.scale),
                                (1400*self.scale, 980*self.scale))
                        self.area.blit(self.gameBoard.getGB(), rect)
                    # save game
                    if mouseX > self.boardArea.get_width() / 2 - 100 and mouseX < self.boardArea.get_width() / 2 + 100\
                        and mouseY > self.boardArea.get_height() / 2 - 40 and mouseY < self.boardArea.get_height() / 2 - 10:
                        pass # NEED TO IMPLEMENT
                    # game options
                    if mouseX > self.boardArea.get_width() / 2 - 100 and mouseX < self.boardArea.get_width() / 2 + 100\
                        and mouseY > self.boardArea.get_height() / 2 and mouseY < self.boardArea.get_height() / 2 + 30:
                        self.popupMenu.setOptionsActive(True)
                        self.popupMenu.game_options()
                    # exit game (maybe implement a double check?)
                    if mouseX > self.boardArea.get_width() / 2 - 100 and mouseX < self.boardArea.get_width() / 2 + 100\
                        and mouseY > self.boardArea.get_height() / 2 + 40 and mouseY < self.boardArea.get_height() / 2 + 70:
                        self.popupMenu.setExitCheckActive(True)
                        self.popupMenu.exit_check()
                # exit double check
                else:
                    if mouseX > self.boardArea.get_width() / 2 - 100 and mouseX < self.boardArea.get_width() / 2 + 100\
                        and mouseY > self.boardArea.get_height() / 2 - 60 and mouseY < self.boardArea.get_height() / 2 - 30:
                        pygame.quit()
                        sys.exit()
                    if mouseX > self.boardArea.get_width() / 2 - 100 and mouseX < self.boardArea.get_width() / 2 + 100\
                        and mouseY > self.boardArea.get_height() / 2 - 20 and mouseY < self.boardArea.get_height() / 2 + 10:
                        self.popupMenu.setExitCheckActive(False)
                        self.popupMenu.make_popup_menu()


            # in game options
            else:
                change = self.popupMenu.change_resolution(mouseX, mouseY)
                if not change == None:
                    self.area = pygame.display.set_mode(change)
                if mouseX > self.boardArea.get_width() / 2 - 100 and mouseX < self.boardArea.get_width() / 2 + 100\
                    and mouseY > self.boardArea.get_height() / 2 - 80 and mouseY < self.boardArea.get_height() / 2 - 50:
                    self.popupMenu.setOptionsActive(False)
                    self.popupMenu.make_popup_menu()

    def play(self):
        game_exit = False
        # Insert Players Display
        rect = pygame.Rect((1440*self.scale, 0),
                           (480*self.scale, 810*self.scale))
        self.area.blit(self.playerDis.getPD(), rect)

        # Insert Game Board
        rect = pygame.Rect((20*self.scale, 20*self.scale),
                           (1400*self.scale, 980*self.scale))
        self.area.blit(self.gameBoard.getGB(), rect)

        
            
        pygame.key.set_repeat(75, 75)
        while not game_exit:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    self.mouseClick()
                elif event.type == KEYDOWN and not self.typing: #TEMPORARY, will later replace with proper game exit
                    if event.key == K_ESCAPE:
                        game_exit = True
                        break
                elif event.type == KEYDOWN and self.typing:
                    if event.key == K_ESCAPE:
                        self.typing = False
                    elif event.key == K_RETURN:
                        self.chatbox.submitText()
                    elif event.key == K_BACKSPACE:
                        self.chatbox.deleteText()
                    else:
                        self.chatbox.typeText(pygame.key.name(event.key))
                        
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    return 0
            self.roll_time += self.clock.get_time()
            if self.roll[0] and self.roll_time>250:
                self.roll = self.dice.roll()
                self.roll_time = 0
            if self.parent:
                self.parent.blit(self.area, (0,0))
            pygame.display.update()
        return "start"
        

def testplayers():
    p1 = Player("player1", "Agriculture")
    p2 = Player("player2", "Arts and Letters")
    p3 = Player("player3", "Natural and Applied Sciences")
    p4 = Player("player4", "Education")
    p5 = Player("player5", "Health and Human Services")
    p6 = Player("player6", "Humanities and Public Affairs")
        
    p2.addDollars(120000000)
    
    return [p1, p2, p3, p4, p5, p6]



def main():
    screen = GameArea(False, 1/3)
    screen.play()



if __name__ == "__main__":
    main()








        
        
            
