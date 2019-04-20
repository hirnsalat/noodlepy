import sys
import pygame
import pygame.midi
import pygame.time
from pygame.locals import *

from timing import Timekeeper
from sequence import DrumSequence, ChordSequence
from constants import *

#fourchords = [[0,4,7],[-1,2,7],[-3,0,4],[-3,0,5]]
#bassnotes = [[0],[-5],[-3],[-7]]
fourchords = [[-3,0,4],[-5,-1,2],[-7,-3,0],[-8,-4,-1]]
bassnotes = [[-3],[-5],[-7],[-8]]
bassdrum = [True,  False, False, False,
            False, False, False, False,
            True,  False, True,  False,
            False, False, False, False]
snare    = [False, False, False, False,
            True,  False, False, False,
            False, False, False, False,
            True,  False, False, False]
hihat    = [True,  False, True,  False,
            True,  False, True,  False,
            True,  False, True,  False,
            True,  False, True,  False]
chords   = [True,  False, False, False,
            True,  False, False, False,
            True,  False, False, False,
            True,  False, False, False]
bassseq  = [True,  False, True,  False,
            True,  False, True,  False,
            True,  False, True,  False,
            True,  False, True,  False]

print(f"ticksperbeat: {ticksperbeat}")
print(f"tickspersecond: {tickspersecond}")
print(f"framespersecond: {framespersecond}")
print(f"ticksperframe: {ticksperframe}")

pygame.init()
pygame.midi.init()

port = pygame.midi.get_default_output_id()

midi_out = pygame.midi.Output(port, latency = 1)
clock = pygame.time.Clock()
screen = pygame.display.set_mode([640,480], pygame.RESIZABLE)
time = Timekeeper(midi_out)

time.add_listener(DrumSequence(0, 36, bassdrum, time))
time.add_listener(DrumSequence(0, 37, snare,    time))
time.add_listener(DrumSequence(0, 42, hihat,    time))
time.add_listener(ChordSequence(1, 72, fourchords, chords,  time))
time.add_listener(ChordSequence(2, 48, bassnotes,  bassseq, time))

activeseq = bassdrum
allseqs = [bassdrum, snare, hihat, chords, bassseq]

def handle_key(event, seq):
    sc = event.scancode
    if 38 <= sc <= 45:
        seq[sc - 38] = not seq[sc - 38]
    elif 52 <= sc <= 59:
        seq[sc - 44] = not seq[sc - 44]
    elif 10 <= sc < 10 + len(allseqs):
        return allseqs[sc-10]
    else:
        print(sc)
    return seq

def drawframe(screen, time, seq):
    brightness = (ticksperstep*2) - time.inbeat
    brightness *= 2
    if brightness < 0:
        brightness = 0
    screen.fill([brightness, brightness, brightness])

    for i in range(0,16):
        if time.step == i:
            color = ONCOLOR # TODO make pink
        else:
            color = OFFCOLOR
        if seq[i]:
            width = 0
        else:
            width = 1
        pygame.draw.rect(screen, color, Rect(8+80*(i%8),48+80*(i//8),64,64), width)
    pygame.display.flip()

try:
    time.first_frame()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type == pygame.KEYDOWN: activeseq = handle_key(event, activeseq)
            #else: print(event)

        drawframe(screen, time, activeseq)

        time.to_next_frame()

        clock.tick(framespersecond)
        #print(clock.get_fps())
finally:
    for i in range(0,127):
        midi_out.note_off(i)
    midi_out.close()
    del midi_out
    pygame.midi.quit()
