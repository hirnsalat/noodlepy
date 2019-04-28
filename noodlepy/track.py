from constants import *

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
