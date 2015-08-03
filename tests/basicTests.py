import unittest
import sys
import os
import hashlib
import time
import pygame

sys.path.insert(0, os.path.abspath('..'))
import pyganim


runningOnPython2 = sys.version_info[0] == 2
NUM_BOLT_IMAGES = 10
BOLT_DURATIONS = 100
BOLT_WIDTH, BOLT_HEIGHT = pygame.image.load('bolt1.png').get_size()


def getTestAnimObj():
    # Returns a standard PygAnimation object.
    frames = [('bolt%s.png' % (i), BOLT_DURATIONS) for i in range(1, NUM_BOLT_IMAGES + 1)]
    return pyganim.PygAnimation(frames)


def compareSurfaces(surf1, surf2):
    if surf1.get_size() != surf2.get_size():
        return 'Surfaces have different sizes: %s and %s' % (surf1.get_size(), surf2.get_size())

    px1 = pygame.PixelArray(surf1)
    px2 = pygame.PixelArray(surf2)

    # note: the compare() method seems to be broken in Pygame for Windows Python 3.3
    # using this comparison instead:
    for x in range(surf1.get_width()):
        for y in range(surf1.get_height()):
            color1 = surf1.unmap_rgb(px1[x][y])
            color2 = surf2.unmap_rgb(px1[x][y])
            if color1 != color2:
                del px1
                del px2
                return 'Pixel at %s, %s is different: %s and %s' % (x, y, color1, color2)
    return None # on success, return None


class TestTestImages(unittest.TestCase):
    # This is here just to make sure the test images of the lightning bolts haven't changed.
    def test_images(self):
        # test bolt images
        boltSha1Sums = {1: 'd556336b479921148ef5199cf0fa8258501603f3',
                        2: '970ae0745ebef5e57c8a04acb7cb98f1478777ca',
                        3: '377e34ced2a7594dd591d08e47eb7b87ce3d4e0a',
                        4: 'fb4796db338f3e2b88b7821a3acef2b5010f126a',
                        5: 'ddc42acb949c2fd8e8d80d3dd9db9df5de9d29c8',
                        6: '004995ee0a2f8bb4c7a36d566a351a1e066a61c9',
                        7: '11af4a9c01f5619566a3f810a0aeba9462bf0d6f',
                        8: '4f39899edefcea6a0196337fbb3b003064ecf8ba',
                        9: '1f2acefa7a5c106565274646f0234907a689baf7',
                        10: 'e9a41735e799ebb7caafc32ac7e8310dc4bd9742'}

        for i in range(1, NUM_BOLT_IMAGES + 1):
            boltFile = open('bolt%s.png' % i, 'rb')
            s = hashlib.sha1(boltFile.read())
            boltFile.close()
            self.assertEqual(s.hexdigest(), boltSha1Sums[i])

        # test animated gif
        gifFile = open('banana.gif', 'rb')
        s = hashlib.sha1(gifFile.read())
        gifFile.close()
        self.assertEqual(s.hexdigest(), '65137061474887dfa0f183f2bc118a3e52fc353e')

        # test sprite sheet
        spritesheetFile = open('smokeSpritesheet.png', 'rb')
        s = hashlib.sha1(spritesheetFile.read())
        spritesheetFile.close()
        self.assertEqual(s.hexdigest(), '566cdeb39ffa26e1fb4e0486a16e22de7ac9f6c4')

        # TODO - add code that checks the individual smoke spritesheet images



class TestGeneral(unittest.TestCase):
    def test_constructor(self):
        # Test ctor with filenames
        frames = [('bolt%s.png' % (i), BOLT_DURATIONS) for i in range(1, 11)]
        animObj = pyganim.PygAnimation(frames)
        self.assertEqual(animObj._state, pyganim.STOPPED)
        self.assertEqual(animObj._loop, True)
        self.assertEqual(animObj._rate, 1.0)
        self.assertEqual(animObj._visibility, True)
        self.assertEqual(len(animObj._images), NUM_BOLT_IMAGES)
        self.assertEqual(len(animObj._durations), NUM_BOLT_IMAGES)

        # Test ctor with pygame.Surface objects
        frames = [(pygame.image.load('bolt%s.png' % (i)), BOLT_DURATIONS) for i in range(1, 11)]
        animObj = pyganim.PygAnimation(frames)
        self.assertEqual(animObj._state, pyganim.STOPPED)
        self.assertEqual(animObj._loop, True)
        self.assertEqual(animObj._rate, 1.0)
        self.assertEqual(animObj._visibility, True)
        self.assertEqual(len(animObj._images), NUM_BOLT_IMAGES)
        self.assertEqual(len(animObj._durations), NUM_BOLT_IMAGES)


    def test_reverse(self):
        animObj = getTestAnimObj()

        imageIdsForward = [id(animObj._images[i]) for i in range(NUM_BOLT_IMAGES)]
        imageIdsReverse = imageIdsForward[:]
        imageIdsReverse.reverse()


        for i in range(NUM_BOLT_IMAGES):
            self.assertEqual(id(animObj._images[i]), imageIdsForward[i])
        animObj.reverse() # reverse
        for i in range(NUM_BOLT_IMAGES):
            self.assertEqual(id(animObj._images[i]), imageIdsReverse[i])
        animObj.reverse() # reverse again to make sure they're in the original order
        for i in range(NUM_BOLT_IMAGES):
            self.assertEqual(id(animObj._images[i]), imageIdsForward[i])


    def test_getCopy(self):
        animObj = getTestAnimObj()

        animCopy = animObj.getCopy()

        self.assertEqual(animObj._state, animCopy._state)
        self.assertEqual(animObj._loop, animCopy._loop)
        self.assertEqual(animObj._rate, animCopy._rate)
        self.assertEqual(animObj._visibility, animCopy._visibility)
        self.assertEqual(animObj._durations, animCopy._durations)

        for i in range(NUM_BOLT_IMAGES):
            self.assertEqual(id(animObj._images[i]), id(animCopy._images[i]))
            self.assertEqual(animObj._durations[i], animCopy._durations[i])


    def test_getCopies(self):
        animObj = getTestAnimObj()

        animCopies = animObj.getCopies(5)

        for c in range(5):
            self.assertEqual(animObj._state, animCopies[c]._state)
            self.assertEqual(animObj._loop, animCopies[c]._loop)
            self.assertEqual(animObj._rate, animCopies[c]._rate)
            self.assertEqual(animObj._visibility, animCopies[c]._visibility)
            self.assertEqual(animObj._durations, animCopies[c]._durations)

            for i in range(NUM_BOLT_IMAGES):
                self.assertEqual(id(animObj._images[i]), id(animCopies[c]._images[i]))
                self.assertEqual(animObj._durations[i], animCopies[c]._durations[i])


    def test_blit(self):
        animObj = getTestAnimObj()
        animObj.pause() # pause the animation on the first frame (bolt1.png)

        surf = pygame.Surface((BOLT_WIDTH, BOLT_HEIGHT))

        # Test blitting to destination (0, 0)
        for dest in ((0, 0), (37, 37)):
            for i in range(1, NUM_BOLT_IMAGES + 1):
                surf.fill(pygame.Color('black'))
                animObj.blit(surf, dest)

                image = pygame.image.load('bolt%s.png' % i)
                orig = pygame.Surface((BOLT_WIDTH, BOLT_HEIGHT))
                orig.fill(pygame.Color('black'))
                orig.blit(image, dest)

                self.assertEqual((dest, None), (dest, compareSurfaces(surf, orig)))

                animObj.nextFrame()


    def test_blitFrameNum(self):
        animObj = getTestAnimObj()

        surf = pygame.Surface((BOLT_WIDTH, BOLT_HEIGHT))

        # Test blitting to destination (0, 0)
        for dest in ((0, 0), (37, 37)):
            for frame in range(1, NUM_BOLT_IMAGES + 1):
                surf.fill(pygame.Color('black'))
                animObj.blitFrameNum(frame, surf, dest)

                image = pygame.image.load('bolt%s.png' % frame)
                orig = pygame.Surface((BOLT_WIDTH, BOLT_HEIGHT))
                orig.fill(pygame.Color('black'))
                orig.blit(image, dest)

                self.assertEqual((dest, None), (dest, compareSurfaces(surf, orig)))


    def test_blitFrameAtTime(self):
        animObj = getTestAnimObj()

        surf = pygame.Surface((BOLT_WIDTH, BOLT_HEIGHT))

        # Test blitting to destination (0, 0)
        for dest in ((0, 0), (37, 37)):
            timeSetting = BOLT_DURATIONS / 2.0
            for i in range(1, NUM_BOLT_IMAGES + 1):
                surf.fill(pygame.Color('black'))
                animObj.blitFrameAtTime(timeSetting, surf, dest)
                timeSetting += BOLT_DURATIONS

                image = pygame.image.load('bolt%s.png' % i)
                orig = pygame.Surface((BOLT_WIDTH, BOLT_HEIGHT))
                orig.fill(pygame.Color('black'))
                orig.blit(image, dest)

                self.assertEqual((dest, None), (dest, compareSurfaces(surf, orig)))


    def test_isFinished(self):
        # test on animation that doesn't loop
        animObj = getTestAnimObj()
        animObj.loop = False
        animObj.play()
        self.assertEqual(animObj.isFinished(), False)
        time.sleep((BOLT_DURATIONS * (NUM_BOLT_IMAGES + 1)) / 1000.0) # should be enough time to finish a single run through of the animation
        self.assertEqual(animObj.isFinished(), True)

        # test on animation that loops
        animObj = getTestAnimObj()
        animObj.loop = True
        animObj.play()
        self.assertEqual(animObj.isFinished(), False)
        time.sleep((BOLT_DURATIONS * (NUM_BOLT_IMAGES + 1)) / 1000.0) # should be enough time to finish a single run through of the animation
        self.assertEqual(animObj.isFinished(), False) # looping animations are never finished


    def test_getFrame(self):
        animObj = getTestAnimObj()

        for i in range(NUM_BOLT_IMAGES):
            frame = animObj.getFrame(i)
            image = pygame.image.load('bolt%s.png' % (i + 1))
            self.assertEqual(None, compareSurfaces(frame, image))


    def test_getCurrentFrame(self):
        animObj = getTestAnimObj()

        for i in range(NUM_BOLT_IMAGES):
            frame = animObj.getCurrentFrame()
            image = pygame.image.load('bolt%s.png' % (i + 1))
            self.assertEqual(None, compareSurfaces(frame, image))

            animObj.nextFrame()


    def test_framesAreSameSize(self):
        # the standard test animation object has same-sized frames
        self.assertTrue(getTestAnimObj().framesAreSameSize())

        diffSized = pyganim.PygAnimation([(pygame.Surface((100, 100)), BOLT_DURATIONS), (pygame.Surface((100, 200)), BOLT_DURATIONS)])
        self.assertFalse(diffSized.framesAreSameSize())


    def test_nextFrame_prevFrame(self):
        animObj = getTestAnimObj()

        expectedFrameNum = 0
        self.assertEqual(expectedFrameNum, animObj.currentFrameNum)
        # test nextFrame()
        for i in range(NUM_BOLT_IMAGES * 2):
            animObj.nextFrame()
            expectedFrameNum = (expectedFrameNum + 1) % len(animObj._images)
            self.assertEqual(expectedFrameNum, animObj.currentFrameNum)

        # test prevFrame()
        for i in range(NUM_BOLT_IMAGES * 2):
            animObj.prevFrame()
            expectedFrameNum = (expectedFrameNum - 1) % len(animObj._images)
            self.assertEqual(expectedFrameNum, animObj.currentFrameNum)

        # test nextFrame() with jump argument
        for i in range(NUM_BOLT_IMAGES * 2):
            animObj.nextFrame(3)
            expectedFrameNum = (expectedFrameNum + 3) % len(animObj._images)
            self.assertEqual(expectedFrameNum, animObj.currentFrameNum)

        # test prevFrame() with jump argument
        for i in range(NUM_BOLT_IMAGES * 2):
            animObj.prevFrame(3)
            expectedFrameNum = (expectedFrameNum - 3) % len(animObj._images)
            self.assertEqual(expectedFrameNum, animObj.currentFrameNum)

    def test_play_pause(self):
        # with looping
        animObj = getTestAnimObj()
        self.assertTrue(animObj.loop)
        for i in range(1, NUM_BOLT_IMAGES + 3): # go a bit past the last frame
            animObj.play()
            time.sleep(BOLT_DURATIONS / 1000.0)
            animObj.pause()
            self.assertEqual(i % NUM_BOLT_IMAGES, animObj.currentFrameNum)

        # without looping
        animObj = getTestAnimObj()
        animObj.loop = False
        for i in range(1, NUM_BOLT_IMAGES + 3): # go a bit past the last frame
            animObj.play()
            time.sleep(BOLT_DURATIONS / 1000.0)
            animObj.pause()
            if i >= NUM_BOLT_IMAGES:
                self.assertEqual(NUM_BOLT_IMAGES - 1, animObj.currentFrameNum) # with looping off, the currentFrameNum does not advance after the last frame
            else:
                self.assertEqual(i, animObj.currentFrameNum)

    def test_togglePause(self):
        # with looping
        animObj = getTestAnimObj()
        self.assertTrue(animObj.loop)
        for i in range(1, NUM_BOLT_IMAGES + 3): # go a bit past the last frame
            animObj.togglePause()
            time.sleep(BOLT_DURATIONS / 1000.0)
            animObj.togglePause()
            self.assertEqual(i % NUM_BOLT_IMAGES, animObj.currentFrameNum)

        # without looping
        animObj = getTestAnimObj()
        animObj.loop = False
        for i in range(1, NUM_BOLT_IMAGES + 3): # go a bit past the last frame
            animObj.togglePause()
            time.sleep(BOLT_DURATIONS / 1000.0)
            animObj.togglePause()
            if i >= NUM_BOLT_IMAGES:
                self.assertEqual(NUM_BOLT_IMAGES - 1, animObj.currentFrameNum) # with looping off, the currentFrameNum does not advance after the last frame
            else:
                self.assertEqual(i, animObj.currentFrameNum)


    def test_getMaxSize(self):
        animObj = getTestAnimObj()
        self.assertEqual((BOLT_WIDTH, BOLT_HEIGHT), animObj.getMaxSize())

        mixedSizesObj = pyganim.PygAnimation([(pygame.Surface((100, 10)), 1), (pygame.Surface((10, 200)), 1000)])
        self.assertEqual((100, 200), mixedSizesObj.getMaxSize())


    def test_getRect(self):
        animObj = getTestAnimObj()
        r = animObj.getRect()
        self.assertEqual((BOLT_WIDTH, BOLT_HEIGHT), r.size)

        mixedSizesObj = pyganim.PygAnimation([(pygame.Surface((100, 10)), 1), (pygame.Surface((10, 200)), 1000)])
        r = mixedSizesObj.getRect()
        self.assertEqual((100, 200), r.size)


    def test_rewind(self):
        animObj = getTestAnimObj()

        animObj.play()
        time.sleep(0.2)
        animObj.pause()
        animObj.rewind()
        self.assertEqual(animObj.elapsed, 0)

        animObj.play()
        time.sleep(0.2)
        animObj.pause()
        origElapsed = animObj.elapsed
        animObj.rewind(100)
        self.assertEqual(animObj.elapsed, origElapsed - 100)


    def test_fastForward(self):
        animObj = getTestAnimObj()
        self.assertEqual(animObj.state, pyganim.STOPPED)
        animObj.fastForward(375)
        self.assertEqual(animObj.elapsed, 375)
        self.assertEqual(animObj.state, pyganim.PAUSED)

        animObj = getTestAnimObj()
        animObj.play()
        time.sleep(0.2)
        animObj.pause()
        origElapsed = animObj.elapsed
        animObj.rewind(100)
        self.assertEqual(animObj.elapsed, origElapsed - 100)

    def test_loadingAnimatedGif(self):
        animObj = pyganim.PygAnimation('banana.gif') # IT'S PEANUT BUTTER JELLY TIME
        self.assertEqual(len(animObj._images), 8)
        for i in range(8):
            self.assertEqual(animObj._durations[i], 100)


class TestSpritesheet(unittest.TestCase):
    def test_loading(self):
        """
        NUM_SPRITES = 10
        SMOKE_WIDTH = 96
        SMOKE_HEIGHT = 94
        smokeImages = [pygame.image.load('smoke%s.png' % i) for i in range(NUM_SPRITES)]


        # basic loading test using width/height arguments
        sheet = pyganim.getImagesFromSpriteSheet('smokeSpritesheet.png', width=SMOKE_WIDTH, height=SMOKE_HEIGHT)
        animObj = pyganim.PygAnimation(sheet.frames)

        self.assertEqual(len(animObj._images), NUM_SPRITES)
        self.assertTrue(animObj.framesAreSameSize())
        self.assertEqual(animObj._images[0].get_width(), SMOKE_WIDTH)
        self.assertEqual(animObj._images[0].get_height(), SMOKE_HEIGHT)

        for i in range(NUM_SPRITES):
            self.assertEqual((i, None), (i, compareSurfaces(animObj._images[i], smokeImages[i])))

        # basic loading test using width/height arguments with default height
        sheet = pyganim.getImagesFromSpriteSheet('smokeSpritesheet.png', width=SMOKE_WIDTH)
        animObj = pyganim.PygAnimation(sheet.frames)

        self.assertEqual(len(animObj._images), NUM_SPRITES)
        self.assertTrue(animObj.framesAreSameSize())
        self.assertEqual(animObj._images[0].get_width(), SMOKE_WIDTH)
        self.assertEqual(animObj._images[0].get_height(), SMOKE_HEIGHT)

        for i in range(NUM_SPRITES):
            self.assertEqual((i, None), (i, compareSurfaces(animObj._images[i], smokeImages[i])))

        # basic loading test using row/col arguments
        sheet = pyganim.getImagesFromSpriteSheet('smokeSpritesheet.png', rows=1, cols=NUM_SPRITES)
        animObj = pyganim.PygAnimation(sheet.frames)

        self.assertEqual(len(animObj._images), NUM_SPRITES)
        self.assertTrue(animObj.framesAreSameSize())
        self.assertEqual(animObj._images[0].get_width(), SMOKE_WIDTH)
        self.assertEqual(animObj._images[0].get_height(), SMOKE_HEIGHT)

        for i in range(NUM_SPRITES):
            self.assertEqual((i, None), (i, compareSurfaces(animObj._images[i], smokeImages[i])))

        # basic loading test using row/col arguments with default rows
        sheet = pyganim.getImagesFromSpriteSheet('smokeSpritesheet.png', cols=NUM_SPRITES)
        animObj = pyganim.PygAnimation(sheet.frames)

        self.assertEqual(len(animObj._images), NUM_SPRITES)
        self.assertTrue(animObj.framesAreSameSize())
        self.assertEqual(animObj._images[0].get_width(), SMOKE_WIDTH)
        self.assertEqual(animObj._images[0].get_height(), SMOKE_HEIGHT)

        for i in range(NUM_SPRITES):
            self.assertEqual((i, None), (i, compareSurfaces(animObj._images[i], smokeImages[i])))

        # loading using rects arguments
        rects = []
        index = 0
        for x in range(0, SMOKE_WIDTH * NUM_SPRITES, SMOKE_WIDTH):
            rects.append((x, 0, SMOKE_WIDTH, SMOKE_HEIGHT, index))
            index += 1
        sheet = pyganim.getImagesFromSpriteSheet('smokeSpritesheet.png', rects=rects)
        animObj = pyganim.PygAnimation(sheet.frames)

        self.assertEqual(len(animObj._images), NUM_SPRITES)
        self.assertTrue(animObj.framesAreSameSize())
        self.assertEqual(animObj._images[0].get_width(), SMOKE_WIDTH)
        self.assertEqual(animObj._images[0].get_height(), SMOKE_HEIGHT)

        for i in range(NUM_SPRITES):
            self.assertEqual((i, None), (i, compareSurfaces(animObj._images[i], smokeImages[i])))

        # loading using rects arguments with indexes in an arbitrary order
        rects = []
        indexes = [9, 3, 6, 0, 1, 2, 4, 7, 5, 8]
        i = 0
        for x in range(0, SMOKE_WIDTH * NUM_SPRITES, SMOKE_WIDTH):
            rects.append((x, 0, SMOKE_WIDTH, SMOKE_HEIGHT, indexes[i]))
            i += 1
        sheet = pyganim.getImagesFromSpriteSheet('smokeSpritesheet.png', rects=rects)
        animObj = pyganim.PygAnimation(sheet.frames)

        self.assertEqual(len(animObj._images), NUM_SPRITES)
        self.assertTrue(animObj.framesAreSameSize())
        self.assertEqual(animObj._images[0].get_width(), SMOKE_WIDTH)
        self.assertEqual(animObj._images[0].get_height(), SMOKE_HEIGHT)

        for i in range(NUM_SPRITES):
            self.assertEqual((i, None), (i, compareSurfaces(animObj._images[i], smokeImages[indexes[i]])))
        """



class MiscTests(unittest.TestCase):
    # This is here just to make sure the test images of the lightning bolts haven't changed.
    def test_getBoundedValue(self):
        self.assertEqual(pyganim.getBoundedValue(0, 5, 10), 5)
        self.assertEqual(pyganim.getBoundedValue(0, 0, 10), 0)
        self.assertEqual(pyganim.getBoundedValue(0, -5, 10), 0)
        self.assertEqual(pyganim.getBoundedValue(0, 10, 10), 10)
        self.assertEqual(pyganim.getBoundedValue(0, 15, 10), 10)

        self.assertEqual(pyganim.getBoundedValue(0, -5, -10), -5)
        self.assertEqual(pyganim.getBoundedValue(0, 0, -10), 0)
        self.assertEqual(pyganim.getBoundedValue(0, 5, -10), 0)
        self.assertEqual(pyganim.getBoundedValue(0, -10, -10), -10)
        self.assertEqual(pyganim.getBoundedValue(0, -15, -10), -10)

        self.assertEqual(pyganim.getBoundedValue(-10, -5, 0), -5)
        self.assertEqual(pyganim.getBoundedValue(-10, 0, 0), 0)
        self.assertEqual(pyganim.getBoundedValue(-10, 5, 0), 0)
        self.assertEqual(pyganim.getBoundedValue(-10, -10, 0), -10)
        self.assertEqual(pyganim.getBoundedValue(-10, -15, 0), -10)

    def test_findStartTime(self):
        st = [0, 1000, 2000, 4000, 8000, 16000]
        self.assertEqual(pyganim.findStartTime(st, 0), 0)
        self.assertEqual(pyganim.findStartTime(st, 999), 0)
        self.assertEqual(pyganim.findStartTime(st, 1000), 1)
        self.assertEqual(pyganim.findStartTime(st, 1001), 1)
        self.assertEqual(pyganim.findStartTime(st, 1999), 1)
        self.assertEqual(pyganim.findStartTime(st, 2000), 2)
        self.assertEqual(pyganim.findStartTime(st, 2001), 2)
        self.assertEqual(pyganim.findStartTime(st, 3999), 2)
        self.assertEqual(pyganim.findStartTime(st, 4000), 3)
        self.assertEqual(pyganim.findStartTime(st, 9999999), 4)


if __name__ == '__main__':
    unittest.main()