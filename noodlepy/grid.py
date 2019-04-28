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

