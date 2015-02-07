import pygame, sys
from pygame.locals import *



def window():
    '''Creates a 800x600 main window'''
    pygame.init()
    size = 800, 600
    screen = pygame.display.set_mode(size)    
    return screen
    

def chatBox(screen):
    '''Takes a 800x600 main window(surface obj)  and Puts a 600x100 chat
    box at the bottom. Returns the surface.'''
    size_rect = pygame.Rect((0, 500), (600,100))
    chatbox = screen.subsurface(size_rect)
    return chatbox



def userInterface(screen):
    '''Takes a 800x600 main window(surface obj) and puts a 150x600 ui
    box on the left side.  Returns the surface'''
    size_rect = pygame.Rect((600,0), (200, 600))
    UI = screen.subsurface(size_rect)
    return UI


def game(windows):
    '''Takes a dict with a "screen", "chatbox", and "userinterface"
    entries and inits them, makes the chatbox and UI white'''
    screen = windows["screen"]
    chatbox = windows["chatbox"]
    UI = windows["userinterface"]
    while 1:
        chatbox.fill((255,255,255))
        UI.fill((255,255,255))
        pygame.display.flip()
        screen.togglefullscreen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0
    


def main():
    windows = dict()
    windows["screen"] = window()
    screen = windows["screen"]
    windows["chatbox"] = chatBox(screen)
    windows["userinterface"] = userInterface(screen)
    game(windows)

if __name__ == '__main__':
        main()
