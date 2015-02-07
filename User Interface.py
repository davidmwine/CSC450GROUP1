import pygame, sys
from pygame.locals import *



def window():
    pygame.init()
    size = 200, 800
    speed = [2, 2]
    white = 255, 255, 255
    screen = pygame.display.set_mode(size)
    while 1:
        screen.fill(white)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()



def main():
    window()

main()
