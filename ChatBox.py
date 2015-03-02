import pygame, sys
from pygame.locals import *







class chatBox(object):
    
    def __init__(self, scale=1, parent=None , size_rect=None):
        self._RightEdge = 1920*scale
        self._BottomEdge = 1080*scale
        self._width = - size_rect.left + size_rect.right
        self._height = size_rect.bottom - size_rect.top
        self._line_width = self._width
        self._line_height = self._height/9
        self._scale = scale
        self._chatlines = []
        if parent != None:
            self._area = parent.subsurface(size_rect)

        self.draw_chat()


    def draw_chat(self):
        self._area.fill((255,255,255))
        self._chatenter = chatEnter(self._area,Rect(0 , self._line_height*8,
        self._line_width, self._line_height), None)
        '''for i in range(7,-1,-1):
            line_rect = Rect(3, i*self._line_height+1,
                        self._line_width-3, self._line_height-1)
            try:
                chatLine( self._area, line_rect, self._chatlines[i])
            except IndexError:
                chatLine(self._area, line_rect, "Line {}".format(i+1))'''
        pygame.draw.rect(self._area,(0,0,0), (0,0, self._area.get_width(),
                                              self._area.get_height()), 2)

    def getLeft(self):
        #print(self._area.get_rect().left)
        #print(self._RightEdge - self._area.get_width())
        return self._RightEdge - self._area.get_width()

    def getRight(self):
        #print(self._RightEdge)
        return self._RightEdge

    def getTopType(self):
        #print(self._BottomEdge - self._chatenter.getArea().get_rect().top)
        return self._BottomEdge - self._chatenter.getArea().get_height()

    def getBottomType(self):
        #print(self._BottomEdge)
        return self._BottomEdge

    def typeText(self, text):
        self._chatenter.appendText(text)

    def deleteText(self):
        self._chatenter.removeText()

    def submitText(self):
        newText = self._chatenter.getText()
        print(len(newText))
        for i in newText:
            self._chatlines.append(i)
        self._chatenter.setText("")
        for i in range(len(self._chatlines)):
            line_rect = Rect(7, i*self._line_height+5,
                        self._line_width-15, self._line_height-1)
            chatLine( self._area, line_rect, self._chatlines[i])

class chatLine(object):
    def __init__(self, parent, rect ,string= " "):
        self._text = string.format(len(string))
        self._width = rect.right - rect.left    
        self._height = rect.bottom - rect.top
        self._area = parent.subsurface(rect)
        self._area.fill((255,255,255))
        self._font = pygame.font.Font( None, self._height)
        self._textarea = self._font.render( self._text, 1, (0,0,0) )
        self._area.blit(self._textarea,(0,0))
        

    def get_area(self):
        return self._area

        



class chatEnter(object):
    def __init__ (self, parent,rect, action):
        self.lineIndex = 0
        self.currLineLen = 0
        self._height = rect.bottom - rect.top
        self._font = pygame.font.Font( None, self._height) #For testing width
        self.lines = ['']
        self._area = parent.subsurface(rect)
        self._area.fill((0xFF, 0xFF, 0xFF, 0xFF))
        pygame.draw.rect(self._area,(0,0,0), (0,0, self._area.get_width(),
                                              self._area.get_height()), 3)


    def chat(self):
        self.chatlines.append(chatLine(self._text))

    def curlyRemove(self):
        sizeL = 0
        sizeR = 0
        for i in self.lines[self.lineIndex]:
            if i == '{':
                sizeL += self._font.size('{')[0]
            elif i == '}':
                sizeR += self._font.size('}')[0]
        sizeTot = sizeL/2 + sizeR/2
        return sizeTot

    def appendText(self, newText):
        self.lines[self.lineIndex] += newText
        self.currLineLen += len(newText)
        if self.lines[self.lineIndex][-1] in ['{', '}']:
            self.currLineLen -= 1
        if self._font.size(self.lines[self.lineIndex])[0] - self.curlyRemove() > self._area.get_width()-5:
            self.currLineLen = 0
            lastSpace = self.lines[self.lineIndex].rfind(' ')
            if lastSpace > -1:
                newLineStart = self.lines[self.lineIndex][lastSpace+1:]
                self.lines[self.lineIndex] = self.lines[self.lineIndex][:lastSpace]
                self.lineIndex += 1
                self.lines.append(newLineStart)
                self.currLineLen = len(newLineStart)
            else:
                nextLine = self.lines[self.lineIndex][-1]
                if self.lines[self.lineIndex][-1] in ['{', '}']:
                    self.lines[self.lineIndex] = self.lines[self.lineIndex][:len(self.lines[self.lineIndex])-2]
                    self.lines.append(nextLine + nextLine)
                else:
                    self.lines[self.lineIndex] = self.lines[self.lineIndex][:len(self.lines[self.lineIndex-1])]
                    self.lines.append(nextLine)
                self.currLineLen = 1
                self.lineIndex += 1
            
        chatLine(self._area, self._area.get_rect(), self.lines[self.lineIndex])
        pygame.draw.rect(self._area,(0,0,0), (0,0, self._area.get_width(),
                                              self._area.get_height()), 3)

    def removeText(self):
        if len(self.lines[self.lineIndex]) < 1 and self.lineIndex == 0:
            return
        if self.lines[self.lineIndex][-1] in ['{', '}']:
            self.lines[self.lineIndex] = self.lines[self.lineIndex][0:-2]
        else:
            self.lines[self.lineIndex] = self.lines[self.lineIndex][0:-1]
        self.currLineLen -= 1
        if len(self.lines[self.lineIndex]) < 1 and self.lineIndex > 0:
            if self.lineIndex >= 0:
                self.lineIndex -= 1
                self.lines.pop()
        chatLine(self._area, self._area.get_rect(), self.lines[self.lineIndex])
        pygame.draw.rect(self._area,(0,0,0), (0,0, self._area.get_width(),
                                              self._area.get_height()), 3)

    def getArea(self):
        return self._area

    def getText(self):
        return self.lines

    def setText(self, newText):
        self.lines = [newText]
        self.lineIndex = 0
        self.currLineLen = 0
        chatLine(self._area, self._area.get_rect(), self.lines[self.lineIndex])
        pygame.draw.rect(self._area,(0,0,0), (0,0, self._area.get_width(),
                                              self._area.get_height()), 3)
            
        


def main():
    pass



if __name__ == "__main__":
    main()

