import pygame, sys
from pygame.locals import *







class chatBox():
    
    def __init__(self, scale=1, parent=None , size_rect=None):

        self._width = - size_rect.left + size_rect.right
        self._height = size_rect.bottom - size_rect.top
        self._line_width = self._width
        self._line_height = self._height/9
        self._scale = scale
        self._chatlines = ["Hey Foo, I do think itsworking, but i know its a demo",
                          "There are apoximatelly {} characters in this line",
                          "bar"
            ]
        if parent != None:
            self._area = parent.subsurface(size_rect)

        self.draw_chat()


    def draw_chat(self):
        self._area.fill((255,255,255))
        self._chatenter = chatEnter(self._area,Rect(0 , self._line_height*8,
        self._line_width, self._line_height), None)
        for i in range(7,-1,-1):
            line_rect = Rect(3, i*self._line_height+1,
                        self._line_width-3, self._line_height-1)
            try:
                chatLine( self._area, line_rect, self._chatlines[i])
            except IndexError:
                chatLine(self._area, line_rect, "Line {}".format(i+1))
        pygame.draw.rect(self._area,(0,0,0), (0,0, self._area.get_width(),
                                              self._area.get_height()), 2)

class chatLine():
    def __init__(self, parent, rect ,string= " "):
        self._text = string.format(len(string))
        self._width = rect.right - rect.left    
        self._height = rect.bottom - rect.top
        self._area = parent.subsurface(rect)
        self._area.fill((255,255,255))
        self._font = pygame.font.Font( None, 20)
        self._textarea = self._font.render( self._text, 1, (0,0,0) )
        self._area.blit(self._textarea,(0,0))
        

    def get_area(self):
        return self._area

        



class chatEnter():
    def __init__ (self, parent,rect, action):
        self._text = ""
        self._area = parent.subsurface(rect)
        self._area.fill((0x40, 0x40, 0x40, 0xFF))
        pygame.draw.rect(self._area,(0,0,0), (0,0, self._area.get_width(),
                                              self._area.get_height()), 3)


    def chat():
        self.chatlines.append(chatLine(self._text))
            
        


def main():
    pass



if __name__ == "__main__":
    main()

