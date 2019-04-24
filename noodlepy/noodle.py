import sys
import pygame
import pygame.midi
import pygame.time
import pygame.freetype
from pygame.locals import *

from timing import Timekeeper
from clip import NoteClip, Row
from constants import *

print(f"ticksperbeat: {ticksperbeat}")
print(f"tickspersecond: {tickspersecond}")
print(f"framespersecond: {framespersecond}")
print(f"ticksperframe: {ticksperframe}")

pygame.init()
pygame.midi.init()

port = pygame.midi.get_default_output_id()

midi_out = pygame.midi.Output(port, latency = 1)
clock = pygame.time.Clock()
screen = pygame.display.set_mode([640,480], pygame.RESIZABLE)
time = Timekeeper(midi_out)

font = pygame.freetype.SysFont("Anonymous Pro", 32)
print(font)
print(font.get_sizes())
textsurf = font.render("test test uasd", ONCOLOR)

#the_row = Row(lambda: NoteClip(0, [36,37,38,42]))
the_row = Row(lambda: NoteClip(0, [36,37,38,39]))

time.add_listener(the_row)

activeclip = the_row

def handle_key(event, clip):
    sc = event.scancode
    if 10 <= sc <= 17:
        clip.click(0,sc - 10)
    elif 24 <= sc <= 31:
        clip.click(1,sc - 24)
    elif 38 <= sc <= 45:
        clip.click(2,sc - 38)
    elif 52 <= sc <= 59:
        clip.click(3,sc - 52)
    elif sc == 113:
        clip.left()
    elif sc == 114:
        clip.right()
    elif sc == 65:
        clip.play()
    elif sc == 95:
        clip.toggle_start()
    elif sc == 96:
        clip.toggle_end()
    # L 113, R 114, U 111, D 116
    else:
        print(sc)

def drawframe(screen, time, clip, title):
    brightness = (ticksperstep*2) - time.inbeat
    brightness *= 2
    if brightness < 0:
        brightness = 0
    screen.fill([brightness, brightness, brightness])
    screen.blit(title[0], (16,16))

    vis = clip.visual()

    for row in range(0,4):
        for col in range(0,8):
            # the next two steps should probably go into the clip
            # maybe figure out if active step is in the clip and pass that to visual()?
            if time.step == col and clip.visible == clip.playing:
                color = ONCOLOR # TODO make pink
            else:
                color = OFFCOLOR
            if vis[row][col]:
                width = 0
            else:
                width = 1
            pygame.draw.rect(screen, color, Rect(8+80*col,168+80*row,64,64), width)
    pygame.display.flip()

try:
    time.first_frame()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type == pygame.KEYDOWN: handle_key(event, activeclip)
            #else: print(event)

        textsurf = font.render(f"DRUM {activeclip.visible}", ONCOLOR)
        drawframe(screen, time, activeclip, textsurf)

        time.to_next_frame()

        clock.tick(framespersecond)
        #print(clock.get_fps())
finally:
    for i in range(0,127):
        midi_out.note_off(i)
    midi_out.close()
    del midi_out
    pygame.midi.quit()
