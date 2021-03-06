import pygame
from pygame.locals import *
import os
import sys
from EntryBox import EntryBox
from Controls import Button
from Controls import SignInControls
import Colors

class SignIn():
    def __init__(self,parent, font_op):
        temprect = Rect(parent.get_width()/2-200,
                        parent.get_height()/2-200, 400,400)
        self.area = parent.subsurface(temprect)
        self.parent = parent
        self.width = 400
        self.height = 400
        self.font_op = font_op
        self.userList = []
        self.userTextList = []
        self.userListArea = self.area.subsurface((25,75,350,250))
        self.next = 0
        self.selected = ''
        self.clock = pygame.time.Clock()
        #sound
        self.click = pygame.mixer.Sound(os.path.join('sound','click.wav')) 



    def load(self):
        with open('userlist.txt', 'r') as file:
            self.userList = [i.strip() for i in file.readlines()]
            
        self.userTextList = [self.font_op(20,'berlin').render(i,1,(0,0,0))
                             for i in self.userList]
        self.selected = ''
        
        self.text1 = self.font_op(20,'berlin').render(
            "Please Sign in or select local Game",1,(255,255,255))
        self.text2 = self.font_op(20,'berlin').render("New User:",1,(220,146,40))
        temprect = Rect(self.text2.get_width()+10, self.text1.get_height()+13,
                        self.area.get_width()/2, self.text2.get_height() +4 )
        self.newUserEntry = EntryBox(self.area, 15, temprect ,self.font_op
                                     , 1, 0, '', -1)
        temprect = Rect((self.newUserEntry.getRight() +10,
                         self.newUserEntry.getTop(),75, self.newUserEntry.getHeight()))
        self.addButton = Button(self.area, temprect, "Add")
        temprect = Rect(0,350,400,50)
        self.controls = SignInControls(self.area, temprect)
        self.bg = pygame.image.load(os.path.join("img","signInBG.png")).convert()
        self.bgLeft = pygame.image.load(os.path.join("img","signInBGLeft.png")).convert()
        self.bgRight = pygame.image.load(os.path.join("img","signInBGRight.png")).convert()
        self.growlSound = pygame.mixer.Sound(os.path.join('sound','growl.wav')) 

    def addUser(self):
        user = self.newUserEntry.getText()
        self.userList.append(user)
        self.userTextList.append(self.font_op(20,'berlin').render(user,1,(0,0,0)))
        with open('userlist.txt', 'a') as file:
            file.write(user+'\n')
        self.newUserEntry.setText()

    def mouseClick(self):
        mousex, mousey = pygame.mouse.get_pos()
        if self.newUserEntry.isClicked(mousex, mousey):
            self.newUserEntry.giveFocus()
        if self.addButton.wasClicked(mousex,mousey):
            self.click.play() 
            print("click")
            self.addUser()
        xoffset, yoffset = self.userListArea.get_abs_offset()
        if (xoffset < mousex<self.userListArea.get_width() +xoffset and yoffset < mousey <self.userListArea.get_height() + yoffset):
            self.textClick(xoffset, yoffset)
        clickedButton = self.controls.wasClicked(mousex, mousey)
        if clickedButton:
            self.click.play() 
            self.buttonActions(clickedButton)

    def buttonActions(self, bNumber):
        print(bNumber)
        if bNumber == 1:
            self.next = 'lobby'
        elif bNumber ==3 or bNumber ==2:
            try:
                f = open('signedin.txt','w')
                f.write(self.userList[self.selected])
                f.close
            except TypeError:
                errorTxt = self.font_op(30,'berlin').render("A User Was Not Selected",1,Colors.WHITE,Colors.BLACK)
                self.parent.blit(errorTxt, ((self.parent.get_width()-errorTxt.get_width())/2,20))
                f.close
                return
            self.next = 'Olobby'
        elif bNumber ==4:
            self.deleteUser(self.selected)

    def deleteUser(self, number):
        if number != '':
            self.userList.pop(number)
            self.userTextList.pop(number)
            self.selected = ''
            with open("userlist.txt" , 'w') as file:
                for i in self.userList:
                    file.write(i +'\n')   

    def textClick(self, xoffset, yoffset):
        mousex, mousey = pygame.mouse.get_pos()
        for i in range(len(self.userTextList)):
            text = self.userTextList[i]
            if(yoffset < mousey <text.get_height()*(i+1) + yoffset and mousey> text.get_height()*(i) + yoffset ):
                self.userTextList[i] = self.font_op(20,'berlin').render(self.userList[i],1,Colors.BLACK ,Colors.LIGHTBLUE)
                self.selected = i
                return
            else:
                self.userTextList[i] = self.font_op(20,'berlin').render(self.userList[i],1,Colors.BLACK ,Colors.WHITE)
                self.selected = ''                   

    def draw(self):
        self.area.blit(self.bg, (0,0))
        self.area.blit(self.text1, (50,5))
        self.area.blit(self.text2, (5,self.text1.get_height()+15))
        self.newUserEntry.draw()
        self.addButton.redraw()
        self.controls.redraw()
        self.userListArea.fill((255,255,255))
        #print('bg',self.bg,'\nt1',self.text1,'\nt2',self.text2,'\nEntry',self.newUserEntry)
        try:
            textHT = self.userTextList[0].get_height()        
        except IndexError:
            pass
        for i in range(len(self.userTextList)):
            self.userListArea.blit(self.userTextList[i], (3,i*textHT))
        
    def run(self):
        self.load()
        self.draw()
        soundTime = pygame.time.get_ticks()/1000.0
        self.clock.tick(30)
        widthX = 0
        soundRunning = 0
        while not self.next:   
            for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN:
                        self.mouseClick()
                    if event.type == KEYDOWN:
                        if self.newUserEntry.hasFocus():
                            if event.key == K_RETURN:
                                self.addUser()
                            self.newUserEntry.textEntry(event)
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                        return 0
            self.draw()

            time = pygame.time.get_ticks()/1000. - soundTime
            if time < 1:
                self.area.blit(self.bgLeft, (0,0))
                self.area.blit(self.bgRight, (200,0))
            if time > 1 and soundRunning == 0:
                self.growlSound.play()
                soundRunning = 1
            if widthX < 200 and time > 1:
                self.area.blit(self.bgLeft, (0 - widthX,0))
                self.area.blit(self.bgRight, (200 + widthX,0))
                widthX += 1
                
            pygame.display.update()    
        return self.next
            
        
            
        
        
        
        
