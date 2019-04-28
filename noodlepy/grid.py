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
            return ("ARRANGEMENT", WHITE)
        else:
            startchar = endchar = " "
            if self.tracks[self.row].loopstart[self.col] or self.col == 0:
                startchar = "["
            if self.tracks[self.row].loopend[self.col] or self.col == 7:
                endchar = "]"
            return (f"{self.trackmeta[self.row][0]} {self.col}       {startchar} {endchar}", self.trackmeta[self.row][1])

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
        self.tracks[self.row].prime(self.col)

    def toggle_start(self):
        self.tracks[self.row].toggle_start(self.col)

    def toggle_end(self):
        self.tracks[self.row].toggle_end(self.col)

    def tick(self, time):
        for track in self.tracks:
            track.tick(time)

    def visual(self, row, col, step):
        flags = 0
        if self.arrangerview:
            active = self.tracks[row].next == col
            if self.tracks[row].playing == col:
                color = self.trackmeta[row][2]
            else:
                color = self.trackmeta[row][1]
            bgcolor = self.trackmeta[row][3]
            if self.tracks[row].loopstart[col] or col == 0:
                flags = flags | 2
            if self.tracks[row].loopend[col] or col == 7:
                flags = flags | 1
        else:
            active = self.tracks[self.row].clips[self.col].isactive(row, col)
            if self.tracks[self.row].playing == self.col and step == col:
                color = self.trackmeta[self.row][2]
            else:
                color = self.trackmeta[self.row][1]
            bgcolor = self.trackmeta[row][3]
        return active, color, bgcolor, flags

    def click(self, row, col, shift = False):
        if self.arrangerview:
            self.row = row
            self.col = col
            if not shift:
                self.play()
            else:
                self.zoom()
        else:
            return self.tracks[self.row].clips[self.col].click(row, col)

