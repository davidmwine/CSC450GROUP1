import pygame
from pygame.locals import *
import os
import sys
from EntryBox import EntryBox
from 



class SignIn():
    def __init__(self,parent, font_op):
        temorect = Rect(parent.get_width()/2-200,parent.get_height()/2-200, 400,400)
        self.area = parent.subsurface(rect)
        self.width = 400
        self.height = 400
        self.font_op = font_op
        self.userList = []
        self.userTextList = []
        self.userListArea = self.area.subsurface((25,75,350,300))


    def load(self):
        with open('userlist.txt', r) as file:
            self.userList = [i for i in file.readlines()]
        
        self.userTextList = [self.font_op(20,'berlin').render(i,1,(0,0,0)) for i in self.userList]
        self.text1 = self.font_op(20,'berlin').render("Please Sign in or select local Game",1,(0,0,0))
        self.text2 = self.font_op(20,'berlin').render("New User:",1,(0,0,0))
        temprect = Rect(self.text2.get_width()+10, self.text1.get_height()+13,
                        self.text2.get_height() +4, self.area/2)
        self.newUserEntry = EntryBox(self.area, 15, temprect ,font_op, 1, 0, '', -1)
        self.bg = pygame.image.load(os.path.join("img","menu_bg4.png"))


    def draw(self):
        self.area.blit(self.bg, (0,0))
        self.area.blit(self.text1, (self.area.get_width()/2-self.text1.get_width(),5))
        self.area.blit(self.text2, (0,self.text1.get_height()+15))
        self.newUser.draw()
        self.userListArea.fill((255,255,255))
        try
            textHT = self.userTextList[:1]
            for i in self.userTextList
        except:
        
        
        
        
