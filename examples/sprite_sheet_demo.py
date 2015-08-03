# trex image from Wyverii on http://opengameart.org/content/unsealed-terrex

import sys
import os
sys.path.append(os.path.abspath('..'))
import pygame
from pygame.locals import *
import pyganim

pygame.init()

# set up the window
windowSurface = pygame.display.set_mode((320, 240), 0, 32)
pygame.display.set_caption('Sprite Sheet Demo')

# create the animation objects
rects = [(  0, 154, 94, 77),
         ( 94, 154, 94, 77),
         (188, 154, 94, 77),
         (282, 154, 94, 77),
         (376, 154, 94, 77),
         (470, 154, 94, 77),
         (564, 154, 94, 77),
         (658, 154, 94, 77),
         (752, 154, 94, 77),]

allImages = pyganim.getImagesFromSpriteSheet('terrex_0.png', rects=rects)
frames = list(zip(allImages, [100] * len(allImages)))

dinoAnim = pyganim.PygAnimation(frames)
dinoAnim.play() # there is also a pause() and stop() method

mainClock = pygame.time.Clock()
BGCOLOR = (100, 50, 50)
while True:
    windowSurface.fill(BGCOLOR)
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

    dinoAnim.blit(windowSurface, (100, 50))

    pygame.display.update()
    mainClock.tick(30) # Feel free to experiment with any FPS setting.