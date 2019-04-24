from constants import *

class Grid:
    def __init__(self, rows):
        self.rows = rows
        self.activerow = 0
        self.arrangerview = True

    def up(self):
        self.activerow = (self.activerow - 1) % len(self.rows)

    def down(self):
        self.activerow = (self.activerow + 1) % len(self.rows)

    def right(self):
        for row in self.rows:
            row.right()

    def left(self):
        for row in self.rows:
            row.left()

    def zoom(self):
        self.arrangerview = not self.arrangerview

    def play(self):
        self.rows[self.activerow].play()

    def toggle_start(self):
        self.rows[self.activerow].toggle_start()

    def toggle_end(self):
        self.rows[self.activerow].toggle_end()

    def tick(self, time):
        for row in self.rows:
            row.tick(time)

    def visual(self, row, col, step):
        if self.arrangerview:
            color = WHITE
            if not self.rows[row].playing == col:
                color = self.rows[row].color
            return (color, self.activerow == row and self.rows[row].visible == col)
        else:
            return self.rows[self.activerow].visual(row, col, step)

    def click(self, row, col):
        if self.arrangerview:
            self.activerow = row
            for r in self.rows:
                r.visible = col
        else:
            return self.rows[self.activerow].click(row, col)


class Row:
    def __init__(self, ClipType, color):
        self.clips = [ClipType() for i in range(0,8)]
        self.playing = 0
        self.visible = 0
        self.next = -1
        self.loopend = [False, True] + [False] * 6
        self.loopstart = [False] * 8
        self.color = color

    def right(self):
        self.visible = (self.visible + 1) % 8

    def left(self):
        self.visible = (self.visible - 1) % 8

    def play(self):
        self.next = self.visible

    def toggle_start(self):
        self.loopstart[self.visible] = not self.loopstart[self.visible]

    def toggle_end(self):
        self.loopend[self.visible] = not self.loopend[self.visible]

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

#    def visual(self):
#        return self.clips[self.visible].visual()

    def visual(self, row, col, step):
        color = self.color
        if self.playing == self.visible and step == col:
            color = WHITE
        return (color, self.clips[self.visible].visual()[row][col])

    def click(self, row, col):
        return self.clips[self.visible].click(row, col)

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

    def visual(self):
        return self.seqs

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
