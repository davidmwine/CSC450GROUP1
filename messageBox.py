import pygame
from pygame.locals import *
import os
import Colors
from TextWrap import wrapLine

# These functions should still work if we change where the message box appears.
# displayMsg and displayMsgOK should still look decent if the message box is
# resized; in displayMsgYN, the Yes and No buttons would have to be repositioned.

def displayMsg(scale, rect, font, msg):
    """
    Returns a pygame Surface the size of rect containing msg.
    'rect' should be a pygame Rect object in the desired position.
    """        
    msgBox = pygame.Surface((rect.width, rect.height))
    msgBox.fill(Globals.lightGray)
    lines = wrapline(msg, font, rect.x)
    i = 0
    for line in lines:
        lineYpos = 50*i*scale + 2
        line = font.render(line, True, Color("black"))
        msgBox.blit(line, (2, lineYpos))
        i += 1

    return msgBox


def displayMsgOK(scale, rect, font, msg):
    """
    Returns a tuple containing:
    [0]: a pygame Surface the size of rect containing msg and an OK button.
    [1]: a pygame Rect object covering the OK button, positioned relative to rect.
    'rect' should be a pygame Rect object in the desired position.
    """      
    # Create message box as a surface and display text.
    msgBox = pygame.Surface((rect.width, rect.height))
    msgBox.fill(Globals.lightGray)
    lines = wrapline(msg, font, rect.x)
    i = 0
    for line in lines:
        lineYpos = 50*i*scale + 2
        line = font.render(line, True, Color("black"))
        msgBox.blit(line, (2, lineYpos))
        i += 1

    # Create and position OK button.
    okButton = pygame.Surface((100*scale, 50*scale))
    okRect = okButton.get_rect()
    okButton.fill(Globals.medGray)
    text = font.render("OK", True, Color("black"))
    textPos = text.get_rect()
    textPos.center = okRect.center
    okButton.blit(text, textPos)
    okRect.bottom = msgBox.get_rect().height - 10
    okRect.centerx = msgBox.get_rect().centerx
    msgBox.blit(okButton, okRect)

    return (msgBox, okRect)


def displayMsgYN(scale, rect, font, msg):
    """
    Returns a tuple containing:
    [0]: a pygame Surface the size of rect containing msg and Yes/No buttons.
    [1]: a pygame Rect object covering the Yes button, positioned relative to rect.
    [2]: a pygame Rect object covering the No button, positioned relative to rect.
    'rect' should be a pygame Rect object in the desired position.
    """          
    # Create message box as a surface and display text.
    msgBox = pygame.Surface((rect.width, rect.height))
    msgBox.fill(Globals.lightGray)
    lines = wrapline(msg, font, rect.x)
    i = 0
    for line in lines:
        lineYpos = 50*i*scale + 2
        line = font.render(line, True, Color("black"))
        msgBox.blit(line, (2, lineYpos))
        i += 1

    # Create and position Yes and No buttons.
    yesButton = pygame.Surface((100*scale, 50*scale))
    yesButton.fill(Globals.medGray)
    yesRect = yesButton.get_rect()
    text = font.render("Yes", True, Color("black"))
    textPos = text.get_rect()
    textPos.center = yesRect.center
    yesButton.blit(text, textPos)
    yesRect.bottom = msgBox.get_rect().height - 10
    yesRect.left = 125*scale
    msgBox.blit(yesButton, yesRect)

    noButton = pygame.Surface((100*scale, 50*scale))
    noButton.fill(Globals.medGray)
    noRect = noButton.get_rect()
    text = font.render("No", True, Color("black"))
    textPos = text.get_rect()
    textPos.center = noRect.center
    noButton.blit(text, textPos)
    noRect.bottom = msgBox.get_rect().height - 10
    noRect.right = msgBox.get_rect().width - 125*scale
    msgBox.blit(noButton, noRect)

    return (msgBox, yesRect, noRect)
