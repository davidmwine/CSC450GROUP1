import pygame, sys, os
from pygame.locals import *
import Colors


class MoneyBox(object):
    def __init__(self, parent, rect, font_op, scale, player):
        self.parent = parent
        self.maxLength = 20
        self.font_op = font_op
        self.rect = rect
        self.area = parent.subsurface(self.rect)
        self.scale = scale
        self.currMoney = 0
        self.currText = self.font_op(20*self.scale, 'berlin').render("$"+str(self.currMoney),1,(0,0,0))
        self.playerText = self.font_op(20*self.scale, 'berlin').render(player.getName(),1,(0,0,0))
        self.player = player

    def draw(self):
        self.area.fill(Colors.COLLEGECOLORS[self.player.getCollege()])
        pygame.draw.rect(self.area, (0, 0, 0), (0, 0, self.area.get_width(),
                                                self.area.get_height()), 2)
        textRect = (self.area.get_width()/2 - self.playerText.get_width()/2,
                    self.area.get_height()/3 - self.playerText.get_height()/2)
        self.area.blit(self.playerText, textRect)
        textRect = (self.area.get_width()/2 - self.currText.get_width()/2,
                    2*self.area.get_height()/3 - self.currText.get_height()/2)
        self.area.blit(self.currText, textRect)
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

    def getCurrMoney(self):
        return self.currMoney

    def moveNext(self):
        #while self.currIndex in self.lockedIndices:
        #    self.currIndex += 1
        #    self.currIndex %= len(self.colleges)
        self.currMoney += 1000
        self.currText = self.font_op(20*self.scale, 'berlin').render("$"+str(self.currMoney),1,(0,0,0))

    def isClicked(self, mousex, mousey):
        top = self.rect.top
        left = self.rect.left
        bottom = self.rect.bottom
        right = self.rect.right
        if left < mousex < left + (right - left)/2 and \
           top < mousey < bottom and self.currMoney > 0:
            self.currMoney -= 1000
            self.currText = self.font_op(20*self.scale, 'berlin').render("$"+str(self.currMoney),1,(0,0,0))
            self.draw()
            return True
        elif left + (right - left)/2 < mousex < right and \
             top < mousey < bottom and \
             self.currMoney < self.player.dollars - 1000:
            self.currMoney += 1000
            self.currText = self.font_op(20*self.scale, 'berlin').render("$"+str(self.currMoney),1,(0,0,0))
            self.draw()
            return True
        return False
