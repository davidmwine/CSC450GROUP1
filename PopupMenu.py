import pygame
import sys
import os
from Controls import Button
from RadioButton import RadioGroup
from Sound import Sound

class PopupMenu(object):
    def __init__(self, parent, soundOn):
        self.displayInfo = pygame.display.Info()
        self.clock = pygame.time.Clock()
        self.parent = parent
        self.width = self.parent.get_width() / 2
        self.height = self.parent.get_height() / 2
        self.area = parent.subsurface((self.parent.get_width() / 4), (self.parent.get_height() / 4), self.width, self.height)
        self.screenModes = [(960, 540), (1280, 720), (1600, 900), (1920, 1080), (960, 720)]## various screen sizes available
        self.resOpt = self.screenModes.index((self.displayInfo.current_w, self.displayInfo.current_h)) # current resolution option
        self.popupActive = False
        self.optionActive = False
        self.exitCheckActive = False
        self.rulesActive = False
        self.bgMusic = Sound('start_menu')
        self.soundOn = soundOn
        print(self.soundOn)

    def loadButtons(self):
        # RADIO BUTTON GROUP
        self.resolveButton = RadioGroup(self.area)
        self.resolveButton.newButton(self.area.get_width() / 2 - 80, self.area.get_height() / 2 + 5, 5)
        self.resolveButton.newButton(self.area.get_width() / 2 - 80, self.area.get_height() / 2 + 25, 5)
        self.resolveButton.newButton(self.area.get_width() / 2 - 80, self.area.get_height() / 2 + 45, 5)
        self.resolveButton.newButton(self.area.get_width() / 2 + 20, self.area.get_height() / 2 + 5, 5)
        #self.resolveButton.newButton(self._area.get_width() / 2 + 20, self._area.get_height() / 2 + 25, 5) #4:3 not supported yet
        self.resolveButton.setCurrent(self.resOpt)

        #Sound buttons
        self.img_on = pygame.image.load(os.path.join("img", "on_small.png")).convert_alpha()
        self.img_off = pygame.image.load(os.path.join("img", "off_small.png")).convert_alpha()
        
    def changeResolution(self, X, Y):
        # supposed to check radio button and return whichever resolution was selected
        if self.resolveButton.checkButton(X - self.parent.get_width() / 4, Y - self.parent.get_height() / 4):
            self.resOpt = self.resolveButton.getCurrent()
            return self.screenModes[self.resolveButton.getCurrent()]
        else:
            return None

    def makePopupMenu(self):
        self.popupActive = True
        self.optionActive = False
        self.rulesActive = False
        self.exitCheckActive = False
        self.area.fill((190, 192, 194))
        self.textOptions = pygame.font.Font(os.path.join("font","berlin.ttf"), 30).render("Options", True, (94, 0, 9))
        self.area.blit(self.textOptions, (self.area.get_width()/2 - (0.5 * self.textOptions.get_width()), 5))
        self.resumeButton = Button(self.area, pygame.Rect(self.area.get_width() / 2 - 100, self.area.get_height() / 2 - 80, 200, 30), "Resume Game", (94, 0, 9), (190, 192, 194))
        self.saveButton = Button(self.area, pygame.Rect(self.area.get_width() / 2 - 100, self.area.get_height() / 2 - 40, 200, 30), "Rules", (94, 0, 9), (190, 192, 194))
        self.gameOptionsButton = Button(self.area, pygame.Rect(self.area.get_width() / 2 - 100, self.area.get_height() / 2, 200, 30), "Game Options", (94, 0, 9), (190, 192, 194))
        self.exitButton = Button(self.area, pygame.Rect(self.area.get_width() / 2 - 100, self.area.get_height() / 2 + 40, 200, 30), "Exit Game", (94, 0, 9), (190, 192, 194))

    def gameOptions(self):
        self.popupActive = True
        self.optionActive = True
        self.exitCheckActive = False
        self.area.fill((190, 192, 194))
        # header
        self.textOptions = pygame.font.Font(os.path.join("font","berlin.ttf"), 30).render("Game Options", True, (94, 0, 9))
        self.area.blit(self.textOptions, (self.area.get_width()/2 - (0.5 * self.textOptions.get_width()), 5))

        # back button
        self.exitButton = Button(self.area, pygame.Rect(self.area.get_width() / 2 - 100, self.area.get_height() / 2 - 80, 200, 30), "Back", (94, 0, 9), (190, 192, 194))

        # resolution options
        self.loadButtons()
        self.textResolution = pygame.font.Font(os.path.join("font","berlin.ttf"), 20).render("Resolution Options", True, (94, 0, 9))
        self.area.blit(self.textResolution, (self.area.get_width() / 2 - (0.5 * self.textResolution.get_width()), self.area.get_height() / 2 - 30))
        self.resolutionText1 = pygame.font.Font(os.path.join("font", "berlin.ttf"), 10).render("960x540", True, (0, 0, 0))
        self.resolutionText2 = pygame.font.Font(os.path.join("font", "berlin.ttf"), 10).render("1280x720", True, (0, 0, 0))
        self.resolutionText3 = pygame.font.Font(os.path.join("font", "berlin.ttf"), 10).render("1600x900", True, (0, 0, 0))
        self.resolutionText4 = pygame.font.Font(os.path.join("font", "berlin.ttf"), 10).render("1920x1080", True, (0, 0, 0))
        # self.resolutionText5 = pygame.font.Font(os.path.join("font", "berlin.ttf"), 10).render("960x720", True, (0, 0, 0))
        self.area.blit(self.resolutionText1, (self.area.get_width() / 2 - 70, self.area.get_height() / 2))
        self.area.blit(self.resolutionText2, (self.area.get_width() / 2 - 70, self.area.get_height() / 2 + 20))
        self.area.blit(self.resolutionText3, (self.area.get_width() / 2 - 70, self.area.get_height() / 2 + 40))
        self.area.blit(self.resolutionText4, (self.area.get_width() / 2 + 30, self.area.get_height() / 2))
        #self._area.blit(self.resolutionText5, (self._area.get_width() / 2 + 30, self._area.get_height() / 2 + 20)) #4:3 not supported yet
        self.resolveButton.draw()

        #Sound heading
        self.textSound = pygame.font.Font(os.path.join("font","berlin.ttf"), 20).render("Music", True, (94, 0, 9))
        self.area.blit(self.textSound, (self.area.get_width() / 2 - (0.5 * self.textSound.get_width()), self.area.get_height() - 65))

        #Sound button - On initial popup
        if self.soundOn:
            self.area.blit(self.img_on,(self.area.get_width()/2 - 21,self.area.get_height() - 40))
        else:
            self.area.blit(self.img_off,(self.area.get_width()/2 - 21,self.area.get_height() - 40))
   
    def soundChange(self):
        #Sound button
        if not self.soundOn:
            self.area.blit(self.img_on,(self.area.get_width()/2 - 21,self.area.get_height() - 40))
        else:
            self.area.blit(self.img_off,(self.area.get_width()/2 - 21,self.area.get_height() - 40))

        # Stop or start sound
        if self.soundOn:
            pygame.mixer.stop()
        else:
            self.bgMusic.play()

        self.soundOn = not self.soundOn

    def rules(self, pageNum=None):
        self.popupActive = True
        self.rulesActive = True
        self.optionActive = False
        self.exitCheckActive = False
        self.area.fill((190, 192, 194))

        self.imgArrow = pygame.image.load(os.path.join("img","arrow.png")).convert_alpha()
        self.imgArrowleft = pygame.image.load(os.path.join("img","arrowLeft.png")).convert_alpha()
        
        # header
        self.textOptions = pygame.font.Font(os.path.join("font","berlin.ttf"), 30).render("Rules", True, (94, 0, 9))
        self.area.blit(self.textOptions, (self.area.get_width()/2 - (0.5 * self.textOptions.get_width()), 0))

        # back button
        self.exitButton = Button(self.area, pygame.Rect(self.area.get_width() / 2 - 50,
                                                        self.area.get_height() / 2 + 95,
                                                        100, 30),
                                 "Back", (94, 0, 9), (190, 192, 194))

        if pageNum == 1:
            self.rulesHeader = 'Introduction'
            self.rulesWords = ['Mastering MSU is a turn-based game for online play.',
                                'The game supports up to six players competing',
                                'against each other to rule the campus. The game is',
                                'free to download and free to play.']
            
        if pageNum == 2:
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

        if pageNum == 3:
            self.rulesHeader = 'Game Play'
            self.rulesWords = ['Each player has a token that starts on the space',
                               "representing Carrington Hall.  On a player's turn,",
                               'he/she rolls the dice and his/her token is moved',
                               'clockwise the corresponding number of spaces.',
                               'Depending on what space the player lands on,',
                               'various actions may be taken or the player may',
                               'be given a decision to make.']    
            
        if pageNum == 4:
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
            
        if pageNum == 5:
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

        if pageNum == 6:
            self.rulesHeader = 'Sports Venues'
            self.rulesWords = ['\u2022 Hammons Field',
                               '\u2022 JQH Arena',
                               '\u2022 Allison South Stadium',
                               '\u2022 Plaster Sports Complex',
                               'Sports venue spaces on the board have a green',
                               'border around their trapezoid. If a player lands on a',
                               'sports venue that is currently unowned, he or she can',
                               'buy it. If it is owned by another player, the player who',
                               'lands on it pays the owner a fee of $1000 times the',
                               'number of Graduate Points earned so far by player',
                               'who landed on the sports venue.']

        if pageNum == 7:
            self.rulesHeader = 'Stealable Buildings'
            self.rulesWords = ['\u2022 Plaster Student Union',
                               '\u2022 University Bookstore',
                               'Each of these buildings generates $50,000 for the',
                               'owner on each turn that he/she owns it.  They can be',
                               'bought (from the bank) when a player lands on them,',
                               'regardless of whether they are already owned by',
                               'another player.']

        if pageNum == 8:
            self.rulesHeader = 'Utilities'
            self.rulesWords = ['These buildings cannot be owned.  When a player',
                               'lands on one of them, he/she must pay a fee:',
                               '\u2022 Power House: $200,000 fee',
                               '\u2022 Central Maintenance: $50,000 per building owned']
            
        if pageNum == 9:
            self.rulesHeader = 'Bear Chest Spaces'
            self.rulesWords = ['\u2022 Foster Recreation Center',
                               '\u2022 Juanita K Hammons',
                               '\u2022 Hammons Student Center',
                               '\u2022 Meyer Library',
                               'Bear chest spaces have no trapezoid.  When a player',
                               'lands on one of them, a card from the center of the',
                               'board is turned over and its instructions are followed.']

        if pageNum == 10:
            self.rulesHeader = 'Bear Park North/South'
            self.rulesWords = ['If a player lands on Bear Park North, he/she loses',
                               'his/her next turn due to the inconvenience of parking',
                               'far away from most buildings.',
                               'If a player lands on Bear Park South, he/she gets an',
                               'extra turn.']

        if pageNum == 11:
            self.rulesHeader = 'Carrington Hall'
            self.rulesWords = ['Each player receives $200,000 and the appropriate',
                               'number of Graduate Points when passing',
                               'Carrington Hall.']

        if pageNum == 12:
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

        if pageNum == 13:
            self.rulesHeader = 'Inflation'
            self.rulesWords = ['All ownable buildings (including academic buildings,',
                               'sports venues, and stealable buildings) initially cost',
                               '$200,000.  After every three rounds (i.e., after each',
                               'player has had three turns), these costs increase',
                               "by 20%. Fees for landing on other players' buildings",
                               "will also increase, since they're a percentage of",
                               'current building cost. (See Upgrades.)']
                                                                                                                                                                                                                  
        if pageNum == 14:
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

        if pageNum == 15:
            self.rulesHeader = 'Upgrades 2'
            self.rulesWords = ['If a player owns three consecutive academic buildings,',
                               'he/she can choose to upgrade to the Doctorate level',
                               'by paying a $500,000 fee (or the appropriate amount',
                               "if they're already upgraded).  The benefits of upgrading",
                               'are an increased number of Graduate Points and',
                               'receiving increased fees when other players land on',
                               'the building:',
                               '\u2022 Associate level: 10% of current building cost',
                               '\u2022 Bachelor level: 20% of current building cost',
                               '\u2022 Master level: 30% of current building cost',
                               '\u2022 Doctoral level: 40% of current building cost']

        if pageNum == 16:
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

        if pageNum == 17:
            self.rulesHeader = 'Trading'
            self.rulesWords = ['Players may choose to sell or trade any buildings',
                               'with each other.']
            
        textOut = self.fontOp(20,"helvetica").render(self.rulesHeader,True,(35,35,35))
        self.area.blit(textOut, (self.area.get_width() / 2 - textOut.get_width() / 2, self.area.get_height() / 2 - 100))

        #Display rules on page  
        for text in range(len(self.rulesWords)): 
            textOut = self.fontOp(12,"helvetica").render(self.rulesWords[text],True,(35,35,35))
            self.area.blit(textOut,(self.area.get_width() / 2 - textOut.get_width()
                                    / 2,self.area.get_height() / 2 - 75 +text*15))

        if pageNum < 17:
            self.area.blit(self.imgArrow,(self.area.get_width() / 2 + 100, self.area.get_height() / 2 + 95))
        if pageNum > 1:
            self.area.blit(self.imgArrowleft,(self.area.get_width() / 2 - 160, self.area.get_height() / 2 + 95))


    def exitCheck(self):
        self.popupActive = True
        self.rulesActive = False
        self.optionActive = False
        self.exitCheckActive = True
        self.area.fill((190, 192, 194))
        self.text = pygame.font.Font(os.path.join("font","berlin.ttf"), 20).render("Are you sure you want to exit?", True, (94, 0, 9))
        self.area.blit(self.text, (self.area.get_width()/2 - (0.5 * self.text.get_width()), 5))
        self.exitButtonYes = Button(self.area, pygame.Rect(self.area.get_width() / 2 - 100, self.area.get_height() / 2 - 60, 200, 30), "Yes", (94, 0, 9), (190, 192, 194))
        self.exitButtonNo = Button(self.area, pygame.Rect(self.area.get_width() / 2 - 100, self.area.get_height() / 2 - 20, 200, 30), "No", (94, 0, 9), (190, 192, 194))

    def getWidth(self):
        return self.area.get_width()

    def getHeight(self):
        return self.area.get_height()

    def getPopupActive(self):
        return self.popupActive

    def setPopupActive(self, x):
        self.popupActive = x

    def getOptionsActive(self):
        return self.optionActive

    def setOptionsActive(self, x):
        self.optionActive = x

    def getExitCheckActive(self):
        return self.exitCheckActive

    def setExitCheckActive(self, x):
        self.ExitCheckActive = x

    #copy from msugame
    def fontOp(self, size, fontName):  #Pick font size and type
        if fontName == "helvetica":
            fontAndSize = pygame.font.Font(os.path.join("font","helvetica.otf"),int(size)) # "font" is directory for the font file
        elif fontName == "berlin":
            fontAndSize = pygame.font.Font(os.path.join("font","berlin.ttf"),int(size))
        return fontAndSize

    def getRulesActive(self):
        return self.rulesActive

    def setRulesActive(self, x):
        self.rulesActive = x
