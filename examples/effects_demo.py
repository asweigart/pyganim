# test2_pyganim.py - A pyganim test program.
#
# This program shows off a lot more of Pyganim features, and offers some interactivity.
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
windowSurface = pygame.display.set_mode((640, 480), 0, 32)
pygame.display.set_caption('Pyganim Effects Demo')

# create the animation objects
boltAnim0 = pyganim.PygAnimation([('testimages/bolt_strike_0001.png', 100),
                                  ('testimages/bolt_strike_0002.png', 100),
                                  ('testimages/bolt_strike_0003.png', 100),
                                  ('testimages/bolt_strike_0004.png', 100),
                                  ('testimages/bolt_strike_0005.png', 100),
                                  ('testimages/bolt_strike_0006.png', 100),
                                  ('testimages/bolt_strike_0007.png', 100),
                                  ('testimages/bolt_strike_0008.png', 100),
                                  ('testimages/bolt_strike_0009.png', 100),
                                  ('testimages/bolt_strike_0010.png', 100)])

# create some copies of the bolt animation
boltAnim1, boltAnim2, boltAnim3, boltAnim4 = boltAnim0.getCopies(4)
boltAnim3.rate = 0.5
boltAnim4.rate = 2.0
bolts = [boltAnim0, boltAnim1, boltAnim2, boltAnim3, boltAnim4]

# supply a "start time" argument to play() so that the bolt animations are
# all in sync with each other.
rightNow = time.time()
for i in range(len(bolts)):
    if i == 2:
        continue # we're not going to call play() on boltAnim2
    bolts[i].play(rightNow) # make sure they all start in sync


# create the fire animation
fireAnim = pyganim.PygAnimation([('testimages/flame_a_0001.png', 100),
                                 ('testimages/flame_a_0002.png', 100),
                                 ('testimages/flame_a_0003.png', 100),
                                 ('testimages/flame_a_0004.png', 100),
                                 ('testimages/flame_a_0005.png', 100),
                                 ('testimages/flame_a_0006.png', 100)])
fireAnim2 = fireAnim.getCopy()
fireAnim3 = fireAnim.getCopy()
spinningFireAnim = fireAnim.getCopy()

# do some transformation on the other two fire animation objects
fireAnim2.smoothscale((200, 200))
fireAnim3.rotate(50)
fireAnim3.smoothscale((256, 360))
fireAnim.rate = 1.2 # make the smaller fire slightly faster

# start playing the fire animations
fireAnim.play()
fireAnim2.play()
fireAnim3.play()
spinningFireAnim.play()

# You can also use pygame.Surface objects in the constructor instead of filename strings.
smokeSurf1 = pygame.image.load('testimages/smoke_puff_0001.png')
smokeSurf2 = pygame.image.load('testimages/smoke_puff_0002.png')
smokeSurf3 = pygame.image.load('testimages/smoke_puff_0003.png')
smokeSurf4 = pygame.image.load('testimages/smoke_puff_0004.png')
smokeAnim = pyganim.PygAnimation([(smokeSurf1, 100),
                                  (smokeSurf2, 100),
                                  (smokeSurf3, 100),
                                  (smokeSurf4, 100),
                                  ('testimages/smoke_puff_0005.png', 100),
                                  ('testimages/smoke_puff_0006.png', 100),
                                  ('testimages/smoke_puff_0007.png', 100),
                                  ('testimages/smoke_puff_0008.png', 300),
                                  ('testimages/smoke_puff_0009.png', 300),
                                  ('testimages/smoke_puff_0010.png', 300)], loop=False)
smokeAnim.play() # start playing the smoke animation

# creating an animation object from an image that doesn't have transparent
# pixels so that the alpha values can be changed.
alAnim = pyganim.PygAnimation([('testimages/alsweigart1.jpg', 500),
                               ('testimages/alsweigart2.jpg', 500)])
alAnim.set_alpha(50)
alAnim.play()


BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
WHITE = (255, 255, 255)
BGCOLOR = (100, 50, 50)
instructionSurf = BASICFONT.render('P to toggle Play/Pause, S to stop, R to reverse, LEFT/RIGHT to rewind/ff.', True, WHITE)
instructionRect = instructionSurf.get_rect()
instructionRect.topleft = (10, 128)
instructionSurf2 = BASICFONT.render('O to replay smoke. I to toggle fire visibility. Esc to quit.', True, WHITE)
instructionRect2 = instructionSurf2.get_rect()
instructionRect2.topleft = (10, 148)
instructionSurf3 = BASICFONT.render('Note the 3rd bolt doesn\'t play because play() wasn\'t called on it.', True, WHITE)
instructionRect3 = instructionSurf2.get_rect()
instructionRect3.topleft = (10, 168)

mainClock = pygame.time.Clock()
spinAmt = 0

while True:
    windowSurface.fill(BGCOLOR)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_p:
                boltAnim0.togglePause()
            if event.key == K_s:
                boltAnim0.stop()
            if event.key == K_LEFT:
                boltAnim0.prevFrame()
            if event.key == K_RIGHT:
                boltAnim0.nextFrame()
            if event.key == K_r:
                boltAnim0.reverse()
            if event.key == K_o:
                smokeAnim.play()
            if event.key == K_i:
                fireAnim.visibility = not fireAnim.visibility
                fireAnim2.visibility = not fireAnim2.visibility
                fireAnim3.visibility = not fireAnim3.visibility

    # draw the animations to the screen
    for i in range(len(bolts)):
        bolts[i].blit(windowSurface, ((i*133), 0))
    fireAnim3.blit(windowSurface, (30, 130))
    fireAnim2.blit(windowSurface, (116, 226))
    fireAnim.blit(windowSurface, (178, 278))
    smokeAnim.blit(windowSurface, (350, 250))

    # handle the spinning fire
    spinAmt += 1
    spinningFireAnim.clearTransforms()
    spinningFireAnim.rotate(spinAmt)
    curSpinSurf = spinningFireAnim.getCurrentFrame() # gets the current
    w, h = curSpinSurf.get_size()

    # technically, in the time span between the getCurrentFrame() call and
    # the following blit() call, enough time could have passed where it
    # has the width and height for the wrong frame. It's unlikely though.
    # But if you want to account for this, just use the blitFrameAtTime()
    # or blitFrameNum() methods instead of blit().
    spinningFireAnim.blit(windowSurface, (550 - int(w/2), 350 - int(h/2)))

    # draw the semitransparent "picture of Al" animation on top of the spinning fire
    alAnim.blit(windowSurface, (512, 352))

    # draw the instructional text
    windowSurface.blit(instructionSurf, instructionRect)
    windowSurface.blit(instructionSurf2, instructionRect2)
    windowSurface.blit(instructionSurf3, instructionRect3)

    pygame.display.update()
    mainClock.tick(30) # Feel free to experiment with any FPS setting.