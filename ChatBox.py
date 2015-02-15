import pygame, sys
from pygame.locals import *







class chatBox():
    
    def __init__(self, scale=1, parent=None , size_rect=None):

        self.rect = size_rect
        self.scale = scale
        self.chatlines = []
        if parent != None:
            self.area = parent.subsurface(size_rect)
        else:
            pygame.init()
            self.area = pygame.display.set_mode((self.width, self.height))
        print(self.rect)
        print(self.area.get_size())
        self.chatenter = chatEnter(self.area,(self.rect.left,self.rect.top+self.rect.height*8/9,
                                              self.rect.width,self.rect.height/9 ), None)
        self.area.fill((0,255,0))

    class chatLine():
        def __init__(self, string= ""):
            self._text = string



        



class chatEnter():
    def __init__ (self, parent,rect, action):
        self._text = ""
        print(rect)
        self._area = parent.subsurface(rect)
        self._area.fill((255,255,255))                                          


    def chat():
        self.chatlines.append(chatLine(self._text))
            
        


def main():
    pass



if __name__ == "__main__":
    main()

