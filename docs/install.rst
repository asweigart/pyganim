.. default-role:: code
============
Installation
============

Background Information
======================

Pyganim requires Pygame to run, and also requires PIL or Pillow to use the animated GIF loading feature.

Pyganim runs on Python 2.5, 2.6, 2.7, 3.1, 3.2, and 3.3.

Currently there is no Pillow module for Python 3.1, so the animated GIF loading does not work on that version. There is no Pygame version currently available for Python 3.4.

Installation
============

Pyganim can be installed using pip by running:

    pip install pyganim

On OS X and Linux, you may need to use sudo:

    sudo pip install pyganim

To test if the installation worked, run `import pyganim` from the interactive shell. Pygame (and, optionally, PIL or Pillow) will need to be installed separately.