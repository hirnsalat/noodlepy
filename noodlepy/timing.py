import sys
import pygame
import pygame.midi
import pygame.time
from pygame.locals import *

from constants import *

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
