import pygame, sys
from player import Player
from playersDisplay import PlayersDisplay
from pygame.locals import *



def window():
    '''Creates a 800x600 main window'''
    pygame.init()
    size = 800, 600
    screen = pygame.display.set_mode(size)    
    return screen
    

def chatBox(screen):
    '''Takes a 800x600 main window(surface obj) and puts a 600x100 chat
    box at the bottom. Returns the surface.'''
    size_rect = pygame.Rect((0, 500), (600,100))
    chatbox = screen.subsurface(size_rect)
    return chatbox



def userInterface(screen):
    '''Takes a 800x600 main window(surface obj) and puts a 150x600 ui
    box on the right side.  Returns the surface'''
    size_rect = pygame.Rect((600,0), (200, 600))
    UI = screen.subsurface(size_rect)
    return UI


def game(windows):
    '''Takes a dict with a "screen", "chatbox", and "userinterface"
    entries and inits them, makes the chatbox and UI white'''
    screen = windows["screen"]
    chatbox = windows["chatbox"]
    UI = windows["userinterface"]
    #UI.insert(0, 0)
    rect = pygame.Rect((600,0), (200, 600))
    screen.blit(UI.getPD(), rect)
    while 1:
        chatbox.fill((255,255,255))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0

def players():
    '''players test function'''
    p1 = Player("player1", "Agriculture")
    p2 = Player("player2", "Arts and Letters")
    p3 = Player("player3", "Natural and Applied Sciences")
    p4 = Player("player4", "Health and Human Services")
    p5 = Player("player5", "Humanities and Public Affairs")
    p6 = Player("player6", "Education")
    
    p1.addBuilding('Siceluff')
    p1.addBuilding('Cheek')
    p1.addBuilding('Plaster Student Union')
    p1.addBuilding('Kemper')
    p1.addBuilding('Glass')
    p1.addBuilding('Strong')
    p1.addBuilding('Karls')
    p1.addBuilding('Ellis')
    p1.addBuilding('JQH Arena')
    p2.addBuilding('Temple')
    
    return [p1, p2, p3, p4, p5, p6]

    


def main():
    windows = dict()
    windows["screen"] = window()
    screen = windows["screen"]
    windows["chatbox"] = chatBox(screen)
    windows["userinterface"] = PlayersDisplay(players(), True)
    game(windows)
    

if __name__ == '__main__':
    main()
