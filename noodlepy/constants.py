from pygame import Color

PINK = Color("#f437f5")
WHITE = Color("#ffffff")
OFFCOLOR = PINK
ONCOLOR = WHITE

ticksperstep = 16
stepsperbeat = 4
beatsperpattern = 2
beatsperminute = 120
ticksperbeat = ticksperstep * stepsperbeat
ticksperminute = ticksperbeat * beatsperminute
ticksperpattern = ticksperbeat * beatsperpattern
tickspersecond = ticksperminute // 60

framespersecond = 30
ticksperframe = tickspersecond // framespersecond
mspertick = 60000 // ticksperminute
