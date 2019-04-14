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
ticksperminute = ticksperbeat * beatsperminute
ticksperpattern = ticksperbeat * beatsperpattern
tickspersecond = ticksperminute // 60

framespersecond = 30
ticksperframe = tickspersecond // framespersecond
mspertick = 60000 // ticksperminute

print(f"ticksperbeat: {ticksperbeat}")
print(f"tickspersecond: {tickspersecond}")
print(f"framespersecond: {framespersecond}")
print(f"ticksperframe: {ticksperframe}")

class Timekeeper:
    def __init__(self, midi_out):
        self.n = 0
        self.beat = 0
        self.step = 0
        self.measure = 0
        self.inbeat = 0
        self.instep = 0
        self.newframe = True
        self._midi_out = midi_out
        self._midi_ms = pygame.midi.time()
        self._midi_events = []
        self.listeners = []

    def add_listener(self, l):
        self.listeners.append(l)

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
        self._midi_ms += mspertick

    def first_frame(self):
        for l in self.listeners:
            l.tick(self)
        self.to_next_frame()

    def to_next_frame(self):
        self.tick()
        while not self.newframe:
            for l in self.listeners:
                l.tick(self)
            self.tick()
        for l in self.listeners:
            l.tick(self)
        self._flush()

    def _flush(self):
        self._midi_out.write(self._midi_events)
        self._midi_events = []

    def note_on(self, note, velocity):
        #print(f"on: {note}, {velocity}, {self._midi_ms}")
        self._midi_events.append([[0x90, note, velocity], self._midi_ms])
    def note_off(self, note):
        #print(f"off: {note}, {self._midi_ms}")
        self._midi_events.append([[0x80, note, 0], self._midi_ms])


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

midi_out = pygame.midi.Output(port, latency = 1)
clock = pygame.time.Clock()
screen = pygame.display.set_mode([640,480], pygame.RESIZABLE)
time = Timekeeper(midi_out)

base = 60
n = 0
time.add_listener(Sequence(36, bassdrum, time))
time.add_listener(Sequence(37, snare,    time))
time.add_listener(Sequence(42, hihat,    time))

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
    time.first_frame()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        drawframe(screen, time, bassdrum)

        time.to_next_frame()

        clock.tick(framespersecond)
finally:
    for i in range(0,127):
        midi_out.note_off(i)
    midi_out.close()
    del midi_out
    pygame.midi.quit()
