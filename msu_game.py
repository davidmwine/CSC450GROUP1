import pygame
from pygame.locals import *
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'  # Center the display

pygame.init()
clock = pygame.time.Clock()

def font_op(size,fontName):  #Pick font size and type
    if fontName == "helvetica":
        fontAndSize = pygame.font.Font(os.path.join("font","helvetica.OTF"),size) # "font" is directory for the font file
    elif fontName == "berlin":
        fontAndSize = pygame.font.Font(os.path.join("font","berlin.TTF"),size)
    return fontAndSize

'''class Player(object):
    
    def __init__(self, name):
        self.name = name
        self.money = 1000  #Amount of money to start with
        self.pos = 0  #Starting position'''

class Game(object):
    screen = None

    def __init__(self):
        #Get screen info and set window to full screen
        '''infoScreen = pygame.display.Info()  
        self.screen = pygame.display.set_mode((infoScreen.current_w, infoScreen.current_h))'''
        
        self.screen = pygame.display.set_mode((800, 600))  #Set display window size

        self.gameActive = 0  #Is the game running or not
        self.quitGame = False
        
    def start(self):
        pygame.display.set_caption("Mastering MSU")
        self.load_images()
        pygame.display.set_icon(self.img_icon_small)
        start_time = pygame.time.get_ticks()/1000.0
        #Remove multiple line comment below to view splash screen
        '''text_color = [230,230,230]

        while True:
            clock.tick(30)
            self.screen.fill((0,0,0))
            time = pygame.time.get_ticks()/1000. - start_time
            
            if time > 1 and time < 6:            
                for i in range(3):
                    if text_color[i] < 255:
                        text_color[i] -= 1.3
                text_title = font_op(72,"berlin").render("Mastering MSU",True,text_color)
                #text_team1 = font_op(24,"helvetica").render("a Team 1 game",True,text_color)
             
                self.screen.blit(self.img_logo,(self.screen.get_width()/2-0.5*self.img_logo.get_width(),220-0.5*self.img_logo.get_height()))
                self.screen.blit(text_title,(self.screen.get_width()/2-0.5*text_title.get_width(),280))
                #self.screen.blit(text_team1,(self.screen.get_width()/2-0.5*text_team1.get_width(),380))
            if time > 7:
                break

            pygame.display.update()'''
        self.menu()
        
    def menu(self):
        text_header = font_op(90,"berlin").render("Mastering MSU",True,(255,255,255))
        text_header_bg = font_op(90,"berlin").render("Mastering MSU",True,(0,0,0))
        text_start = font_op(32,"berlin").render("New Game",True,(255,255,255))
        text_start_bg = font_op(32,"berlin").render("New Game",True,(0,0,0))
        text_resume = font_op(32,"berlin").render("Resume Game",True,(255,255,255))
        text_resume_bg = font_op(32,"berlin").render("Resume Game",True,(0,0,0))
        text_rules = font_op(32,"berlin").render("Rules",True,(255,255,255))
        text_rules_bg = font_op(32,"berlin").render("Rules",True,(0,0,0))
        text_options = font_op(32,"berlin").render("Options",True,(255,255,255))
        text_options_bg = font_op(32,"berlin").render("Options",True,(0,0,0))
        text_exit = font_op(32,"berlin").render("Exit",True,(255,255,255))
        text_exit_bg = font_op(32,"berlin").render("Exit",True,(0,0,0)) 

        menu = True
        rulesActive = False

        while menu:
            clock.tick(30)
            self.screen.fill((240,240,240))

            for event in pygame.event.get():
                if event.type == QUIT:
                    exit() 
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        if rulesActive == True:
                            rulesActive = False
                        elif self.gameActive == 1:
                            menu = False
                            
                if event.type == MOUSEMOTION:  #Highlight text on hover
                    mouseX,mouseY = pygame.mouse.get_pos() 
                    if mouseX > self.screen.get_width()/2-107\
                       and mouseX < self.screen.get_width()/2-57+text_start.get_width()+5\
                       and mouseY > 195 and mouseY < 200+text_start.get_height():
                        text_start = font_op(32,"berlin").render("New Game",True,(255,255,255))
                    elif self.gameActive == 1:
                        text_start = font_op(32,"berlin").render("New Game",True,(220,146,40)) 
                        if mouseX > self.screen.get_width()/2-107\
                           and mouseX < self.screen.get_width()/2-57+text_resume.get_width()+5\
                           and mouseY > 270 and mouseY < 275+text_resume.get_height():
                            text_resume = font_op(32,"berlin").render("Resume Game",True,(255,255,255))
                        else:
                            text_resume = font_op(32,"berlin").render("Resume Game",True,(220,146,40))
                    else:
                        text_start = font_op(32,"berlin").render("New Game",True,(220,146,40))    
                    if mouseX > self.screen.get_width()/2-107\
                       and mouseX < self.screen.get_width()/2-57+text_rules.get_width()+5\
                       and mouseY > 270+75*self.gameActive\
                       and mouseY < 275+text_rules.get_height()+75*self.gameActive:
                        text_rules = font_op(32,"berlin").render("Rules",True,(255,255,255))
                    else:
                        text_rules = font_op(32,"berlin").render("Rules",True,(220,146,40))
                    if mouseX > self.screen.get_width()/2-107\
                       and mouseX < self.screen.get_width()/2-57+text_options.get_width()+5\
                       and mouseY > 345+75*self.gameActive\
                       and mouseY < 350+text_options.get_height()+75*self.gameActive:
                        text_options = font_op(32,"berlin").render("Options",True,(255,255,255))
                    else:
                        text_options = font_op(32,"berlin").render("Options",True,(220,146,40))       
                    if mouseX > self.screen.get_width()/2-107\
                       and mouseX < self.screen.get_width()/2-57+text_exit.get_width()+5\
                       and mouseY > 420+75*self.gameActive\
                       and mouseY < 425+text_exit.get_height()+75*self.gameActive:
                        text_exit = font_op(32,"berlin").render("Exit",True,(255,255,255))
                    else:
                        text_exit = font_op(32,"berlin").render("Exit",True,(220,146,40))
                        
                if event.type == MOUSEBUTTONDOWN:  #Perform action on click
                    mouseX,mouseY = pygame.mouse.get_pos()
                    if rulesActive == True:
                        if mouseX > self.screen.get_width()-156\
                           and mouseX < self.screen.get_width()-96\
                           and mouseY > 57 and mouseY < 117:
                            rulesActive = False
                        if self.rules_page > 1:
                            if mouseX > self.screen.get_width()/2-310\
                               and mouseX < self.screen.get_width()/2-254\
                               and mouseY > 385 and mouseY < 428:
                                self.rules_next_page(-1)
                        if self.rules_page < rules_count:
                            if mouseX > self.screen.get_width()/2+245\
                               and mouseX < self.screen.get_width()/2+320\
                               and mouseY > 385 and mouseY < 428:
                                self.rules_next_page(1)
                    if mouseX > self.screen.get_width()/2-107\
                       and mouseX < self.screen.get_width()/2-57+text_rules.get_width()+5\
                       and mouseY > 270+75*self.gameActive\
                       and mouseY < 275+text_rules.get_height()+75*self.gameActive:
                        self.rules_next_page()
                        rulesActive = True
                    elif mouseX > self.screen.get_width()/2-107\
                         and mouseX < self.screen.get_width()/2-57+text_exit.get_width()+5\
                         and mouseY > 420+75*self.gameActive\
                         and mouseY < 425+text_exit.get_height()+75*self.gameActive:
                        self.quitGame = True
                        menu = False
                        
                        
            if rulesActive == True:
                rules_count = 3  #Number of rules/rule pages
                self.screen.blit(self.img_menu_bg, (0, 0))
                pygame.draw.rect(self.screen,(255,255,255),Rect((self.screen.get_width()/2-300,75),(600,350)))
                self.screen.blit(self.img_rules,(0,450))
                pygame.draw.rect(self.screen,(0,0,0),Rect((self.screen.get_width()/2-300,75),(600,350)),1)
                self.screen.blit(self.img_icon_exit_x,(self.screen.get_width()- 151,62))
                if self.rules_page < rules_count: 
                    self.screen.blit(self.img_arrow,(self.screen.get_width()/2+250,390))
                if self.rules_page > 1:
                    self.screen.blit(self.img_arrow_left,(self.screen.get_width()/2-315,390))

                #Page number display
                self.screen.blit(font_op(22,"helvetica").render(str(self.rules_page)+"/"+str(rules_count),True,(68,201,20)),(self.screen.get_width()/2-294,77))

                header = font_op(50,"berlin").render(self.rules_header,True,(255,255,255))
                self.screen.blit(header,(self.screen.get_width()/2-0.5*header.get_width(),4))
                for text in range(len(self.rules_words)): #Display rules on a page 
                    textOut = font_op(20,"helvetica").render(self.rules_words[text],True,(0,0,0))
                    self.screen.blit(textOut,(self.screen.get_width()/2-240,130+text*25))   
            else:
                self.screen.blit(self.img_menu_bg, (0, 0))
                self.screen.blit(text_header_bg,(self.screen.get_width()/2-3-0.5*text_header_bg.get_width()+4,31))
                self.screen.blit(text_header,(self.screen.get_width()/2-3-0.5*text_header.get_width(),27))

                self.screen.blit(text_start_bg,(self.screen.get_width()/2-55,202))
                self.screen.blit(text_start,(self.screen.get_width()/2-57,200))
                self.screen.blit(text_rules_bg,(self.screen.get_width()/2-55,277+75*self.gameActive))
                self.screen.blit(text_rules,(self.screen.get_width()/2-57,275+75*self.gameActive))
                self.screen.blit(text_options_bg,(self.screen.get_width()/2-55,352+75*self.gameActive))
                self.screen.blit(text_options,(self.screen.get_width()/2-57,350+75*self.gameActive))
                self.screen.blit(text_exit_bg,(self.screen.get_width()/2-55,427+75*self.gameActive))
                self.screen.blit(text_exit,(self.screen.get_width()/2-57,425+75*self.gameActive))
            
                self.screen.blit(self.img_icon_start,(self.screen.get_width()/2-112,195))
                self.screen.blit(self.img_icon_rules,(self.screen.get_width()/2-112,270+75*self.gameActive))
                self.screen.blit(self.img_icon_options,(self.screen.get_width()/2-112,345+75*self.gameActive))
                self.screen.blit(self.img_icon_exit,(self.screen.get_width()/2-112,420+75*self.gameActive))

            if self.gameActive == 1:
                self.screen.blit(text_resume_bg,(self.screen.get_width()/2-55,277))
                self.screen.blit(text_resume,(self.screen.get_width()/2-57,275))
                self.screen.blit(self.img_icon_resume,(self.screen.get_width()/2-112,270))
            
            pygame.display.update()
        if self.quitGame:
            pygame.quit()



    def load_images(self):
        self.img_logo = pygame.image.load(os.path.join("img","logo.png")).convert_alpha()
        self.img_menu_bg = pygame.image.load(os.path.join("img","menu_bg4.png")).convert()
        self.img_arrow = pygame.image.load(os.path.join("img","arrow.png")).convert_alpha()
        self.img_arrow_left = pygame.image.load(os.path.join("img","arrowLeft.png")).convert_alpha()
        
        self.img_icon_small = pygame.image.load(os.path.join("img","icon_small.png")).convert_alpha()
        self.img_icon_start = pygame.image.load(os.path.join("img","dice2b.png")).convert_alpha()
        self.img_icon_resume = pygame.image.load(os.path.join("img","thumb_up2.png")).convert_alpha()
        self.img_icon_rules = pygame.image.load(os.path.join("img","book-brownb.png")).convert_alpha()
        self.img_icon_options = pygame.image.load(os.path.join("img","gear_01b.png")).convert_alpha()
        self.img_icon_exit = pygame.image.load(os.path.join("img","exitb.png")).convert_alpha() #Game exit
        self.img_icon_exit_x = pygame.image.load(os.path.join("img","exit.png")).convert_alpha() #Rules exit

    def rules_next_page(self, pageNum=None):
        if pageNum == None:
            self.rules_page = 1
        else:
            self.rules_page += pageNum
        self.img_rules = pygame.Surface((800,150)).convert()
        bottom_image = "rulesBottom1.png"

        if self.rules_page == 1:
            self.rules_header = "Rules Intro Header"
            self.rules_words = ["Here are some rules for you to look at. Wow",
                                "look at all of this great stuff on this line.",
                                "Here's some more info. RRRRrrrrrrrrrrrrrrrrrr",
                                "rrrrrrrrrr."]
        if self.rules_page == 2:
            bottom_image = "rulesBottom2.png"
            self.rules_header = "General Rules"
            self.rules_words = ["Here are some rules for you to look at and stuff.",
                                "Here's some more info."]
        if self.rules_page == 3:
            bottom_image = "rulesBottom3.png"
            self.rules_header = "More Rules"
            self.rules_words = ["Here are some rules for you to look at and stuff.",
                                "Here's some more info."]   
        self.img_rules.blit(pygame.image.load(os.path.join("img",bottom_image)), (50, 0), Rect((0,0),(750,150)))                        
                                
Game().start()
