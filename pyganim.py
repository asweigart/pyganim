"""
pyganim.py
A sprite animation module for Pygame.

By Al Sweigart al@inventwithpython.com
http://inventwithpython.com/pyganim
Released under a "Simplified BSD" license

There's a tutorial (and sample code) on how to use this library at http://inventwithpython.com/pyganim
NOTE: This module requires Pygame to be installed to use. Download it from http://pygame.org

This should be compatible with both Python 2 and Python 3. Please email any
bug reports to Al at al@inventwithpython.com


I_don't_like_the_naming_conventions_of_PEP_8
JustDealWithIt

Version 1
"""


# TODO: Feature idea: if the same image file is specified, re-use the Surface object. (Make this optional though.)

import pygame, time

# setting up constants
PLAYING = 'playing'
PAUSED = 'paused'
STOPPED = 'stopped'

# These values are used in the anchor() method.
NORTHWEST = 'northwest'
NORTH = 'north'
NORTHEAST = 'northeast'
WEST = 'west'
CENTER = 'center'
EAST = 'east'
SOUTHWEST = 'southwest'
SOUTH = 'south'
SOUTHEAST = 'southeast'


class PygAnimation(object):
    def __init__(self, frames, loop=True):
        """
        Constructor function for the animation object. Starts off in the STOPPED state.
        
        @param frames
            A list of tuples for each frame of animation, in one of the following format:
              (image_of_frame<pygame.Surface>, duration_in_seconds<int>)
              (filename_of_image<str>, duration_in_seconds<int>)
            Note that the images and duration cannot be changed. A new PygAnimation object
            will have to be created.
        @param loop Tells the animation object to keep playing in a loop.
        """

        # _images stores the pygame.Surface objects of each frame
        self.__images = []
        # _durations stores the durations (in seconds) of each frame.
        # e.g. [1, 1, 2.5] means the first and second frames last one second,
        # and the third frame lasts for two and half seconds.
        self.__durations = []
        # _startTimes shows when each frame begins. len(self.__startTimes) will
        # always be one more than len(self.__images), because the last number
        # will be when the last frame ends, rather than when it starts.
        # The values are in seconds.
        # So self.__startTimes[-1] tells you the length of the entire animation.
        # e.g. if _durations is [1, 1, 2.5], then _startTimes will be [0, 1, 2, 4.5]
        self.__startTimes = None

        # if the sprites are transformed, the originals are kept in _images
        # and the transformed sprites are kept in _transformedImages.
        self.__transformedImages = []

        self.__state = STOPPED # The state is always either PLAYING, PAUSED, or STOPPED
        self.__loop = loop # If True, the animation will keep looping. If False, the animation stops after playing once.
        self.__rate = 1.0 # 2.0 means play the animation twice as fast, 0.5 means twice as slow
        self.__visibility = True # If False, then nothing is drawn when the blit() methods are called

        self.__playingStartTime = 0 # the time that the play() function was last called.
        self.__pausedStartTime = 0 # the time that the pause() function was last called.

        if frames != '_copy': # ('_copy' is passed for frames by the getCopies() method)
            self.numFrames = len(frames)
            assert self.numFrames > 0, 'Must contain at least one frame.'
            for i in range(self.numFrames):
                # load each frame of animation into _images
                frame = frames[i]
                assert type(frame) in (list, tuple) and len(frame) == 2, 'Frame %s has incorrect format.' % (i)
                assert type(frame[0]) in (str, pygame.Surface), 'Frame %s image must be a string filename or a pygame.Surface' % (i)
                assert frame[1] > 0, 'Frame %s duration must be greater than zero.' % (i)
                if type(frame[0]) == str:
                    frame = (pygame.image.load(frame[0]), frame[1])
                self.__images.append(frame[0])
                self.__durations.append(frame[1])
            self.__startTimes = self.__getStartTimes()


    def __getStartTimes(self):
        """Internal method to get the start times based off of the _durations list.
        Don't call this method."""
        startTimes = [0]
        for i in range(self.numFrames):
            startTimes.append(startTimes[-1] + self.__durations[i])
        return startTimes


    def reverse(self):
        """
        Reverses the order of the animations.
        """

        elapsed = self.elapsed
        elapsed = self.__startTimes[-1] - elapsed
        self.__images.reverse()
        self.__transformedImages.reverse()
        self.__durations.reverse()


    def getCopy(self):
        """
        Returns a copy of this PygAnimation object, but one that refers to the
        Surface objects of the original so it efficiently uses memory.
        
        NOTE: Messing around with the original Surface objects will affect all
        the copies. If you want to modify the Surface objects, then just make
        copies using constructor function instead.
        """
        return self.getCopies(1)[0]


    def getCopies(self, numCopies=1):
        """
        Returns a list of copies of this PygAnimation object, but one that refers to the
        Surface objects of the original so it efficiently uses memory.
        
        NOTE: Messing around with the original Surface objects will affect all
        the copies. If you want to modify the Surface objects, then just make
        copies using constructor function instead.
        """
        # TODO Chad this is not very clean
        retval = []
        for i in range(numCopies):
            newAnim = PygAnimation('_copy', loop=self.__loop)
            newAnim.__images = self.__images[:]
            newAnim.__transformedImages = self.__transformedImages[:]
            newAnim.__durations = self.__durations[:]
            newAnim.__startTimes = self.__startTimes[:]
            newAnim.numFrames = self.numFrames
            retval.append(newAnim)
        return retval


    def blit(self, destSurface, dest):
        """
        Draws the appropriate frame of the animation to the destination Surface
        at the specified position.
        
        NOTE: If the visibility attribute is False, then nothing will be drawn.
        
        @param destSurface
            The Surface object to draw the frame
        @param dest
            The position to draw the frame. This is passed to Pygame's Surface's
            blit() function, so it can be either a (top, left) tuple or a Rect
            object.
        """
        if self.isFinished():
            self.__state = STOPPED
        if not self.__visibility or self.__state == STOPPED:
            return
        frameNum = findStartTime(self.__startTimes, self.elapsed)
        destSurface.blit(self.getFrame(frameNum), dest)


    def getFrame(self, frameNum):
        """
        Returns the pygame.Surface object of the frameNum-th frame in this
        animation object. If there is a transformed version of the frame,
        it will return that one.
        """
        if self.__transformedImages == []:
            return self.__images[frameNum]
        else:
            return self.__transformedImages[frameNum]


    def getCurrentFrame(self):
        """
        Returns the pygame.Surface object of the frame that would be drawn
        if the blit() method were called right now. If there is a transformed
        version of the frame, it will return that one.
        """
        return self.getFrame(self.currentFrameNum)


    def clearTransforms(self):
        """
        Deletes all the transformed frames so that the animation object
        displays the original Surfaces/images as they were before
        transformation functions were called on them.
        
        This is handy to do for multiple transformation, where calling
        the rotation or scaling functions multiple times results in
        degraded/noisy images.
        """
        self.__transformedImages = []


    def blitFrameNum(self, frameNum, destSurface, dest):
        """
        Draws the specified frame of the animation object. This ignores the
        current playing state.
        
        NOTE: If the visibility attribute is False, then nothing will be drawn.
        
        @param frameNum
            The frame to draw (the first frame is 0, not 1)
        @param destSurface
            The Surface object to draw the frame
        @param dest
            The position to draw the frame. This is passed to Pygame's Surface's
            blit() function, so it can be either a (top, left) tuple or a Rect
            object.
        """
        if self.isFinished():
            self.__state = STOPPED
        if not self.__visibility or self.__state == STOPPED:
            return
        destSurface.blit(self.getFrame(frameNum), dest)


    def blitFrameAtTime(self, elapsed, destSurface, dest):
        """
        Draws the frame the is "elapsed" number of seconds into the animation,
        rather than the time the animation actually started playing.
        
        NOTE: If the visibility attribute is False, then nothing will be drawn.
        
        @param elapsed
            The amount of time into an animation to use when determining which
            frame to draw. blitFrameAtTime() uses this parameter rather than
            the actual time that the animation started playing. (In seconds)
        @param destSurface
            The Surface object to draw the frame
        @param dest
            The position to draw the frame. This is passed to Pygame's Surface's
            blit() function, so it can be either a (top, left) tuple or a Rect
            object.
        """
        elapsed = int(elapsed * self.__rate)
        if self.isFinished():
            self.__state = STOPPED
        if not self.__visibility or self.__state == STOPPED:
            return
        frameNum = findStartTime(self.__startTimes, elapsed)
        destSurface.blit(self.getFrame(frameNum), dest)


    def isFinished(self):
        """
        Returns True if this animation doesn't loop and has finished playing
        all the frames it has.
        """
        return not self.__loop and self.elapsed >= self.__startTimes[-1]


    def play(self, startTime=None):
        """
        Start playing the animation.
        """

        if startTime is None:
            startTime = time.time()

        if self.__state == PLAYING:
            if self.isFinished():
                # if the animation doesn't loop and has already finished, then
                # calling play() causes it to replay from the beginning.
                self.__playingStartTime = startTime
        elif self.__state == STOPPED:
            # if animation was stopped, start playing from the beginning
            self.__playingStartTime = startTime
        elif self.__state == PAUSED:
            # if animation was paused, start playing from where it was paused
            self.__playingStartTime = startTime - (self.__pausedStartTime - self.__playingStartTime)
        self.__state = PLAYING


    def pause(self, startTime=None):
        """
        Stop having the animation progress, and keep it at the current frame.
        """

        if startTime is None:
            startTime = time.time()

        if self.__state == PAUSED:
            return # do nothing
        elif self.__state == PLAYING:
            self.__pausedStartTime = startTime
        elif self.__state == STOPPED:
            rightNow = time.time()
            self.__playingStartTime = rightNow
            self.__pausedStartTime = rightNow
        self.__state = PAUSED


    def stop(self):
        """
        Reset the animation to the beginning frame, and do not continue playing
        """
        if self.__state == STOPPED:
            return # do nothing
        self.__state = STOPPED


    def togglePause(self):
        """
        If paused, start playing. If playing, then pause.
        """
        if self.__state == PLAYING:
            if self.isFinished():
                # the one exception: if this animation doesn't loop and it
                # has finished playing, then toggling the pause will cause
                # the animation to replay from the beginning.
                #self.__playingStartTime = time.time() # effectively the same as calling play()
                self.play()
            else:
                self.pause()
        elif self.__state in (PAUSED, STOPPED):
            self.play()
    
    @property
    def playingStartTime(self):
        return self.__playingStartTime

    @property
    def pausedStartTime(self):
        return self.__pausedStartTime
    
    @property
    def elapsed(self):
        """
        NOTE: Do to floating point rounding errors, this doesn't work precisely.

        Find out how long ago the play()/pause() functions were called.
        """
        if self.__state == STOPPED:
            # if stopped, then just return 0
            return 0
        else:
            if self.__state == PLAYING:
                # if playing, then draw the current frame (based on when the animation
                # started playing). If not looping and the animation has gone through
                # all the frames already, then draw the last frame.
                elapsed = (time.time() - self.__playingStartTime) * self.__rate
            elif self.__state == PAUSED:
                # if paused, then draw the frame that was playing at the time the
                # PygAnimation object was paused
                elapsed = (self.__pausedStartTime - self.__playingStartTime) * self.__rate

            if self.__loop:
                elapsed = elapsed % self.__startTimes[-1]
            else:
                elapsed = getInBetweenValue(0, elapsed, self.__startTimes[-1])

            elapsed += 0.00001 # done to compensate for rounding errors
            return elapsed

    # TODO Chad reconcile the two setElapsed functions!
    @elapsed.setter
    def elapsed(self, elapsed):
        """
        Sets the playing/paused time (depending on the current state) to a
        specific "elapsed time". For example, calling setElapsed(2) would
        set this animation object as though it had the play() function called
        2 seconds ago. This is handy if you want to sync multiple animations
        together.
        """
        if elapsed < 0:
            # a negative elapsed means "this many seconds from the end"
            elapsed = self.__startTimes[-1] + elapsed

        if self.__loop:
            elapsed = elapsed % self.__startTimes[-1]
        else:
            elapsed = getInBetweenValue(0, elapsed, self.__startTimes[-1])

        # set up the playing start time.
        rightNow = time.time()
        self.__playingStartTime = rightNow - elapsed
        if self.__state in (STOPPED, PAUSED):
            # if stopped or paused, also set up the paused starting time
            self.__pausedStartTime = rightNow
            self.__state = PAUSED # if stopped, then set to paused
            # "stopped" is only a valid state when the animation is at
            # the very beginning, otherwise, set it to the "paused" state.

    def areFramesSameSize(self):
        """
        Returns True if all the Surface objects in this animation object
        have the same width and height. Otherwise, returns False
        """
        width, height = self.getFrame(0).get_size()
        for i in range(len(self.__images)):
            if self.getFrame(i).get_size() != (width, height):
                return False
        return True

    def getMaxSize(self):
        """
        Goes through all the Surface objects in this animation object
        and returns the max width and max height that it finds. (These
        widths and heights may be on different Surface objects.)
        """
        frameWidths = []
        frameHeights = []
        for i in range(len(self.__images)):
            frameWidth, frameHeight = self.__images[i].get_size()
            frameWidths.append(frameWidth)
            frameHeights.append(frameHeight)
        maxWidth = max(frameWidths)
        maxHeight = max(frameHeights)

        return (maxWidth, maxHeight)

    def get_rect(self):
        """
        Returns a pygame.Rect object for this animation object.
        The top and left will be set to 0, 0, and the width and height
        will be set to what is returned by getMaxSize().
        """
        maxWidth, maxHeight = self.getMaxSize()
        return pygame.Rect(0, 0, maxWidth, maxHeight)

    def anchor(self, anchorPoint):
        """
        If the Surface objects are of different sizes, align them all to a
        specific "anchor point" (one of the NORTH, SOUTH, SOUTHEAST, etc. constants)
        
        By default, they are all anchored to the NORTHWEST corner.
        """
        if self.areFramesSameSize():
            return # nothing needs to be anchored
            # This check also prevents additional calls to anchor() from doing
            # anything, since anchor() sets all the image to the same size.
            # The lesson is, you can only effectively call anchor() once.

        self.clearTransforms() # clears transforms since this method anchors the original images.

        maxWidth, maxHeight = self.getMaxSize()
        halfMaxWidth = int(maxWidth / 2)
        halfMaxHeight = int(maxHeight / 2)

        for i in range(len(self.__images)):
            # go through and copy all frames to a max-sized Surface object
            # NOTE: This makes changes to the original images in self.__images, not the transformed images in self.__transformedImages
            newSurf = pygame.Surface((maxWidth, maxHeight)) # TODO: this is probably going to have errors since I'm using the default depth.

            # set the expanded areas to be transparent
            newSurf = newSurf.convert_alpha()
            newSurf.fill((0,0,0,0))

            frameWidth, frameHeight = self.__images[i].get_size()
            halfFrameWidth = int(frameWidth / 2)
            halfFrameHeight = int(frameHeight / 2)

            # position the Surface objects to the specified anchor point
            if anchorPoint == NORTHWEST:
                newSurf.blit(self.__images[i], (0, 0))
            elif anchorPoint == NORTH:
                newSurf.blit(self.__images[i], (halfMaxWidth - halfFrameWidth, 0))
            elif anchorPoint == NORTHEAST:
                newSurf.blit(self.__images[i], (maxWidth - frameWidth, 0))
            elif anchorPoint == WEST:
                newSurf.blit(self.__images[i], (0, halfMaxHeight - halfFrameHeight))
            elif anchorPoint == CENTER:
                newSurf.blit(self.__images[i], (halfMaxWidth - halfFrameWidth, halfMaxHeight - halfFrameHeight))
            elif anchorPoint == EAST:
                newSurf.blit(self.__images[i], (maxWidth - frameWidth, halfMaxHeight - halfFrameHeight))
            elif anchorPoint == SOUTHWEST:
                newSurf.blit(self.__images[i], (0, maxHeight - frameHeight))
            elif anchorPoint == SOUTH:
                newSurf.blit(self.__images[i], (halfMaxWidth - halfFrameWidth, maxHeight - frameHeight))
            elif anchorPoint == SOUTHEAST:
                newSurf.blit(self.__images[i], (maxWidth - frameWidth, maxHeight - frameHeight))
            self.__images[i] = newSurf


    def nextFrame(self, jump=1):
        """
        Set the elapsed time to the beginning of the next frame.
        You can jump ahead by multiple frames by specifying a different
        argument for jump.
        Negative values have the same effect as calling prevFrame()
        """
        self.setFrameNum(self.currentFrameNum + int(jump))


    def prevFrame(self, jump=1):
        """
        Set the elapsed time to the beginning of the previous frame.
        You can jump ahead by multiple frames by specifying a different
        argument for jump.
        Negative values have the same effect as calling nextFrame()
        """
        self.setFrameNum(self.currentFrameNum - int(jump))

    @property
    def currentFrameNum(self):
        """
        Return the frame number of the frame that will be currently
        displayed if the animation object were drawn right now.
        """
        return findStartTime(self.__startTimes, self.elapsed)

    @currentFrameNum.setter
    def currentFrameNum(self, frameNum):
        """
        Change the elapsed time to the beginning of a specific frame.
        """
        if self.__loop:
            frameNum = frameNum % len(self.__images)
        else:
            frameNum = getInBetweenValue(0, frameNum, len(self.__images)-1)
        self.setElapsed(self.__startTimes[frameNum])


    def rewind(self, seconds=None):
        """
        Set the elapsed time back relative to the current elapsed time.
        """
        if seconds is None:
            self.setElapsed(0.0)
        else:
            elapsed = self.elapsed
            self.setElapsed(elapsed - seconds)


    def fastforward(self, seconds=None):
        """
        Set the elapsed time forward relative to the current elapsed time.
        """
        if seconds is None:
            self.setElapsed(self.__startTimes[-1] - 0.00002) # done to compensate for rounding errors
        else:
            elapsed = self.elapsed
            self.setElapsed(elapsed + seconds)


    def setElapsed(self, elapsed):
        """
        NOTE: Do to floating point rounding errors, this doesn't work precisely.
        """
        elapsed += 0.00001 # done to compensate for rounding errors

        # Set the elapsed time to a specific value.
        if self.__loop:
            elapsed = elapsed % self.__startTimes[-1]
        else:
            elapsed = getInBetweenValue(0, elapsed, self.__startTimes[-1])

        rightNow = time.time()
        self.__playingStartTime = rightNow - (elapsed * self.__rate)

        if self.__state in (PAUSED, STOPPED):
            self.__state = PAUSED # if stopped, then set to paused
            self.__pausedStartTime = rightNow


    def __makeTransformedSurfacesIfNeeded(self):
        """
        Internal-method. Creates the Surface objects for the _transformedImages list.
        Don't call this method.
        """
        if self.__transformedImages == []:
            self.__transformedImages = [surf.copy() for surf in self.__images]


    # Transformation methods.
    # (These are analogous to the pygame.transform.* functions, except they
    # are applied to all frames of the animation object.
    def flip(self, xbool, ybool):
        """
        Flips the image horizontally, vertically, or both.
        See http://pygame.org/docs/ref/transform.html#pygame.transform.flip
        """
        self.__makeTransformedSurfacesIfNeeded()
        for i in range(len(self.__images)):
            self.__transformedImages[i] = pygame.transform.flip(self.getFrame(i), xbool, ybool)


    def scale(self, width_height):
        """
        NOTE: Does not support the DestSurface parameter
        Increases or decreases the size of the images.
        See http://pygame.org/docs/ref/transform.html#pygame.transform.scale
        """
        self.__makeTransformedSurfacesIfNeeded()
        for i in range(len(self.__images)):
            self.__transformedImages[i] = pygame.transform.scale(self.getFrame(i), width_height)


    def rotate(self, angle):
        """
        Rotates the image.
        See http://pygame.org/docs/ref/transform.html#pygame.transform.rotate
        """
        self.__makeTransformedSurfacesIfNeeded()
        for i in range(len(self.__images)):
            self.__transformedImages[i] = pygame.transform.rotate(self.getFrame(i), angle)


    def rotozoom(self, angle, scale):
        """
        Rotates and scales the image simultaneously.
        See http://pygame.org/docs/ref/transform.html#pygame.transform.rotozoom
        """
        self.__makeTransformedSurfacesIfNeeded()
        for i in range(len(self.__images)):
            self.__transformedImages[i] = pygame.transform.rotozoom(self.getFrame(i), angle, scale)


    def scale2x(self):
        """
        NOTE: Does not support the DestSurface parameter
        Double the size of the image using an efficient algorithm.
        See http://pygame.org/docs/ref/transform.html#pygame.transform.scale2x
        """
        self.__makeTransformedSurfacesIfNeeded()
        for i in range(len(self.__images)):
            self.__transformedImages[i] = pygame.transform.scale2x(self.getFrame(i))


    def smoothscale(self, width_height):
        """
        NOTE: Does not support the DestSurface parameter
        Scales the image smoothly. (Computationally more expensive and
        slower but produces a better scaled image.)
        See http://pygame.org/docs/ref/transform.html#pygame.transform.smoothscale
        """
        self.__makeTransformedSurfacesIfNeeded()
        for i in range(len(self.__images)):
            self.__transformedImages[i] = pygame.transform.smoothscale(self.getFrame(i), width_height)



    # pygame.Surface method wrappers
    # These wrappers call their analogous pygame.Surface methods on all Surface objects in this animation.
    # They are here for the convenience of the module user. These calls will apply to the transform images,
    # and can have their effects undone by called clearTransforms()
    #
    # It is not advisable to call these methods on the individual Surface objects in self.__images.
    def _surfaceMethodWrapper(self, wrappedMethodName, *args, **kwargs):
        self.__makeTransformedSurfacesIfNeeded()
        for i in range(len(self.__images)):
            methodToCall = getattr(self.__transformedImages[i], wrappedMethodName)
            methodToCall(*args, **kwargs)

    # There's probably a more terse way to generate the following methods,
    # but I don't want to make the code even more unreadable.
    def convert(self, *args, **kwargs):
        """
        See http://pygame.org/docs/ref/surface.html#Surface.convert
        """
        self._surfaceMethodWrapper('convert', *args, **kwargs)


    def convert_alpha(self, *args, **kwargs):
        """
        See http://pygame.org/docs/ref/surface.html#Surface.convert_alpha
        """
        self._surfaceMethodWrapper('convert_alpha', *args, **kwargs)


    def set_alpha(self, *args, **kwargs):
        """
        See http://pygame.org/docs/ref/surface.html#Surface.set_alpha
        """
        self._surfaceMethodWrapper('set_alpha', *args, **kwargs)


    def get_alpha(self):
        """
        See http://pygame.org/docs/ref/surface.html#Surface.get_alpha
        
        This method raises an error to remind the module user that the
        individual Surface objects in this animation object can have
        different alpha values. Use animObj.getFrame(0).get_alpha()
        instead.
        """
        raise NotImplementedError('get_alpha() must be called on a single Surface object, not the PygAnimation object. Use <animObj>.getFrame(0).get_alpha() instead.')


    def scroll(self, *args, **kwargs):
        """
        See http://pygame.org/docs/ref/surface.html#Surface.scroll
        """
        self._surfaceMethodWrapper('scroll', *args, **kwargs)


    def set_clip(self, *args, **kwargs):
        """
        See http://pygame.org/docs/ref/surface.html#Surface.set_clip
        """
        self._surfaceMethodWrapper('set_clip', *args, **kwargs)


    def get_clip(self):
        """
        See http://pygame.org/docs/ref/surface.html#Surface.get_clip
        
        This method raises an error to remind the module user that the
        individual Surface objects in this animation object can have
        different clip values. Use animObj.getFrame(0).get_clip()
        instead.
        """
        raise NotImplementedError('get_clip() must be called on a single Surface object, not the PygAnimation object. Use <animObj>.getFrame(0).get_clip() instead.')


    def set_colorkey(self, *args, **kwargs):
        """
        See http://pygame.org/docs/ref/surface.html#Surface.set_colorkey
        """
        self._surfaceMethodWrapper('set_colorkey', *args, **kwargs)


    def get_colorkey(self):
        """
        See http://pygame.org/docs/ref/surface.html#Surface.get_colorkey
        
        This method raises an error to remind the module user that the
        individual Surface objects in this animation object can have
        different colorkey values. Use animObj.getFrame(0).get_colorkey()
        instead.
        """
        raise NotImplementedError('get_colorkey() must be called on a single Surface object, not the PygAnimation object. Use <animObj>.getFrame(0).get_colorkey() instead.')


    def lock(self, *args, **kwargs):
        """
        See http://pygame.org/docs/ref/surface.html#Surface.unlock
        """
        self._surfaceMethodWrapper('lock', *args, **kwargs)


    def unlock(self, *args, **kwargs):
        """
        See http://pygame.org/docs/ref/surface.html#Surface.lock
        """
        self._surfaceMethodWrapper('unlock', *args, **kwargs)



    # Getter and setter methods for properties
    # TODO Chad make this proper Python OO
    @property
    def rate(self):
        return self.__rate
    
    @rate.setter
    def rate(self, rate):
        rate = float(rate)
        if rate < 0:
            raise ValueError('rate must be greater than 0.')
        self.__rate = rate

    @property
    def loop(self):
        return self.__loop

    @loop.setter
    def loop(self, loop):
        if self.__state == PLAYING and self.__loop and not loop:
            # if we are turning off looping while the animation is playing,
            # we need to modify the _playingStartTime so that the rest of
            # the animation will play, and then stop. (Otherwise, the
            # animation will immediately stop playing if it has already looped.)
            self.__playingStartTime = time.time() - self.elapsed
        self.__loop = bool(loop)

    @property
    def state(self):
        if self.isFinished():
            self.__state = STOPPED # if finished playing, then set state to STOPPED.

        return self.__state
    
    @state.setter
    def state(self, state):
        if state not in (PLAYING, PAUSED, STOPPED):
            raise ValueError('state must be one of pyganim.PLAYING, pyganim.PAUSED, or pyganim.STOPPED')
        if state == PLAYING:
            self.play()
        elif state == PAUSED:
            self.pause()
        elif state == STOPPED:
            self.stop()

    @property
    def visibility(self):
        return self.__visibility

    @visibility.setter
    def visibility(self, visibility):
        self.__visibility = bool(visibility)

class PygGroup(object):
    def __init__(self):
        pass
"""
Add/remove group. check for group membership. Remove all from group, etc.
in operator usage.

play()
pause()


"""



def getInBetweenValue(lowerBound, value, upperBound):
    """
    Returns the value within the bounds of the lower and upper bound parameters.
    If value is less than lowerBound, then return lowerBound.
    If value is greater than upperBound, then return upperBound.
    Otherwise, just return value as it is.
    """
    if value < lowerBound:
        return lowerBound
    elif value > upperBound:
        return upperBound
    return value


def findStartTime(startTimes, target):
    """
    With startTimes as a list of sequential numbers and target as a number,
    returns the index of the number in startTimes that preceeds target.
    
    For example, if startTimes was [0, 2, 4.5, 7.3, 10] and target was 6,
    then findStartTime() would return 2. If target was 12, returns 4.
    """
    assert startTimes[0] == 0
    lb = 0 # "lb" is lower bound
    ub = len(startTimes) - 1 # "ub" is upper bound

    # handle special cases:
    if len(startTimes) == 0:
        return 0
    if target >= startTimes[-1]:
        return ub - 1

    # perform binary search:
    while True:
        i = int((ub - lb) / 2) + lb

        if startTimes[i] == target or (startTimes[i] < target and startTimes[i+1] > target):
            if i == len(startTimes):
                return i - 1
            else:
                return i

        if startTimes[i] < target:
            lb = i
        elif startTimes[i] > target:
            ub = i
