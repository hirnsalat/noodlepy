from constants import *

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
