import pygame, sys
from pygame.locals import *







class chatBox():
    
    def __init__(self, scale=1, parent=None , size_rect=None):

        self.width = - size_rect.left + size_rect.right
        self.height = size_rect.bottom - size_rect.top
        self.line_width = self.width
        self.line_height = self.height/9
        self.scale = scale
        self.chatlines = ["Hey Foo, I do think itsworking, but i know its a demo",
                          "There are apoximatelly {} characters in this line",
                          "bar"
            ]
        if parent != None:
            self.area = parent.subsurface(size_rect)
        self.area.fill((0,255,0))
        self.draw_chat()


    def draw_chat(self):
        self.chatenter = chatEnter(self.area,Rect(0 , self.line_height*8,
        self.line_width, self.line_height), None)
        for i in range(7,-1,-1):
            line_rect = Rect(0, i*self.line_height,
                        self.line_width, self.line_height)
            try:
                chatLine( self.area, line_rect, self.chatlines[i])
            except IndexError:
                chatLine(self.area, line_rect, "Line {}".format(i+1))

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

