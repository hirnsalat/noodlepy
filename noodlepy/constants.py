from pygame import Color

PINK = Color("#f437f5")
NOTPINK = Color("#37f5f4")
ALSONOTPINK = Color("#f5f437")
GREEN = Color("#00ff00")
WHITE = Color("#ffffff")
BLACK = Color("#000000")
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
