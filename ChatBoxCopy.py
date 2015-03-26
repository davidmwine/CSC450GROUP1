import pygame, sys
from pygame.locals import *

class ChatBox(object):
    '''chatBox(scale=1, parent=None, sizeRect=None)
    Create a chatbox with the given scale factor, parent
    rectangle, and if parent rectangle is given sizeRect
    is the size of the parent rectangle'''
    
    def __init__(self, scale=1, parent=None , sizeRect=None):
        self.rightEdge = 1920*scale
        self.bottomEdge = 1080*scale
        self.width = - sizeRect.left + sizeRect.right
        self.height = sizeRect.bottom - sizeRect.top
        self.lineWidth = self.width
        self.lineHeight = self.height/9
        self.scale = scale
        self.chatLines = [] #List of each line entered into chat
        if parent != None:
            self.area = parent.subsurface(sizeRect)

        self.drawChat()


    def drawChat(self):
        '''drawChat()
        drawChat creates the entered chat area, and displays
        the blank chatbox'''
        self.area.fill((255,255,255))
        self.chatEnt = ChatEnter(self.area,Rect(0, self.lineHeight*8,
        self.lineWidth, self.lineHeight), None)
        '''for i in range(7,-1,-1):
            line_rect = Rect(3, i*self._line_height+1,
                        self._line_width-3, self._line_height-1)
            try:
                ChatLine( self._area, line_rect, self._chatlines[i])
            except IndexError:
                ChatLine(self._area, line_rect, "Line {}".format(i+1))'''
        pygame.draw.rect(self.area,(0,0,0), (0,0, self.area.get_width(),
                                              self.area.get_height()), 2)
    def redraw(self):
        self.drawChat()
        lineNum = 0
        for i in range(7):
            lineRect = Rect(7, lineNum*self.lineHeight+5,
                        self.lineWidth-15, self.lineHeight-1)
            try:
                ChatLine( self.area, lineRect, self.chatLines[i])
            except IndexError:
                ChatLine(self.area, lineRect)
            lineNum += 1
        
    
    def getLeft(self):
        '''getLeft() returns the location of left end of the chatbox'''
        #print(self._area.get_rect().left)
        #print(self._RightEdge - self._area.get_width())
        return self.rightEdge - self.area.get_width()

    def getRight(self):
        '''getRight() returns the location of the right end of the chatbox'''
        #print(self._RightEdge)
        return self.rightEdge

    def getTopType(self):
        '''getTopType() returns the location of the top of the chatbox'''
        #print(self._BottomEdge - self._chatenter.getArea().get_rect().top)
        return self.bottomEdge - self.chatEnt.getArea().get_height()

    def getBottomType(self):
        '''getBottomType() returns the location of the bottom of the chatbox'''
        #print(self._BottomEdge)
        return self.bottomEdge

    def typeText(self, text):
        '''typeText(text) appends new text to the enter chat box'''
        self.chatEnt.appendText(text)

    def deleteText(self):
        '''deleteText() removes one character from the enter chat box'''
        self.chatEnt.removeText()

    def submitText(self):
        '''submitText() gets the text from the enter chat box, and displays
        the most recent seven lines entered by the user'''
        newText = self.chatEnt.getText()
        #print(len(newText))
        for i in newText:
            self.chatLines.append(i)
        self.chatEnt.setText("")
        lineNum = 0
        for i in range(max(len(self.chatLines)-7, 0), len(self.chatLines)):
            lineRect = Rect(7, lineNum*self.lineHeight+5,
                        self.lineWidth-15, self.lineHeight-1)
            ChatLine( self.area, lineRect, self.chatLines[i])
            lineNum += 1
    
    
class ChatLine(object):
    def __init__(self, parent, rect ,string= " "):
        '''ChatLine(parent, rect, string = " ")
        ChatLine takes a parent surface, a rectangular area
        and a string, then displays the string in the given
        rectangular area.'''
        self.text = string.format(len(string))
        self.width = rect.right - rect.left    
        self.height = rect.bottom - rect.top
        self.area = parent.subsurface(rect)
        self.area.fill((255,255,255))
        self.font = pygame.font.Font( None, self.height)
        self.textArea = self.font.render( self.text, 1, (0,0,0) )
        self.area.blit(self.textArea,(0,0))
        

    def getArea(self):
        '''getArea() returns the size of the area the text is
        being displayed in'''
        return self.area

        



class ChatEnter(object):
    def __init__ (self, parent,rect, action):
        '''ChatEnter(parent, rect, action)
        ChatEnter takes a parent surface, and a rectangular area
        which text will be displayed in'''
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
        '''curlyRemove() returns the total size of doubled
        curly braces that were used as escape characters, so
        that they can be ignored in determining the length of
        a line of text.'''
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
        '''appendText(newText) takes a new string, and adds it to
        the current text being displayed'''
        self.lines[self.lineIndex] += newText
        self.currLineLen += len(newText)
        if self.lines[self.lineIndex][-1] in ['{', '}']:
            self.currLineLen -= 1 #Ignoring doubled curly braces needed as escape characters
        if self.font.size(self.lines[self.lineIndex])[0] - self.curlyRemove() > self.area.get_width()-5: #Reached end of line
            self.currLineLen = 0
            lastSpace = self.lines[self.lineIndex].rfind(' ')
            if lastSpace > -1: #If no space in current line, simply wrap text
                newLineStart = self.lines[self.lineIndex][lastSpace+1:]
                self.lines[self.lineIndex] = self.lines[self.lineIndex][:lastSpace]
                self.lineIndex += 1
                self.lines.append(newLineStart)
                self.currLineLen = len(newLineStart)
            else: #If there was a space, wrap any text after last space to new line
                nextLine = self.lines[self.lineIndex][-1]
                if self.lines[self.lineIndex][-1] in ['{', '}']: #Double braces for escape character
                    self.lines[self.lineIndex] = self.lines[self.lineIndex][:len(self.lines[self.lineIndex])-2]
                    self.lines.append(nextLine + nextLine)
                else:
                    self.lines[self.lineIndex] = self.lines[self.lineIndex][:len(self.lines[self.lineIndex-1])]
                    self.lines.append(nextLine)
                self.currLineLen = 1
                self.lineIndex += 1
            
        ChatLine(self.area, self.area.get_rect(), self.lines[self.lineIndex])
        pygame.draw.rect(self.area,(0,0,0), (0,0, self.area.get_width(),
                                              self.area.get_height()), 3)

    def removeText(self):
        '''removeText() deletes a character from the existing text being entered'''
        if len(self.lines[self.lineIndex]) < 1 and self.lineIndex == 0: #If no text left to delete
            return
        if self.lines[self.lineIndex][-1] in ['{', '}']: #Delete two characters if a brace
            self.lines[self.lineIndex] = self.lines[self.lineIndex][0:-2]
        else: #Otherwise simply delete the character
            self.lines[self.lineIndex] = self.lines[self.lineIndex][0:-1]
        self.currLineLen -= 1
        if len(self.lines[self.lineIndex]) < 1 and self.lineIndex > 0: #Remove the line if backspaced to beginning of line
            if self.lineIndex >= 0:
                self.lineIndex -= 1
                self.lines.pop()
        ChatLine(self.area, self.area.get_rect(), self.lines[self.lineIndex])
        pygame.draw.rect(self.area,(0,0,0), (0,0, self.area.get_width(),
                                              self.area.get_height()), 3)

    def getArea(self):
        '''getArea() returns the size of the enter chat box'''
        return self.area

    def getText(self):
        '''getText() returns the lines of text needing entered into chat'''
        return self.lines

    def setText(self, newText):
        '''setText(newText) takes a string and sets the current text field to that string'''
        self.lines = [newText]
        self.lineIndex = 0
        self.currLineLen = 0
        ChatLine(self.area, self.area.get_rect(), self.lines[self.lineIndex])
        pygame.draw.rect(self.area,(0,0,0), (0,0, self.area.get_width(),
                                              self.area.get_height()), 3)
            
        


def main():
    pass



if __name__ == "__main__":
    main()

