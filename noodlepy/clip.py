from constants import *

class Clip:
    def __init__(self):
        pass

    def tick(self, time):
        pass

    def click(self, row, col):
        pass

    def visual(self):
        pass

# i don't know how the metaclip thing will work. is it also a clip? or not? who knows! it's probably a clip for most purposes.

class NoteClip(Clip):
    # todo: monophony
    def __init__(self, channel, notes):
        super().__init__()
        self.channel = channel
        self.notes = notes
        self.seqs = [[False] * 8,[False] * 8,[False] * 8,[False] * 8]

    def tick(self, time):
        if time.instep == 0:
            for i in range(0,4):
                if self.seqs[i][time.step]:
                    time.note_on(self.channel, self.notes[3-i], 127)
        elif time.instep == 12:
            for i in range(0,4):
                if self.seqs[i][time.step]:
                    time.note_off(self.channel, self.notes[3-i])

    def click(self, row, col):
        self.seqs[row][col] = not self.seqs[row][col]

    def isactive(self, row, col):
        return self.seqs[row][col]

class MonoClip(NoteClip):
    def click(self, row, col):
        self.seqs[row][col] = not self.seqs[row][col]
        for i in range(0,4):
            if not i == row:
                self.seqs[i][col] = False

class ChordState:
    def __init__(self):
        self.base = 69 # middle A. i think.
        #self.scale = [0,2,4,5,7,9,11] # major
        self.scale = [0,2,3,5,7,-4,-2] # minor
        self.degree = 0
        self.chordnotes = [0,0,0]
        self.leadnotes = [0,0,0,0]
        self.bassnotes = [0,0,0,0]
        self._update()

    def getscalenote(self, i):
        ret = self.scale[(i + self.degree) % len(self.scale)]
        return self.base + ret

    def _update(self):
        self.bassnotes[0] = self.getscalenote(0) - 24
        self.bassnotes[1] = self.getscalenote(4) - 24
        if self.bassnotes[1] < self.bassnotes[0]:
            self.bassnotes[1] += 12
        self.bassnotes[2] = self.bassnotes[0] + 12
        self.bassnotes[3] = self.bassnotes[1] + 12
        self.chordnotes[0] = self.getscalenote(0)
        self.chordnotes[1] = self.getscalenote(2)
        self.chordnotes[2] = self.getscalenote(4)
        self.chordnotes.sort()
        self.leadnotes[:3] = self.chordnotes
        self.leadnotes[3] = self.leadnotes[0] + 12

    def setdegree(self, i):
        self.degree = i % len(self.scale)
        self._update()

_chordstate = ChordState()

class BassClip(MonoClip):
    def __init__(self, channel):
        super().__init__(channel, _chordstate.bassnotes)

class LeadClip(MonoClip):
    def __init__(self, channel):
        super().__init__(channel, _chordstate.leadnotes)

class ChordClip(Clip):
    def __init__(self, channel):
        self.channel = channel
        self.chord = _chordstate
        self.notes = self.chord.chordnotes
        self.steps = [False] * 9
        self.degree = 0
        self.on = False

    def tick(self, time):
        if time.step == 0 and time.instep == 0:
            self.chord.setdegree(self.degree)

        if time.instep == 0 and self.steps[time.step] and not self.on:
            self.on = True
            for i in self.notes:
                time.note_on(self.channel, i, 127)
        elif time.instep == 12 and self.on and not self.steps[time.step +1]:
            self.on = False
            for i in self.notes:
                time.note_off(self.channel, i)

    def click(self, row, col):
        if row == 0:
            self.degree = col
        elif row == 3:
            self.steps[col] = not self.steps[col]

    def isactive(self, row, col):
        if row == 0:
            return self.degree == col
        elif row == 3:
            return self.steps[col]
        return False

"""
# chord thing will be more complicated, some 4 row thing
# row 1 base note
# row 2 variation (sus4, b7#9)
# row 3 arp (chord, 2 octave chord, quick 1, quick 2, up, down, updown, random)
# row 4 rhythm (like other patterns)
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
"""
