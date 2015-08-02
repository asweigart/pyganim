"""
This example shows how Pyganim can be used with "simulation time", instead of the actual system clock time as returned by time.time()
"""

import sys
import os
sys.path.append(os.path.abspath('..'))

import pygame
from pygame.locals import *
import time
import pyganim

pygame.init()

# set up the window
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Pyganim Simulation Clock Demo')

# creating the PygAnimation objects for walking/running in all directions
animTypes = 'back_walk front_walk left_walk'.split()
animObjs = {}
for animType in animTypes:
    imagesAndDurations = [('gameimages/crono_%s.%s.gif' % (animType, str(num).rjust(3, '0')), 1) for num in range(6)] # since we are not using the real system clock, "1" here is not "1 millisecond" but 1 step in the simulation clock
    animObjs[animType] = pyganim.PygAnimation(imagesAndDurations)

# create the right-facing sprites by copying and flipping the left-facing sprites
animObjs['right_walk'] = animObjs['left_walk'].getCopy()
animObjs['right_walk'].flip(True, False)
animObjs['right_walk'].makeTransformsPermanent()

# have the animation objects managed by a conductor.
# With the conductor, we can call play() and stop() on all the animtion
# objects at the same time, so that way they'll always be in sync with each
# other.
moveConductor = pyganim.PygConductor(animObjs)


BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BGCOLOR = (100, 50, 50)

mainClock = pygame.time.Clock()





simulationTime = 0 # this is the variable that contains the current "simulation time"
simulationClockFunction = lambda: simulationTime
pyganim.TIME_FUNC = simulationClockFunction
moveConductor.play()

def getPositionAtTime(t):
    """
    Simulation time t runs from 0 to 99

    First quarter: walking right from 50, 50 to 250, 50
    Second quarter: walking down from 250, 50 to 250, 250
    Third quarter: walking left from 250, 250 to 50, 250
    Fourth quarter: walking up from 50, 250 to 50, 50
    """
    if 0 <= t < 25:
        return 50 + ((t - 0) * 8), 50, 'right'
    elif 25 <= t < 50:
        return  250, 50 + ((t - 25) * 8), 'front'
    elif 50 <= t < 75:
        return 250 - ((t - 50) * 8), 250, 'left'
    elif 75 <= t < 100:
        return 50, 250 - ((t - 75) * 8), 'back'


mouseDown = False

while True:
    for event in pygame.event.get(): # event handling loop

        # handle ending the program
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            mouseDown = True
            mousex, mousey = event.pos
            if not (200 <= mousex < 300) or not (390 <= mousey < 430):
                continue
            simulationTime = mousex - 200

        elif event.type == MOUSEBUTTONUP:
            mouseDown = False
        elif event.type == MOUSEMOTION:
            if not mouseDown:
                continue
            mousex, mousey = event.pos
            if not (200 <= mousex < 300) or not (390 <= mousey < 430):
                continue
            simulationTime = mousex - 200


    # draw scene
    windowSurface.fill(BGCOLOR)

    # draw character
    x, y, direction = getPositionAtTime(simulationTime)
    animObjs[direction + '_walk'].blit(windowSurface, (x, y))

    # draw instructions
    instructionSurf = BASICFONT.render('Drag slider to see different points of the simulation. Simulation time: %s' % (simulationTime), True, WHITE)
    instructionRect = instructionSurf.get_rect()
    instructionRect.bottomleft = (10, WINDOWHEIGHT - 10)
    windowSurface.blit(instructionSurf, instructionRect)

    # draw slider
    pygame.draw.rect(windowSurface, WHITE, (200, 400, 100, 20))
    pygame.draw.line(windowSurface, RED, (200 + simulationTime, 390), (200 + simulationTime, 430))

    pygame.display.update()
    mainClock.tick(30) # Feel free to experiment with any FPS setting.