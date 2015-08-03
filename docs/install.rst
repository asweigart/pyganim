.. default-role:: code
============
Installation
============

Background Information
======================

Pyganim (pronounced like "pig" and "animation") is a Python module for Pygame that makes it easy to add sprite animations to your Pygame programs. Pyganim works with Python 2 and Python 3.

The mascot of Pyganim is a red vitruvian pig.

Pyganim was written by Al Sweigart and released under a "Simplified BSD" license. Contact Al with any questions/bug reports: al@inventwithpython.com

This documentation can be found at https://pyganim.readthedocs.org

Pyganim requires Pygame to run, and also requires PIL or Pillow to use the animated GIF loading feature.

Pyganim runs on Python 2.5, 2.6, 2.7, 3.1, 3.2, 3.3, 3.4.

Currently there is no Pillow module for Python 3.1, so the animated GIF loading does not work on that version. There is no Pygame version currently available for Python 3.5.

Installation
============

Pyganim can be installed using pip by running:

    pip install pyganim

The PyPI entry is at https://pypi.python.org/pypi/Pyganim

To test if the installation worked, run `import pyganim` from the interactive shell. Pygame (and, optionally, PIL or Pillow) will need to be installed separately.

Basic Usage
===========

First, create an animation object:

    import pyganim
    animObj = pyganim.PygAnimation([('frame1.png', 200), ('frame2.png', 200), ('frame3.png', 600)])
    animObj.play()

Then, during the program's loop when it must draw to the Surface object, call the `blit()` method and pass it the Surface object to draw on along with the XY coordinates:

    animObj.blit(windowSurface, (x, y))

Here's a small example program, given the following lightning bolt images:

.. image:: bolt_strike_0001.png

.. image:: bolt_strike_0002.png

.. image:: bolt_strike_0003.png

.. image:: bolt_strike_0004.png

.. image:: bolt_strike_0005.png

.. image:: bolt_strike_0006.png

.. image:: bolt_strike_0007.png

.. image:: bolt_strike_0008.png

.. image:: bolt_strike_0009.png

.. image:: bolt_strike_0010.png

The source code is:

    import pygame
    from pygame.locals import *
    import pyganim

    pygame.init()
    windowSurface = pygame.display.set_mode((320, 240), 0, 32)
    pygame.display.set_caption('Pyganim Basic Demo')

    boltAnim = pyganim.PygAnimation([('bolt_strike_0001.png', 100),
                                     ('bolt_strike_0002.png', 100),
                                     ('bolt_strike_0003.png', 100),
                                     ('bolt_strike_0004.png', 100),
                                     ('bolt_strike_0005.png', 100),
                                     ('bolt_strike_0006.png', 100),
                                     ('bolt_strike_0007.png', 100),
                                     ('bolt_strike_0008.png', 100),
                                     ('bolt_strike_0009.png', 100),
                                     ('bolt_strike_0010.png', 100)])
    boltAnim.play()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        windowSurface.fill((100, 50, 50))
        boltAnim.blit(windowSurface, (100, 50))
        pygame.display.update()

.. image:: basic_demo_screenshot.png

Other examples exist in the `/examples` folder.

