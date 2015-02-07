import pygame, sys
from pygame.locals import *



def window():
    pygame.init()
    size = 800, 600
    speed = [2, 2]
    white = 255, 255, 255
    screen = pygame.display.set_mode(size)    
    return screen
    

def chatBox(screen):
    size_rect = pygame.Rect((0, 500), (600,100))
    chatbox = screen.subsurface(size_rect)
    return chatbox



def userInterface(screen):
    size_rect = pygame.Rect((600,0), (200, 600))
    UI = screen.subsurface(size_rect)
    return UI


def game(windows):
    screen = windows["screen"]
    chatbox = windows["chatbox"]
    UI = windows["userinterface"]
    while 1:
        chatbox.fill((255,255,255))
        UI.fill((255,255,255))
        pygame.display.flip()
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

main()
