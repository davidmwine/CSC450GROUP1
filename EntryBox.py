import pygame, sys, os
from pygame.locals import *
from TextWrap import *


class EntryBox():

    def __init__(self, parent, length, position ,font_op, scale , offset, start_text = '', maxChar = -1):
        self.parent = parent
        self.len = length
        self.font_op = font_op
        self.width, self.height = self.font_op(10, 'berlin').size(" " + "W"*length)
        if self.width > position[2]:
            position = (position[0], position[1], self.width, position[3])
        self.text = start_text
        self.x_start = position[0]
        self.y_start = position[1]
        self.area = parent.subsurface(position)
        self.focus = False
        self.scale = scale
        self.offset = offset #For isClick to know proper location
        self.maxChar = maxChar

    def draw(self):
        self.area.fill((255,255,255))
        boxText = self.font_op(20*self.scale, 'berlin').render(" " +self.text,1,(0,0,0))
   
        pygame.draw.rect(self.area,(0,0,0), (0,0, self.area.get_width(),
                                              self.area.get_height()), 2)
        self.area.blit(boxText, (0,0))

    def setMaxChar(self, num):
        self.maxChar = num

    def getMaxChar(self):
        return self.maxChar

    def getText(self):
        return self.text

    def setText(self, entry = ""):
        self.text = entry

    def deleteText(self):
        self.text = self.text[:-1]

    def hasFocus(self):
        return self.focus

    def giveFocus(self):
        self.focus = True

    def takeFocus(self):    
        self.focus = False

    def getLeft(self):
        return self.area.get_offset()[0]

    def getRight(self):
        return self.area.get_offset()[0] + self.area.get_width() 

    def getTop(self):
        return self.area.get_offset()[1]

    def getBottom(self):
        return self.area.get_offset()[1] + self.area.get_height()

    def getHeight(self):
        return self.area.get_height()

    def isClicked(self, mousex, mousey):
        xoffset, yoffset = self.area.get_abs_offset()
        if(xoffset < mousex<self.area.get_width() +xoffset and yoffset < mousey <self.area.get_height() + yoffset):
            return True
        else:
            return False
        #if(self.x_start< mousex-self.offset[0]< self.x_start+self.area.get_width()) and (self.y_start< mousey-self.offset[1]< self.y_start+self.area.get_height()):
         #  return True
        #else:
         #  return False

         
    def textEntry(self,event):
        CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789-=[];\'\\,./`'
        CHARSCAPS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ)!@#$%^&*(_+{}:"|<>?~'
        if event.key == K_ESCAPE:
            self.focus = False
        elif event.key == K_BACKSPACE:
            self.deleteText()
        elif event.key <= 127 and event.key >= 32 and (self.getMaxChar() == -1 or\
             len(self.getText()) < self.getMaxChar()): #Only accept regular ascii characters (ignoring certain special characters)
            checkCaps = pygame.key.get_pressed()
            if checkCaps[K_RSHIFT] or checkCaps[K_LSHIFT] and chr(event.key) in CHARS:
                index = CHARS.index(chr(event.key))
                currText = self.getText()
                self.setText(currText+CHARSCAPS[index])
            elif checkCaps[K_CAPSLOCK] and chr(event.key) in CHARS:
                index = CHARS.index(chr(event.key))
                if index < 26: #Only caps lock regular alphabet
                    currText = self.getText()
                    self.setText(currText+CHARSCAPS[index])
                else:
                    currText = self.getText()
                    self.setText(currText+chr(event.key))
            else:
                currText = self.getText()
                self.setText(currText+chr(event.key))
        
        
class DropDown(object):

    def __init__(self, parent, rect, font_op, scale, offset, vals):
        self.parent = parent
        self.menu = vals
        self.font_op = font_op
        self.rect = rect
        self.area = parent.subsurface(self.rect)
        self.scale = scale
        self.offset = offset
        self.currVal = self.menu[-1]
        self.focus = False
        self.hovered = False
        self.hovIndex = -1

    def draw(self):
        self.area.fill((255, 255, 255))
        pygame.draw.rect(self.area,(0,0,0), (0,0, self.area.get_width(),\
                                             self.area.get_height()), 2)
        text = self.font_op(20*self.scale, 'berlin').render(self.currVal,1,(0,0,0))
        self.area.blit(text, (10*self.scale,0))
        pygame.draw.polygon(self.area,(0,0,0),((6*self.area.get_width()/10,\
                                            3*self.area.get_height()/8),\
                                            (8*self.area.get_width()/10,\
                                            3*self.area.get_height()/8),\
                                               (7*self.area.get_width()/10,\
                                                5*self.area.get_height()/8), 2))
        if self.focus:
            pygame.draw.rect(self.parent, (255,255,255), (self.rect.left, self.rect.top+self.area.get_height(), self.area.get_width(),\
                                                    len(self.menu)*self.area.get_height()), 0)
            if self.hovered:
                pygame.draw.rect(self.parent, (3, 132, 243), (self.rect.left, self.rect.top+(self.hovIndex)*self.area.get_height(),\
                                                                  self.area.get_width(), self.area.get_height()), 0)
            for i in range(len(self.menu)):
                pygame.draw.rect(self.parent, (0,0,0), (self.rect.left, self.rect.top+(i+1)*self.area.get_height(),\
                                                      self.area.get_width(), self.area.get_height()), 2)
                text = self.font_op(20*self.scale, 'berlin').render(self.menu[i],1,(0,0,0))
                self.parent.blit(text, (10*self.scale + self.rect.left, self.rect.top+(i+1)*self.area.get_height()))

    def getText(self):
        return self.currVal

    def hasFocus(self):
        return self.focus

    def giveFocus(self):
        self.focus = not self.focus

    def takeFocus(self):    
        self.focus = False

    def takeHover(self):
        self.hover = False

    def isClicked(self, mousex, mousey):
        xoffset, yoffset = self.area.get_abs_offset()
        if(xoffset < mousex<self.area.get_width() +xoffset and yoffset < mousey <self.area.get_height    + yoffset):
            return True
        else:
            return False
        #if(self.rect.left< mousex-self.offset[0]< self.rect.right+self.area.get_width()) and (self.rect.top< mousey-self.offset[1]< self.rect.top+self.area.get_height()):
        #   return True
       # else:
       #    return False

    def isSelected(self):
        if not self.focus:
            return False
        elif self.hovered:
            return True
        return False

    def setNewVal(self):
        self.currVal = self.menu[self.hovIndex-1]

    def setIfHovered(self, mousex, mousey):
        if not self.focus:
            self.hovered = False
        elif self.rect.left < mousex < self.rect.right and\
             self.rect.bottom < mousey < self.rect.bottom + (len(self.menu))*self.area.get_height():
            self.hovered = True
            locInBox = (mousey - self.rect.bottom)%self.area.get_height()
            topOfBox = mousey - locInBox
            self.hovIndex = int(topOfBox/self.area.get_height())
        else:
            self.hovered = False


class EntryBoxSet():


    def __init__(self, scale):
        self.entryBoxes = dict()
        self.scale = scale
        self.focused = None

    def createNew(self,parent, length, position , font_op , offset,start_text = '', maxChar = -1):
        name = str(len(self.entryBoxes))
        self.entryBoxes[name] = EntryBox(parent, length, position , font_op, self.scale, offset ,start_text, maxChar)
        return self.entryBoxes[name]

    def newDropDown(self, parent, rect, font_op, scale, offset, vals, name = ''):
        if name == '':
            name = str(len(self.entryBoxes))
        #print(name)
        self.entryBoxes[name] = DropDown(parent, rect, font_op, scale, offset, vals)
        return self.entryBoxes[name]

    def isClicked(self, mousex, mousey, dropDownKey = ''):
        result = False
        for i in self.entryBoxes.keys():
            if self.entryBoxes[i].isClicked(mousex, mousey) and (dropDownKey == '' or not self.entryBoxes[dropDownKey].isSelected()):
                #If box clicked and not clicked in area of a focused drop down
                result = True
                self.entryBoxes[i].giveFocus()
                if not self.focused is None:
                    self.focused.takeFocus()
                if self.entryBoxes[i].hasFocus():
                    self.focused = self.entryBoxes[i]
                else:
                    self.focused = None
            elif dropDownKey != '' and self.entryBoxes[dropDownKey].isSelected(): #If clicked in a focused dropdown
                result = True
                self.entryBoxes[dropDownKey].setNewVal()
                self.entryBoxes[dropDownKey].takeFocus()
                self.entryBoxes[dropDownKey].takeHover()
            elif dropDownKey != '' and not self.entryBoxes[dropDownKey].isSelected()\
                 and self.entryBoxes[dropDownKey].hasFocus() and not self.entryBoxes[dropDownKey].isClicked(mousex, mousey):
                #If clicked outside of a focused drop down, take away the focus
                result = False
                self.entryBoxes[dropDownKey].takeFocus()
                self.entryBoxes[dropDownKey].takeHover()
                self.focused = None
                                                
        return result
            
    def getBoxes(self):
        return self.entryBoxes

    def getBox(self, name):
        return self.entryBoxes[name]

    def getFocused(self):
        return self.focused

    def draw(self, val = -1, dropDownKey = ''):
        if val > -1: #KEYS MUST BE STRINGS OF INTEGERS IN ORDER OF BEING CREATED TO WORK
            for i in range(val):
                #print(val)
                self.entryBoxes.get(str(i)).draw()
        else:
            for i in self.entryBoxes:
                self.entryBoxes.get(i).draw()
        if dropDownKey != '' and self.entryBoxes.get(dropDownKey).hasFocus():
            self.entryBoxes.get(dropDownKey).draw()
    





