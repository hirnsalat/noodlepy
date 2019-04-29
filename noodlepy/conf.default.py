from pygame import Color
from grid import Grid
from track import Track
from clip import NoteClip, ChordClip, LeadClip, BassClip

def get_grid():
    # colors can be configured :D
    C_PINK = Color("#ff00ff")
    C_BLUE = Color("#00ffff")
    C_YELL = Color("#ffff00")
    C_GREE = Color("#00ff00")
    
    the_grid = Grid()

    # midi channel for different tracks is here ---------------v
    the_grid.addtrack("CHRD", C_PINK, Track(lambda: ChordClip( 0)))
    the_grid.addtrack("LEAD", C_BLUE, Track(lambda: LeadClip(  1)))
    the_grid.addtrack("BASS", C_YELL, Track(lambda: BassClip(  2)))
    the_grid.addtrack("DRUM", C_GREE, Track(lambda: NoteClip(  3, [36,37,41,42])))
    # notes for the drum tracks can be set here -------------------^^^^^^^^^^^

    return the_grid
