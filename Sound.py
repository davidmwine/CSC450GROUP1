import pygame, os, sys

class Sound(object):
    
    def __init__(self, soundID):
        self.soundID = soundID 
        self.soundOff1 = False
        self.soundOff2 = False
        self.soundOff3 = False
        self.load_sound()

    def load_sound(self):
        self.sound_intro = pygame.mixer.Sound(os.path.join('sound','radio.wav'))
        self.sound_start_menu = pygame.mixer.Sound(os.path.join('sound','start_menu.wav'))
        self.sound_click = pygame.mixer.Sound(os.path.join('sound','click.wav'))

    def setSound(self, soundID):
        if soundID == 'intro':
            self.soundOff1 = not self.soundOff1
        if soundID == 'start_menu':
            self.soundOff2 = not self.soundOff2
        if soundID == 'click':
            self.soundOff3 = not self.soundOff3
        
    def play(self):
        if self.soundID == 'intro':
            if self.soundOff1 == False:
                self.sound_intro.play()
                self.sound_intro.fadeout(6000)
        if self.soundID == 'start_menu':
            if self.soundOff2 == False:
                self.sound_start_menu.play(-1)
            else:
                pygame.mixer.stop()
        if self.soundID == 'click':
            if self.soundOff3 == False:
                self.sound_click.play()
            else:
                pygame.mixer.stop()

  
