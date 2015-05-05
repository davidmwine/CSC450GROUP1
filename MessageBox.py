import pygame
from pygame.locals import *
import os
import Colors
from TextWrap import wrapLine

# These functions should still work if we change where the message box appears.
# displayMsg and displayMsgOK should still look decent if the message box is
# resized; in displayMsgYN, the Yes and No buttons would have to be repositioned.


def displayMsg(scale, smallRect, largeRect, font, msg):
    """
    This method initially tries to fit msg into smallRect; if it won't fit,
    it uses largeRect.
    Returns a tuple containing:
    [0]: a string indicating the size of the rectangle used, "small" or "large".
    [1]: a pygame Surface the size of the indicated size containing msg.
    """
    size = "small"
    padding = 5*scale
    lines = wrapLine(msg, font, smallRect.width - 2*padding)
    lineHeight = font.get_linesize()
    textHeight = 1.3 * lineHeight * (len(lines)-1) + lineHeight + 2*padding
    if textHeight <= smallRect.height:
        msgBox = pygame.Surface((smallRect.width, smallRect.height))
    else:
        msgBox = pygame.Surface((largeRect.width, largeRect.height))
        lines = wrapLine(msg, font, largeRect.width - 2*padding)
        size = "large"
    msgBox.fill(Colors.LIGHTGRAY)
    
    i = 0
    for line in lines:
        lineYpos = 1.3 * i * lineHeight + padding     # 1.3 is line spacing
        line = font.render(line, True, Color("black"))
        msgBox.blit(line, (padding, lineYpos))
        i += 1

    return (size, msgBox)


def displayMsgOK(scale, rect, font, msg):
    """
    Returns a tuple containing:
    [0]: a pygame Surface the size of rect containing msg and an OK button.
    [1]: a pygame Rect object covering the OK button, positioned relative to rect.
    'rect' should be a pygame Rect object in the desired position.
    """      
    # Create message box as a surface and display text.
    padding = 5*scale
    msgBox = pygame.Surface((rect.width, rect.height - 2*padding))
    msgBox.fill(Colors.LIGHTGRAY)
    
    lines = wrapLine(msg, font, rect.width)
    lineHeight = font.get_linesize()
    i = 0
    for line in lines:
        lineYpos = 1.5 * i * lineHeight + padding   # 1.5 is line spacing
        line = font.render(line, True, Color("black"))
        msgBox.blit(line, (padding, lineYpos))
        i += 1

    # Create and position OK button.
    okButton = pygame.Surface((100*scale, 50*scale))
    okRect = okButton.get_rect()
    okButton.fill(Colors.MEDGRAY)
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
    padding = 5*scale
    msgBox = pygame.Surface((rect.width, rect.height))
    msgBox.fill(Colors.LIGHTGRAY)
    
    lines = wrapLine(msg, font, rect.width - 2*padding)
    lineHeight = font.get_linesize()
    i = 0
    for line in lines:
        lineYpos = 1.5 * i * lineHeight + padding   # 1.5 is line spacing
        line = font.render(line, True, Color("black"))
        msgBox.blit(line, (padding, lineYpos))
        i += 1

    # Create and position Yes and No buttons.
    yesButton = pygame.Surface((100*scale, 50*scale))
    yesButton.fill(Colors.MEDGRAY)
    yesRect = yesButton.get_rect()
    text = font.render("Yes", True, Color("black"))
    textPos = text.get_rect()
    textPos.center = yesRect.center
    yesButton.blit(text, textPos)
    yesRect.bottom = msgBox.get_rect().height - 10
    yesRect.left = 125*scale
    msgBox.blit(yesButton, yesRect)

    noButton = pygame.Surface((100*scale, 50*scale))
    noButton.fill(Colors.MEDGRAY)
    noRect = noButton.get_rect()
    text = font.render("No", True, Color("black"))
    textPos = text.get_rect()
    textPos.center = noRect.center
    noButton.blit(text, textPos)
    noRect.bottom = msgBox.get_rect().height - 10
    noRect.right = msgBox.get_rect().width - 125*scale
    msgBox.blit(noButton, noRect)

    return (msgBox, yesRect, noRect)
