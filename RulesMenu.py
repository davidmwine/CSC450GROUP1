'''Rules listing in start menu'''
import pygame
from pygame.locals import *
import os
import sys

class Rules(object):
    def __init__(self, screen, fontOp, yOffset, click):
        self.screen = screen
        self.fontOp = fontOp
        self.yOffset = yOffset
        self.loadImages()
        self.loadText()
        self.rulesCount = 17  #Number of rules/rule pages
        self.click = click

    def loadImages(self):     
        self.imgArrow = pygame.image.load(os.path.join("img","arrow.png")).convert_alpha()
        self.imgArrowleft = pygame.image.load(os.path.join("img","arrowLeft.png")).convert_alpha()
        self.imgMenuBG = pygame.image.load(os.path.join("img","menu_bg4.png")).convert()

    def loadText(self):
        self.textExitRules = self.fontOp(22,"berlin").render("Exit Rules",True,(220,146,40))
        #Index text
        self.textIntro = self.fontOp(20,"berlin").render("Introduction",True,(255,255,255))
        self.textObjective = self.fontOp(20,"berlin").render("Objective",True,(255,255,255))
        self.textGamePlay = self.fontOp(20,"berlin").render("Game Play",True,(255,255,255))
        self.textBuildings = self.fontOp(20,"berlin").render("Buildings",True,(255,255,255))
        self.textAcademic = self.fontOp(20,"berlin").render("Academic Buildings",True,(255,255,255))
        self.textSports = self.fontOp(20,"berlin").render("Sports Venues",True,(255,255,255))
        self.textBearChest = self.fontOp(20,"berlin").render("Bear Chest Spaces",True,(255,255,255))
        self.textUtilities = self.fontOp(20,"berlin").render("Utilities",True,(255,255,255))
        self.textStealable = self.fontOp(20,"berlin").render("Stealable Buildings",True,(255,255,255))
        self.textBearPark = self.fontOp(20,"berlin").render("Bear Park North/South",True,(255,255,255))
        self.textCarrington = self.fontOp(20,"berlin").render("Carrington Hall",True,(255,255,255))
        self.textAccreditation = self.fontOp(20,"berlin").render("Accreditation Review",True,(255,255,255))
        self.textInflation = self.fontOp(20,"berlin").render("Inflation",True,(255,255,255))
        self.textUpgrades1 = self.fontOp(20,"berlin").render("Upgrades 1",True,(255,255,255))
        self.textUpgrades2 = self.fontOp(20,"berlin").render("Upgrades 2",True,(255,255,255))
        self.textGraduate = self.fontOp(20,"berlin").render("Graduate Points",True,(255,255,255))
        self.textTrading = self.fontOp(20,"berlin").render("Trading",True,(255,255,255))

    def buttonClick(self):
        mouseX,mouseY = pygame.mouse.get_pos()
        #Exit rules
        if mouseX > self.rulesXPosition + 494\
        and mouseX < self.rulesXPosition + 595\
        and mouseY > self.screen.get_height()/8+self.yOffset-5 \
        and mouseY < self.screen.get_height()/8+self.yOffset+self.textExitRules.get_height()+5:
            self.click.play()
            return False
        #Prev page
        if self.rulesPage > 1:
            if mouseX > self.rulesXPosition - 10\
            and mouseX < self.rulesXPosition + 65\
            and mouseY > self.screen.get_height()/8+self.yOffset+390 \
            and mouseY < self.screen.get_height()/8+self.yOffset+self.imgArrowleft.get_height()+400:
                self.click.play()
                self.rulesNextPage(-1)
                return True
        #Next page
        if self.rulesPage < self.rulesCount:
            if mouseX > self.rulesXPosition + 545\
            and mouseX < self.rulesXPosition + 620\
            and mouseY > self.screen.get_height()/8+self.yOffset+390 \
            and mouseY < self.screen.get_height()/8+self.yOffset+self.imgArrow.get_height()+400:
                self.click.play()
                self.rulesNextPage(1)
                return True

        #Index
        indexXPosition = 20
        indexYPosition = self.screen.get_height()/8 + self.yOffset - 25     # Subtracting 25 so it will be correct when incremented.
        for i in range(self.rulesCount):
            indexYPosition += 25
                                                                            # Using the width of the widest item.            
            if mouseX > indexXPosition \
            and mouseX < indexXPosition + self.textBearPark.get_width()\
            and mouseY > indexYPosition \
            and mouseY < indexYPosition + self.textIntro.get_height():      
                self.click.play()
                self.rulesNextPage(i+1, True)
                return True
     
        return True
        

    def rulesNextPage(self, pageNum=None, index=False):
        if pageNum == None:
            self.rulesPage = 1
        elif index == True:
            self.rulesPage = pageNum
        else:
            self.rulesPage += pageNum

        if self.rulesPage == 1:
            self.rulesHeader = 'Introduction'
            self.rulesWords = ['Mastering MSU is a turn-based game for online play.',
                                'The game supports up to six players competing',
                                'against each other to rule the campus. The game is',
                                'free to download and free to play.']
            
        if self.rulesPage == 2:
            self.rulesHeader = 'Objective'
            self.rulesWords = ['Each player plays as the dean of one of the seven',
                               'colleges at MSU: ',
                               '\u2022 Agriculture             \u2022 Health and Human Services',
                               '\u2022 Arts and Letters    \u2022 Humanities and Public Affairs',
                               '\u2022 Business               \u2022 Natural and Applied Sciences',
                               '\u2022 Education', 
                               'The winner is the dean who, while avoiding bankruptcy,',
                               'can graduate the most students with the highest',
                               'degrees. (See Graduate Points.)']

        if self.rulesPage == 3:
            self.rulesHeader = 'Game Play'
            self.rulesWords = ['Each player has a token that starts on the space',
                               "representing Carrington Hall.  On a player's turn,",
                               'he/she rolls the dice and his/her token is moved',
                               'clockwise the corresponding number of spaces.',
                               'Depending on what space the player lands on,',
                               'various actions may be taken or the player may',
                               'be given a decision to make.']    
            
        if self.rulesPage == 4:
            self.rulesHeader = 'Buildings'
            self.rulesWords = ['Each space on the board represents a building',
                               'on campus. There are five "types" of buildings,',
                               'plus the corner spaces.  See the following pages',
                               'for more details about the different types of buildings.',
                               '\u2022 Academic Buildings',
                               '\u2022 Sports Venues',
                               '\u2022 Bear Chest Spaces',
                               '\u2022 Utilities',
                               '\u2022 Stealable Buildings']
            
        if self.rulesPage == 5:
            self.rulesHeader = 'Academic Buildings'
            self.rulesWords = ['Half of the buildings on the board are academic',
                               'buildings.  Their spaces on the board have a trapezoid',
                               'with no border.  If a player lands on an academic',
                               'building that is currently unowned, he or she can buy it.',
                               'If it is owned by another player, the player who landed',
                               'on it pays the owner fees (for the privilege of holding',
                               'classes in that building).  Academic buildings are the',
                               'only buildings that directly help a player earn Graduate',
                               'Points and are the only buildings involved in upgrades.']

        if self.rulesPage == 6:
            self.rulesHeader = 'Sports Venues'
            self.rulesWords = ['\u2022 Hammons Field',
                               '\u2022 JQH Arena',
                               '\u2022 Allison South Stadium',
                               '\u2022 Plaster Sports Complex',
                               'Sports venue spaces on the board have a green',
                               'border around their trapezoid. If a player lands on a',
                               'sports venue that is currently unowned, he or she can',
                               'buy it. If it is owned by another player, the player who',
                               'lands on it pays the owner a fee of $50000 plus',
                               '$10000 times the number of Graduate Points earned so',
                               'far by player who landed on the sports venue.']

        if self.rulesPage == 7:
            self.rulesHeader = 'Stealable Buildings'
            self.rulesWords = ['\u2022 Plaster Student Union',
                               '\u2022 University Bookstore',
                               'Each of these buildings generates $50,000 for the',
                               'owner on each turn that he/she owns it.  They can be',
                               'bought (from the bank) when a player lands on them,',
                               'regardless of whether they are already owned by',
                               'another player.']

        if self.rulesPage == 8:
            self.rulesHeader = 'Utilities'
            self.rulesWords = ['These buildings cannot be owned.  When a player',
                               'lands on one of them, he/she must pay a fee:',
                               '\u2022 Power House: $200,000 fee',
                               '\u2022 Central Maintenance: $50,000 per building owned']
            
        if self.rulesPage == 9:
            self.rulesHeader = 'Bear Chest Spaces'
            self.rulesWords = ['\u2022 Foster Recreation Center',
                               '\u2022 Juanita K Hammons',
                               '\u2022 Hammons Student Center',
                               '\u2022 Meyer Library',
                               'Bear chest spaces have no trapezoid.  When a player',
                               'lands on one of them, a card from the center of the',
                               'board is turned over and its instructions are followed.']

        if self.rulesPage == 10:
            self.rulesHeader = 'Bear Park North/South'
            self.rulesWords = ['If a player lands on Bear Park North, he/she loses',
                               'his/her next turn due to the inconvenience of parking',
                               'far away from most buildings.',
                               'If a player lands on Bear Park South, he/she gets an',
                               'extra turn.']

        if self.rulesPage == 11:
            self.rulesHeader = 'Carrington Hall'
            self.rulesWords = ['Each player receives $300,000 and the appropriate',
                               'number of Graduate Points when passing',
                               'Carrington Hall.']

        if self.rulesPage == 12:
            self.rulesHeader = 'Accreditation Review'
            self.rulesWords = ['If a player lands on (or is sent to) Accreditation Review,',
                               'on his/her next turn, he/she must roll the dice to',
                               'determine whether the college passed the Accreditation',
                               'Review.  If the roll is even, the college passed, and the',
                               'player moves according to the dice roll.  If the roll is odd,',
                               'the player must pay $100,000 to make improvements',
                               'required by the accrediting committee.  On his/her next',
                               'turn, the player must again roll to determine whether',
                               'the college passed Accreditation review.']

        if self.rulesPage == 13:
            self.rulesHeader = 'Inflation'
            self.rulesWords = ['All ownable buildings (including academic buildings,',
                               'sports venues, and stealable buildings) initially cost',
                               '$200,000.  After every three rounds (i.e., after each',
                               'player has had three turns), these costs increase',
                               "by 20%. Fees for landing on other players' buildings",
                               "will also increase, since they're a percentage of",
                               'current building cost. (See Upgrades.)']
                                                                                                                                                                                                                  
        if self.rulesPage == 14:
            self.rulesHeader = 'Upgrades 1'
            self.rulesWords = ['When a player buys an academic building, it can grant',
                               'Associate degrees.  If a player owns two or more',
                               'academic buildings, he/she can choose to upgrade',
                               'any of those buildings to the Bachelor level by paying',
                               'a $100,000 fee.  If a player owns two consecutive',
                               'academic buildings (meaning that there are no other',
                               'academic buildings between them, though there could',
                               'be other buildings), he/she can choose to upgrade to',
                               'the Master level by paying a $250,000 fee (or $150,000',
                               "if they're already at the Bachelor level)."]

        if self.rulesPage == 15:
            self.rulesHeader = 'Upgrades 2'
            self.rulesWords = ['If a player owns three consecutive academic buildings,',
                               'he/she can choose to upgrade to the Doctorate level',
                               'by paying a $500,000 fee (or the appropriate amount',
                               "if they're already upgraded).  The benefits of upgrading",
                               'are an increased number of Graduate Points and',
                               'receiving increased fees when other players land on',
                               'the building:',
                               '\u2022 Associate level: 20% of current building cost',
                               '\u2022 Bachelor level: 40% of current building cost',
                               '\u2022 Master level: 60% of current building cost',
                               '\u2022 Doctoral level: 80% of current building cost']

        if self.rulesPage == 16:
            self.rulesHeader = 'Graduate Points'
            self.rulesWords = ['When a player passes Carrington Hall, he/she',
                               'receives Graduate Points based on the number',
                               'of buildings owned and their degree levels.',
                               '\u2022 Associate level: 1 Graduate Point per building',
                               '\u2022 Bachelor level: 2 Graduate Points per building',
                               '\u2022 Master level: 3 Graduate Points per building',
                               '\u2022 Doctoral level: 4 Graduate Points per building',
                               'The first player to earn 50 graduate points wins the',
                               'game.  The game can also be won if all other players',
                               'go bankrupt.']

        if self.rulesPage == 17:
            self.rulesHeader = 'Trading'
            self.rulesWords = ['Players may choose to sell or trade any buildings',
                               'with each other.']

    def run(self):
        self.rulesNextPage()

        self.rulesIndex = [self.textIntro, self.textObjective, self.textGamePlay, self.textBuildings,
                           self.textAcademic, self.textSports, self.textStealable, self.textUtilities,
                           self.textBearChest, self.textBearPark, self.textCarrington,
                           self.textAccreditation, self.textInflation, self.textUpgrades1,
                           self.textUpgrades2, self.textGraduate, self.textTrading]

        # On the smallest screen size, we have to move the rules over to make room for the index.
        if self.screen.get_width() < 1000:
            self.rulesXPosition = 3 * self.screen.get_width()/10
        else:
            self.rulesXPosition = self.screen.get_width()/2 - 300
        
        rulesExit = False      
        while not rulesExit:
            self.screen.blit(pygame.transform.scale(self.imgMenuBG,(self.screen.get_width(),\
                            int(self.screen.get_height()-(2*self.yOffset)))),(0,self.yOffset))

            self.text_header = self.fontOp(50,"berlin").render(self.rulesHeader,True,(255,255,255))
            self.screen.blit(self.text_header,(self.screen.get_width()/2-0.5*self.text_header.get_width(),self.screen.get_height()/50+self.yOffset))

            #Rules rects
            pygame.draw.rect(self.screen,(255,255,255),Rect((self.rulesXPosition, self.screen.get_height()/8+self.yOffset),\
                                                            (600,420)))
            pygame.draw.rect(self.screen,(0,0,0),Rect((self.rulesXPosition, self.screen.get_height()/8+self.yOffset),\
                                                      (600,420)),2)

            #Page number / exit button
            self.screen.blit(self.textExitRules,(self.rulesXPosition + 498, self.screen.get_height()/8+self.yOffset))
            self.screen.blit(self.fontOp(22,"berlin").render(str(self.rulesPage)+" of "+\
                                str(self.rulesCount),True,(220,146,40)),(self.rulesXPosition + 6,self.screen.get_height()/8+self.yOffset))

            #Draw red line
            pygame.draw.line(self.screen, (242,107,122), (self.rulesXPosition + 2, 170 + self.yOffset),\
                             (self.rulesXPosition + 598, 170 + self.yOffset), 1)
            #Draw blue lines
            for line in range(12): 
                pygame.draw.line(self.screen, (209,229,240), (self.rulesXPosition + 2, 195+self.yOffset+line*25),\
                                 (self.rulesXPosition + 598, 195+self.yOffset+line*25), 1)
            
            #Display rules index
            indexXPosition = 20
            indexYPosition = self.screen.get_height()/8 + self.yOffset
            for i in range(len(self.rulesIndex)):
                self.screen.blit(self.rulesIndex[i], (indexXPosition, indexYPosition))
                indexYPosition += 25  
                    
            #Next/Prev rule arrows
            if self.rulesPage < self.rulesCount:
                self.screen.blit(self.imgArrow,(self.rulesXPosition + 550, self.screen.get_height()/8+self.yOffset+395))
            if self.rulesPage > 1:
                self.screen.blit(self.imgArrowleft,(self.rulesXPosition - 15, self.screen.get_height()/8+self.yOffset+395))

            #Display rules on page  
            for text in range(len(self.rulesWords)): 
                textOut = self.fontOp(18,"helvetica").render(self.rulesWords[text],True,(35,35,35))
                self.screen.blit(textOut,(self.rulesXPosition + 50, 176+self.yOffset+text*25))
                
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        rulesExit = True
                        break
                elif event.type == MOUSEBUTTONDOWN: 
                    if not self.buttonClick():
                        rulesExit = True
                        break
                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
            pygame.display.update()
        return "start"
