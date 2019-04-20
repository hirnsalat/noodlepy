from pygame import Color


ONCOLOR = Color("#f437f5")
OFFCOLOR = Color("#ffffff")

ticksperstep = 16
stepsperbeat = 4
beatsperpattern = 4
beatsperminute = 120
ticksperbeat = ticksperstep * stepsperbeat
ticksperminute = ticksperbeat * beatsperminute
ticksperpattern = ticksperbeat * beatsperpattern
tickspersecond = ticksperminute // 60

framespersecond = 30
ticksperframe = tickspersecond // framespersecond
mspertick = 60000 // ticksperminute
