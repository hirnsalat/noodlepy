from constants import *

class Grid:
    def __init__(self):
        self.tracks = []
        self.trackmeta = []
        self.row = 0
        self.col = 0
        self.width = 8 # TODO
        self.arrangerview = True

    def gettitle(self):
        if self.arrangerview:
            return ("ARRANGE", WHITE)
        else:
            return (f"{self.trackmeta[self.row][0]} {self.col}", self.trackmeta[self.row][1])

    def addtrack(self, name, color, track, hicolor=WHITE, bgcolor=BLACK):
        self.tracks.append(track)
        self.trackmeta.append((name, color, hicolor, bgcolor))

    def up(self):
        self.row = (self.row - 1) % len(self.tracks)

    def down(self):
        self.row = (self.row + 1) % len(self.tracks)

    def right(self):
        self.col = (self.col + 1) % self.width

    def left(self):
        self.col = (self.col - 1) % self.width

    def zoom(self):
        self.arrangerview = not self.arrangerview

    def play(self):
        self.track[self.row].prime(self.col)

    def toggle_start(self):
        self.tracks[self.row].toggle_start(self.col)

    def toggle_end(self):
        self.tracks[self.row].toggle_end(self.col)

    def tick(self, time):
        for track in self.tracks:
            track.tick(time)

    def visual(self, row, col, step):
        if self.arrangerview:
            if self.tracks[row].playing == col:
                color = self.trackmeta[row][2]
            else:
                color = self.trackmeta[row][1]
            return (color, self.row == row and self.col == col)
        else:
            if self.tracks[self.row].playing == self.col and step == col:
                color = self.trackmeta[self.row][2]
            else:
                color = self.trackmeta[self.row][1]
            return (color, self.tracks[self.row].clips[self.col].isactive(row, col))

    def click(self, row, col):
        if self.arrangerview:
            self.row = row
            self.col = col
        else:
            return self.tracks[self.row].clips[self.col].click(row, col)


class Track:
    def __init__(self, ClipType):
        self.clips = [ClipType() for i in range(0,8)]
        self.playing = 0
        self.next = -1
        self.loopend = [False, True] + [False] * 6
        self.loopstart = [False] * 8

    def prime(self, clipind):
        self.next = clipind

    def toggle_start(self, clipind):
        self.loopstart[clipind] = not self.loopstart[clipind]

    def toggle_end(self, clipind):
        self.loopend[clipind] = not self.loopend[clipind]

    def tick(self, time):
        if time.step == 0 and time.instep == 0:
            if self.next >= 0:
                self.playing = self.next
                self.next = -1
            elif self.loopend[self.playing]:
                while self.playing > 0 and not self.loopstart[self.playing]:
                    self.playing -= 1
            else:
                self.playing = (self.playing + 1) % 8
        self.clips[self.playing].tick(time)



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
