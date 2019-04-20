import sys
import pygame
import pygame.midi
import pygame.time
from pygame.locals import *

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

ONCOLOR = Color("#f437f5")
OFFCOLOR = Color("#ffffff")

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
        self.bar = 0
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
            self.bar += 1
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

    def note_on(self, channel, note, velocity):
        #print(f"on: {note}, {velocity}, {self._midi_ms}")
        self._midi_events.append([[0x90+channel, note, velocity], self._midi_ms])
    def note_off(self, channel, note):
        #print(f"off: {note}, {self._midi_ms}")
        self._midi_events.append([[0x80+channel, note, 0], self._midi_ms])


class Sequence:
    def __init__(self, seq):
        self.seq = seq
        self.on = False

    def tick(self, time):
        if time.instep == 0 and self.seq[time.step]:
            self.do_on(time.bar, time.step);
            self.on = True
        elif self.on and time.instep == 12:
            self.do_off(time.bar, time.step);
            self.on = False

class DrumSequence(Sequence):
    def __init__(self, channel, note, seq, out):
        Sequence.__init__(self, seq)
        self.channel = channel
        self.note = note
        self.out = out

    def do_on(self, bar, step):
        self.out.note_on(self.channel, self.note, 127)

    def do_off(self, bar, step):
        self.out.note_off(self.channel, self.note)

class ChordSequence(Sequence):
    def __init__(self, channel, basenote, notes, seq, out):
        Sequence.__init__(self, seq)
        self.channel = channel
        self.basenote = basenote
        self.notes = notes
        self.out = out

    def do_on(self, bar, step):
        for note in self.notes[bar % 4]:
            self.out.note_on(self.channel, self.basenote + note, 127)

    def do_off(self, bar, step):
        for note in self.notes[bar % 4]:
            self.out.note_off(self.channel, self.basenote + note)

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
