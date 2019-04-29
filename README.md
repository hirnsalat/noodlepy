# noodlepy

Hello, this is noodlepy, a software sequencer/arpeggiator/thing written in [pygame](https://www.pygame.org). It is still in early development, so please excuse the lack of proper documentation.

## installation

The requirements are:

- [Python 3](https://www.python.org)
- [pygame](https://www.pygame.org)
- [Anonymous Pro](https://www.marksimonson.com/fonts/view/anonymous-pro)

To run noodlepy, install the requirements, copy `noodlepy/conf.default.py` to `noodlepy/conf.py`, and run `noodle.py`.

## how to use

The computer keyboard corresponds to the pads on screen. The top left pad is the '1' key, the one to the right of that is the '2' key, and so on. Bottom right pad is the ',' key.

In arrangement view, each pad corresponds to one of the 8 clips in each of the 4 tracks. Press a pad/key to play the corresponding clip, in time. Play continues to the right and loops. Press shift and a key to edit the corresponding clip.

In clip view, pads turn different notes on or off. Arrow keys can be used to move between the clips, and Escape returns to arrangement view. F11 and F12 set loop start/end flags.

Things are still moving around, so this might be out of date ;)
