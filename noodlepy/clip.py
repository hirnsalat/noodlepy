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
