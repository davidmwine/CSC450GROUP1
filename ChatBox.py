import pygame, sys
from pygame.locals import *







class chatBox():
    
    def __init__(self, scale=1, parent=None , size_rect=None):

        self.width = - size_rect.left + size_rect.right
        self.height = size_rect.bottom - size_rect.top
        self.line_width = self.width
        self.line_height = self.height/9
        self.scale = scale
        self.chatlines = []
        if parent != None:
            self.area = parent.subsurface(size_rect)
        self.area.fill((0,255,0))
        self.chatenter = chatEnter(self.area,Rect(0 , self.line_height*8,
        self.line_width, self.line_height), None)
        for i in range(7):
            line_rect = Rect(0, i*self.line_height,
                        self.line_width, self.line_height)
            print(line_rect)
            self.chatlines.append(chatLine( self.area,line_rect
                                        ,"Line {}".format(i)))
                

class chatLine():
    def __init__(self, parent, rect ,string= ""):
        self._text = string
        self._width = rect.right - rect.left    
        self._height = rect.top - rect.bottom
        self._area = parent.subsurface(rect)
        self._font = pygame.font.Font( None, int(self._height))
        self._textarea = self._font.render( self._text, 1, (255,255,255) )
        print(self._textarea, rect, self._text)
        self._area.convert()
        self._area.blit(self._textarea,rect)
        

    def get_area(self):
        return self._area

        



class chatEnter():
    def __init__ (self, parent,rect, action):
        self._text = ""
        self._area = parent.subsurface(rect)
        self._area.fill((0,0,0))                                      


    def chat():
        self.chatlines.append(chatLine(self._text))
            
        


def main():
    pass



if __name__ == "__main__":
    main()

