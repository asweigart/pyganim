# gif_demo.py - Loading the PygAnimation object from a single animated gif file.
#
# This program just runs a single animation. It shows you what you need to do to use Pyganim. Basically:
#   1) Import the pyganim module
#   2) Create a pyganim.PygAnimation object, passing the constructor the filename of an animated gif.
#   3) Call the play() method.
#   4) Call the blit() method.
#
# The animation images come from POW Studios, and are available under an Attribution-only license.
# Check them out, they're really nice.
# http://powstudios.com/

import sys
import os
sys.path.append(os.path.abspath('..'))
import pygame
from pygame.locals import *
import time
import pyganim

pygame.init()

# set up the window
windowSurface = pygame.display.set_mode((385, 380), 0, 32)
pygame.display.set_caption('Pyganim GIF Demo')

# create the animation objects   ('filename of image',    duration_in_seconds)
bananaAnim = pyganim.PygAnimation('banana.gif')
bananaAnim.play() # there is also a pause() and stop() method

mainClock = pygame.time.Clock()
BGCOLOR = (100, 50, 50)
while True:
    windowSurface.fill(BGCOLOR)
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

    bananaAnim.blit(windowSurface, (10, 10))

    pygame.display.update()
    mainClock.tick(30) # Feel free to experiment with any FPS setting.