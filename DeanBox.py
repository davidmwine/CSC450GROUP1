import pygame, sys, os
from pygame.locals import *
import Colors


class DeanBox(object):
    def __init__(self, parent, rect, font_op, scale, offset, default, playerNum):
        self.parent = parent
        self.maxLength = 8 #Max length of the string for player name
        self.font_op = font_op
        self.rect = rect
        self.area = parent.subsurface(self.rect)
        self.scale = scale
        self.offset = offset #Determine click location
        self.locked = False
        self.lockedIndices = []
        self.currColl = default
        self.colleges = list(Colors.COLLEGEABBR.keys())
        self.colleges.sort()
        self.currIndex = self.colleges.index(self.currColl)
        self.currText = self.font_op(20*self.scale, 'berlin').render(Colors.COLLEGEABBR[self.currColl],1,(0,0,0))
        self.currColor = Colors.COLLEGECOLORS[self.currColl]
        self.playerText = self.font_op(20*self.scale, 'berlin').render("Player " + str(playerNum),1,(0,0,0))

    def draw(self):
        self.area.fill(Colors.COLLEGECOLORS[self.currColl])
        pygame.draw.rect(self.area, (0, 0, 0), (0, 0, self.area.get_width(), self.area.get_height()), 2)
        textRect = (self.area.get_width()/2 - self.playerText.get_width()/2, self.area.get_height()/3 - self.playerText.get_height()/2)
        self.area.blit(self.playerText, textRect)
        textRect = (self.area.get_width()/2 - self.currText.get_width()/2, 2*self.area.get_height()/3 - self.currText.get_height()/2)
        self.area.blit(self.currText, textRect)
        if not self.locked:
            pygame.draw.polygon(self.area, (0, 0, 0), ((self.area.get_width()/16,\
                                                        self.area.get_height()/2),\
                                                       (self.area.get_width()/8,\
                                                        self.area.get_height()/2 + self.area.get_height()/8),
                                                       (self.area.get_width()/8,\
                                                        self.area.get_height()/2 - self.area.get_height()/8)), 0)
            pygame.draw.polygon(self.area, (0, 0, 0), ((self.area.get_width() - self.area.get_width()/16,\
                                                        self.area.get_height()/2),\
                                                       (self.area.get_width() - self.area.get_width()/8,\
                                                        self.area.get_height()/2 + self.area.get_height()/8),
                                                       (self.area.get_width() - self.area.get_width()/8,\
                                                        self.area.get_height()/2 - self.area.get_height()/8)), 0)

    def getRect(self):
        return self.rect

    def setLocked(self):
        self.locked = not self.locked
        if self.locked:
            self.lockedIndices.append(self.currIndex)
            return True

    def getLocks(self):
        return self.lockedIndices

    def getIsLocked(self):
        return self.locked

    def setLocks(self, locks):
        self.lockedIndices = locks
        if not self.locked:
            self.moveNext()

    def unlock(self):
        self.locked = False

    def getCurrIndex(self):
        return self.currIndex

    def moveNext(self):
        while self.currIndex in self.lockedIndices:
            self.currIndex += 1
            self.currIndex %= len(self.colleges)
        self.currColl = self.colleges[self.currIndex]
        self.currText = self.font_op(20*self.scale, 'berlin').render(Colors.COLLEGEABBR[self.currColl],1,(0,0,0))

    def isClicked(self, mousex, mousey):
        top = self.rect.top
        left = self.rect.left
        bottom = self.rect.bottom
        right = self.rect.right
        if left < mousex < left + (right - left)/2 and\
           top < mousey < bottom and not self.locked:
            self.currIndex -= 1
            self.currIndex %= len(self.colleges)
            while self.currIndex in self.lockedIndices:
                self.currIndex -= 1
                self.currIndex %= len(self.colleges)
            self.currColl = self.colleges[self.currIndex]
            self.currText = self.font_op(20*self.scale, 'berlin').render(Colors.COLLEGEABBR[self.currColl],1,(0,0,0))
            return True
        elif left + (right - left)/2 < mousex < right and\
             top < mousey < bottom and not self.locked:
            self.currIndex += 1
            self.currIndex %= len(self.colleges)
            while self.currIndex in self.lockedIndices:
                self.currIndex += 1
                self.currIndex %= len(self.colleges)
            self.currColl = self.colleges[self.currIndex]
            self.currText = self.font_op(20*self.scale, 'berlin').render(Colors.COLLEGEABBR[self.currColl],1,(0,0,0))
            return True
        return False

class DeanBoxes(object):
    def __init__(self, parent, font_op, scale, offset, width, height):
        self.parent = parent
        self.font_op = font_op
        self.scale = scale
        self.offset = offset
        self.width = width
        self.height = height
        self.boxes = []

    def newBox(self, rect, default):
        self.boxes.append(DeanBox(self.parent, rect, self.font_op, self.scale, self.offset, default, len(self.boxes)+1))

    def getBox(self, val):
        return self.boxes[val]

    def drawBoxes(self, val):
        for i in range(val):
            self.boxes[i].draw()

    def unlock(self, val):
        self.boxes[val].unlock()

    def lock(self, val):
        self.boxes[val].setLocked()

    def updateLocks(self, currInd, currLocked):
        lockSet = set()
        for i in self.boxes:
            lockSet = lockSet | set(i.getLocks()) #Combine all locks for all boxes
        if not currLocked: #Remove unlocked item
            lockSet -= set([currInd])
        for i in self.boxes:
            i.setLocks(list(lockSet))

