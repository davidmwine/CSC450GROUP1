import pygame, sys
from pygame.locals import *

class ChatBox(object):
    '''chatBox(scale=1, parent=None, size_rect=None)
    Create a chatbox with the given '''
    
    def __init__(self, scale=1, parent=None , sizeRect=None):
        self.rightEdge = 1920*scale
        self.bottomEdge = 1080*scale
        self.width = - sizeRect.left + sizeRect.right
        self.height = sizeRect.bottom - sizeRect.top
        self.lineWidth = self.width
        self.lineHeight = self.height/9
        self.scale = scale
        self.chatLines = []
        if parent != None:
            self.area = parent.subsurface(sizeRect)

        self.drawChat()


    def drawChat(self):
        self.area.fill((255,255,255))
        self.chatEnt = ChatEnter(self.area,Rect(0, self.lineHeight*8,
        self.lineWidth, self.lineHeight), None)
        '''for i in range(7,-1,-1):
            line_rect = Rect(3, i*self._line_height+1,
                        self._line_width-3, self._line_height-1)
            try:
                chatLine( self._area, line_rect, self._chatlines[i])
            except IndexError:
                chatLine(self._area, line_rect, "Line {}".format(i+1))'''
        pygame.draw.rect(self.area,(0,0,0), (0,0, self.area.get_width(),
                                              self.area.get_height()), 2)

    def getLeft(self):
        #print(self._area.get_rect().left)
        #print(self._RightEdge - self._area.get_width())
        return self.rightEdge - self.area.get_width()

    def getRight(self):
        #print(self._RightEdge)
        return self.rightEdge

    def getTopType(self):
        #print(self._BottomEdge - self._chatenter.getArea().get_rect().top)
        return self.bottomEdge - self.chatEnt.getArea().get_height()

    def getBottomType(self):
        #print(self._BottomEdge)
        return self.bottomEdge

    def typeText(self, text):
        self.chatEnt.appendText(text)

    def deleteText(self):
        self.chatEnt.removeText()

    def submitText(self):
        newText = self.chatEnt.getText()
        #print(len(newText))
        for i in newText:
            self.chatLines.append(i)
        self.chatEnt.setText("")
        lineNum = 0
        for i in range(max(len(self.chatLines)-7, 0), len(self.chatLines)):
            lineRect = Rect(7, lineNum*self.lineHeight+5,
                        self.lineWidth-15, self.lineHeight-1)
            chatLine( self.area, lineRect, self.chatLines[i])
            lineNum += 1

class ChatLine(object):
    def __init__(self, parent, rect ,string= " "):
        self.text = string.format(len(string))
        self.width = rect.right - rect.left    
        self.height = rect.bottom - rect.top
        self.area = parent.subsurface(rect)
        self.area.fill((255,255,255))
        self.font = pygame.font.Font( None, self.height)
        self.textArea = self.font.render( self.text, 1, (0,0,0) )
        self.area.blit(self.textArea,(0,0))
        

    def getArea(self):
        return self.area

        



class ChatEnter(object):
    def __init__ (self, parent,rect, action):
        self.lineIndex = 0
        self.currLineLen = 0
        self.height = rect.bottom - rect.top
        self.font = pygame.font.Font( None, self.height) #For testing width
        self.lines = ['']
        self.area = parent.subsurface(rect)
        self.area.fill((0xFF, 0xFF, 0xFF, 0xFF))
        pygame.draw.rect(self.area,(0,0,0), (0,0, self.area.get_width(),
                                              self.area.get_height()), 3)


    def chat(self):
        #Probably needs removal
        self.chatLines.append(chatLine(self.text))

    def curlyRemove(self):
        sizeL = 0
        sizeR = 0
        for i in self.lines[self.lineIndex]:
            if i == '{':
                sizeL += self.font.size('{')[0]
            elif i == '}':
                sizeR += self.font.size('}')[0]
        sizeTot = sizeL/2 + sizeR/2
        return sizeTot

    def appendText(self, newText):
        self.lines[self.lineIndex] += newText
        self.currLineLen += len(newText)
        if self.lines[self.lineIndex][-1] in ['{', '}']:
            self.currLineLen -= 1
        if self.font.size(self.lines[self.lineIndex])[0] - self.curlyRemove() > self.area.get_width()-5:
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
            
        chatLine(self.area, self.area.get_rect(), self.lines[self.lineIndex])
        pygame.draw.rect(self.area,(0,0,0), (0,0, self.area.get_width(),
                                              self.area.get_height()), 3)

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
        chatLine(self.area, self.area.get_rect(), self.lines[self.lineIndex])
        pygame.draw.rect(self.area,(0,0,0), (0,0, self.area.get_width(),
                                              self.area.get_height()), 3)

    def getArea(self):
        return self._area

    def getText(self):
        return self.lines

    def setText(self, newText):
        self.lines = [newText]
        self.lineIndex = 0
        self.currLineLen = 0
        chatLine(self.area, self.area.get_rect(), self.lines[self.lineIndex])
        pygame.draw.rect(self.area,(0,0,0), (0,0, self.area.get_width(),
                                              self.area.get_height()), 3)
            
        


def main():
    pass



if __name__ == "__main__":
    main()

