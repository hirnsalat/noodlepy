import sys
import pygame
import pygame.midi
import pygame.time
from pygame.locals import *

fourchords = [[0,4,7],[-1,2,7],[-3,0,4],[-3,0,5]]
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
            True,  True,  True,  True]

ticksperstep = 16
stepsperbeat = 4
beatsperpattern = 4
beatsperminute = 120
ticksperbeat = ticksperstep * stepsperbeat
ticksperpattern = ticksperbeat * beatsperpattern
tickspersecond = (ticksperbeat * beatsperminute) // 60

framespersecond = 30
ticksperframe = tickspersecond // framespersecond

print(f"ticksperbeat: {ticksperbeat}")
print(f"tickspersecond: {tickspersecond}")
print(f"framespersecond: {framespersecond}")
print(f"ticksperframe: {ticksperframe}")

class Timekeeper:
    def __init__(self):
        self.n = 0
        self.beat = 0
        self.step = 0
        self.measure = 0
        self.inbeat = 0
        self.instep = 0
        self.newframe = True
        self._clock = pygame.time.Clock()

    def tick(self):
        self.n += 1
        self.inbeat += 1
        self.instep += 1
        if self.n == ticksperpattern:
            self.n = 0
            self.beat = 0
            self.step = 0
            self.measure += 1
            self.inbeat = 0
            self.instep = 0
        elif self.n % ticksperbeat == 0:
            self.beat += 1
            self.inbeat = 0
            self.step += 1
            self.instep = 0
        elif self.n % ticksperstep == 0:
            self.step += 1
            self.instep = 0
        if self.n % ticksperframe == 0:
            self.newframe = True
        else:
            self.newframe = False
        self._clock.tick(tickspersecond)


class Sequence:
    def __init__(self, note, seq, out):
        self.note = note
        self.seq = seq
        self.out = out
        self.on = False

    def tick(self, time):
        if time.instep == 0 and self.seq[time.step]:
            self.out.note_on(self.note, 127)
            self.on = True
        elif self.on:
            self.out.note_off(self.note)
            self.on = False

pygame.init()
pygame.midi.init()

port = pygame.midi.get_default_output_id()

midi_out = pygame.midi.Output(port, 0)

time = Timekeeper()

base = 60
n = 0
seqs = [Sequence(36, bassdrum, midi_out)
       ,Sequence(37, snare,    midi_out)
       ,Sequence(42, hihat,    midi_out)
       ]

def drawframe(screen, time, seq):
    brightness = (ticksperstep*2) - time.inbeat
    brightness *= 2
    if brightness < 0:
        brightness = 0
    screen.fill([brightness, brightness, brightness])

    for i in range(0,16):
        if time.step == i:
            color = [255,0,0] # TODO make pink
        else:
            color = [255,255,255]
        if seq[i]:
            width = 0
        else:
            width = 1
        pygame.draw.rect(screen, color, Rect(8+80*(i%8),48+80*(i//8),64,64), width)
    pygame.display.flip()

try:
    screen = pygame.display.set_mode([640,480], pygame.RESIZABLE)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        for s in seqs:
            s.tick(time)

        if time.newframe:
            drawframe(screen, time, bassdrum)

        time.tick()
finally:
    for i in range(0,127):
        midi_out.note_off(i)
    midi_out.close()
    del midi_out
    pygame.midi.quit()
