import pyb
import hcsr04
import utime
import math
import micropython
import random
import gc

_BRIGHTNESS = const(0b11100100)

_STRIP = pyb.SPI(1, pyb.SPI.MASTER, baudrate=4000000, crc=None, bits=8, firstbit=pyb.SPI.MSB, phase=1)

DISTANCE_SENSORS = [hcsr04.HCSR04(machine.Pin(p), machine.Pin(p)) for p in ('X1', 'X2', 'X3', 'X4')]
closest_distance_sensor = 0

_USER_BUTTON = pyb.Switch()

@micropython.native
def rainbow(h, xbgr):
  # h is hue between 0-119.
  if h < 20:
    xbgr[3] = 255
    xbgr[2] = (h * 255) // 20
    xbgr[1] = 0
  elif h < 40:
    xbgr[3] = ((40-h) * 255) // 20
    xbgr[2] = 255
    xbgr[1] = 0
  elif h < 60:
    xbgr[3] = 0
    xbgr[2] = 255
    xbgr[1] = ((h-40) * 255) // 20
  elif h < 80:
    xbgr[3] = 0
    xbgr[2] = ((80-h) * 255) // 20
    xbgr[1] = 255
  elif h < 100:
    xbgr[3] = ((h-80) * 255) // 20
    xbgr[2] = 0
    xbgr[1] = 255
  else:
    xbgr[3] = 255
    xbgr[2] = 0
    xbgr[1] = ((120-h) * 255) // 20

_LEDS = const(722)
pixeldata = bytearray(4 + _LEDS*4 + 20*4)

RAINBOW_COLORS = []

COORDS_X = b'\x00\x00\x00\x00\x00\x00\x01\x01\x01\x01\x01\x01\x01\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x03\x03\x03\x04\x04\x04\x05\x05\x06\x06\x06\x07\x07\x07\x08\x08\x03\x03\x03\x03\x03\x03\x04\x04\x04\x05\x05\x05\x06\x06\x07\x07\x07\x08\x08\x08\x08\x08\x08\t\t\t\t\t\n\n\x07\x07\x07\x06\x06\x05\x05\x04\x04\x0c\x0c\x0c\x0c\x0c\r\r\r\r\r\r\r\r\r\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0f\x0f\x0f\x10\x10\x10\x11\x11\x12\x12\x12\x13\x13\x13\x13\x13\x13\x13\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x15\x15\x15\x15\x15\x15\x15\x15\x15\x15\x15\x15\x15\x15\x16\x16\x16\x16\x16\x16\x16\x16\x16\x16\x17\x17\x17\x17\x17\x17\x18\x13\x13\x13\x12\x12\x12\x11\x11\x11\x10\x10\x10\x10\x0f\x0f\x0f\x0f\x0f\x19\x19\x19\x19\x19\x1a\x1a\x1a\x1a\x1a\x1a\x1a\x1a\x1a\x1b\x1b\x1b\x1b\x1b\x1b\x1b\x1b\x1b\x1b\x1b\x1c\x1c\x1c\x1d\x1d\x1d\x1e\x1e\x1f\x1f\x1f       !!!!!!!!!!!!""""""""""""""##########$$$$$$%   \x1f\x1f\x1f\x1e\x1e\x1e\x1d\x1d\x1d\x1d\x1c\x1c\x1c\x1c\x1c###$$$$%%%&&&\'\'\'(((((((((((((((()))))))))))))******++++++,,,,,,-------......////00\'\'\'\'\'\'\'\'\'&&\x08\x08\t\t\t\t\t\t\n\n\n\n\x08\x08\x08\x07\x07\x06\x06\x06\x05\x05\x05\x05\x05\x05\x05\x06\x06\x06\x06\x06\x07\x07\x07\x07\x07\x07\x07\x07\x08\x08\x08\x08\x08\t\t\t\t\n\n\n\n\n\n\x0b\x0b\x0b\x0b\x0c\x0c\x0b\x0b\x06\x06\x05\x05\x04\x04\x04\x03\x03\x03\x03\x03\x03\x03\x02\x02\x02\x02\x02\x04\x04\x04\x04\x04\x04\x04\r\r\r\x0e\x0e\x0e\x0e\x0f\x0f\x0f\x10\x10\x10\x11\x11\x11\x11\x12\x12\x12\x12\x12\x12\x12\x12\x12\x13\x13\x13\x13\x13\x13\x13\x13\x13\x13\x13\x13\x13\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x15\x15\x15\x15\x15\x15\x15\x15\x16\x16\x16\x1c\x1c\x1d\x1d\x1d\x1e\x1e\x15\x15\x16\x16\x16\x17\x17\x18\x18\x19\x19\x19\x19\x19\x1a\x1a\x1a\x1a\x1a\x1a\x1a\x1a\x1a\x1a\x1b\x1b\x1b\x1b\x1b\x1b\x1b\x1b\x1b\x1b\x1b\x1b\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1d\x1d\x1d\x1f\x1f     !!!!!!!!!!""""""""""""########$$$%%%&&&\'\'\'\'\'\'\'\'\'&&(((((((((((()))))))))))******++,,,------,............////////////0000000001111'
COORDS_Y = b'\t\n\x0b\x0c\r\x0e\x0f\x0e\r\x0c\x0b\n\t\x08\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x10\x0f\x0e\x0e\x0f\x10\x10\x0f\x0e\x0f\x10\x10\x0f\x0e\x0e\x0f\x0b\n\t\x08\x07\x06\x05\x06\x07\x07\x06\x05\x05\x06\x07\x06\x05\x05\x06\x07\x08\t\n\n\t\x08\x07\x06\x07\x08\t\n\x0b\x0b\n\n\x0b\x0b\n\n\x0b\x0c\r\x0e\x0f\x0e\r\x0c\x0b\n\t\x08\x07\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x10\x0f\x0e\x0e\x0f\x10\x0f\x0e\r\x0e\x0f\x10\x0f\x0e\r\x0c\x0b\n\x10\x0f\x0e\r\x0c\x0b\n\t\x08\x07\x06\x05\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\t\x08\x07\x06\x05\x04\x03\x02\x01\x00\x00\x01\x02\x03\x04\x05\x00\x06\x07\x08\x07\x06\x05\x05\x06\x07\x08\x07\x06\x05\x06\x07\x08\t\n\n\x0b\x0c\r\x0e\x0f\x0e\r\x0c\x0b\n\t\x08\x07\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x10\x0f\x0e\x0e\x0f\x10\x0f\x0e\r\x0e\x0f\x10\x0f\x0e\r\x0c\x0b\n\x10\x0f\x0e\r\x0c\x0b\n\t\x08\x07\x06\x05\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\t\x08\x07\x06\x05\x04\x03\x02\x01\x00\x00\x01\x02\x03\x04\x05\x00\x06\x07\x08\x07\x06\x05\x05\x06\x07\x08\x07\x06\x05\x06\x07\x08\t\n\x12\x13\x14\x15\x14\x13\x12\x13\x14\x15\x15\x14\x13\x12\x13\x14\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08\x07\x06\x05\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x11\x10\x0f\x0e\r\x0c\n\x0b\x0c\r\x0e\x0f\r\x0c\x0b\n\t\x08\x06\x07\x08\t\n\x0b\x0c\n\t\x08\x07\x06\x05\x05\x06\x07\x08\x06\x05\r\x0c\x0b\n\t\x08\x07\x06\x05\x06\x07\x18\x19\x19\x18\x17\x16\x15\x14\x15\x16\x17\x18\x16\x15\x14\x14\x15\x16\x15\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1b\x1a\x19\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f \x1f\x1e\x1d\x1c\x1b\x1d\x1e\x1f  \x1f\x1e\x1d\x1c\x1b\x1a\x1b\x1c\x1d\x1b\x1a\x1f \x1f  \x1f\x1e\x1f  \x1f\x1e\x1d\x1c\x1b\x1a\x1b\x1c\x1d\x1e\x1f\x1c\x1b\x1a\x19\x18\x17\x16%&\'(\'&%&\'((\'&$%&\'\'&%$#"! \x1f\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x1a\x19\x18\x14\x15\x15\x14\x13\x13\x14\x14\x15\x15\x14\x13\x13\x14"##"! \x1f\x1a\x1b\x1c\x1d\x1e\x1f !"##"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x1a\x19\x18"##"! \x1f\x1a\x1b\x1c\x1d\x1e\x1f !"##"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x1c\x1b\x1a\x19\x1a\x1b\x1a\x19\x18\x18\x19\x1a\x1e\x1f !"##"#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18\x18\x19\x1a\x1c\x1c\x1d\x1e\x1f !"\x1e\x1d\x1c\x1b\x1a\x19\x1a\x1b\x1b\x1a\x19\x18\x19\x1a!"###"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x1a\x1b\x1c\x1d'

#INV_COORDS = {}

DIST = bytearray(_LEDS*4)

WAVE = bytearray(256)

@micropython.native
def pixel_blank(t, i, l, xbgr):
  xbgr[1], xbgr[2], xbgr[3] = 0, 0, 0

@micropython.native
def frame_nop(t):
  pass

@micropython.native
def pixel_rainbow_letters(t, i, l, xbgr):
  t = t // 4
  if l == t % 8:
    xbgr[1], xbgr[2], xbgr[3] = RAINBOW_COLORS[t%len(RAINBOW_COLORS)]
  else:
    xbgr[1], xbgr[2], xbgr[3] = xbgr[1]*5//6, xbgr[2]*5//6, xbgr[3]*5//6

@micropython.native
def pixel_fire(t, i, l, xbgr):
  i = (t + i) % 13827
  xbgr[3] = (i * 37 + i * i * 17 + i) % 200
  xbgr[2] = (i * 61 + i * i * 31 + i) % (1+xbgr[3]//2)
  xbgr[1] = 0

@micropython.native
def pixel_red_sparkle(t, i, l, xbgr):
  x = COORDS_X[i]
  xbgr[3], xbgr[2], xbgr[1] = 2 * WAVE[(t*10 + i*400) % len(WAVE)] * HEAT_X2[x] // 128, 0, 0
  #xbgr[3], xbgr[2], xbgr[1] = 2 * WAVE[(t*10 + i*400) % len(WAVE)], 0, 0

@micropython.native
def pixel_green_sparkle(t, i, l, xbgr):
  x = COORDS_X[i]
  xbgr[3], xbgr[2], xbgr[1] = 0, 2 * WAVE[(t*10 + i*400) % len(WAVE)] * HEAT_X2[x] // 128, 0

@micropython.native
def pixel_blue_sparkle(t, i, l, xbgr):
  x = COORDS_X[i]
  xbgr[3], xbgr[2], xbgr[1] = 0, 0, 2 * WAVE[(t*10 + i*400) % len(WAVE)] * HEAT_X2[x] // 128

@micropython.native
def pixel_scan(t, i, l, xbgr):
  xbgr[1], xbgr[2], xbgr[3] = 0, 0, 0
  x, y = COORDS_X[i], COORDS_Y[i]
  for i in range(0, 50, 10):
    if x == t%40:
      xbgr[3] = 255
    if y == t%50:
      xbgr[2] = 255
    t += 10

@micropython.native
def pixel_wave_green(t, i, l, xbgr):
  xbgr[1], xbgr[2], xbgr[3] = 0, WAVE[(t*10 + DIST[i+_LEDS*closest_distance_sensor]*2) % len(WAVE)], 0

@micropython.native
def pixel_rainbow_x(t, i, l, xbgr):
  h = t*2 + COORDS_X[i]
  if l < 4:
    rainbow(h % 120, xbgr)
  else:
    rainbow((h+60) % 120, xbgr)

prev_l = -1

@micropython.native
def pixel_distance(t, i, l, xbgr):
  global prev_l
  xbgr[1], xbgr[2], xbgr[3] = 0, 0, 0
  if l == prev_l:
    return

  prev_l = l
  if closest_distance_sensor == l:
    xbgr[2] = 255

LINE_COORDS = bytearray([0,40,50,0])

@micropython.native
def pixel_line(t, i, l, xbgr):
  x, y = COORDS_X[i], COORDS_Y[i]
  d = (x - LINE_COORDS[0])*(LINE_COORDS[3] - LINE_COORDS[1]) - (y - LINE_COORDS[1])*(LINE_COORDS[2] - LINE_COORDS[0])
  if d < 0:
    xbgr[1], xbgr[2], xbgr[3] = CURRENT_COLOUR1[1], CURRENT_COLOUR1[2], CURRENT_COLOUR1[3]
  else:
    xbgr[1], xbgr[2], xbgr[3] = CURRENT_COLOUR2[1], CURRENT_COLOUR2[2], CURRENT_COLOUR2[3]

@micropython.native
def frame_line(t):
  if t == 0:
    rainbow(random.randint(0,119), CURRENT_COLOUR1)
    rainbow(random.randint(0,119), CURRENT_COLOUR2)
  if LINE_COORDS[0] == 0 and LINE_COORDS[1] > 0:
    LINE_COORDS[1] -= 2
    LINE_COORDS[3] += 2
  if LINE_COORDS[1] == 0 and LINE_COORDS[0] < 50:
    LINE_COORDS[0] += 2
    LINE_COORDS[2] -= 2
  if LINE_COORDS[0] == 50 and LINE_COORDS[1] < 40:
    LINE_COORDS[1] += 2
    LINE_COORDS[3] -= 2
  if LINE_COORDS[1] == 40 and LINE_COORDS[0] > 0:
    LINE_COORDS[0] -= 2
    LINE_COORDS[2] += 2

CIRCLES = []
CURRENT_COLOUR1 = bytearray(b'\x00\x00\x00\xff')
CURRENT_COLOUR2 = bytearray(b'\x00\x00\xff\x00')

@micropython.native
def pixel_circles(t, i, l, xbgr):
  x, y = COORDS_X[i], COORDS_Y[i]
  for cx, cy, cr2, h in CIRCLES:
    if (cx-x)**2 + (cy-y)**2 < cr2:
      rainbow(h, xbgr)

@micropython.native
def frame_circles(t):
  while len(CIRCLES) > 1:
    CIRCLES.pop(0)
  CIRCLES.append((random.randint(0, 50), random.randint(0, 40), random.randint(20, 40), random.randint(0, 119),))

@micropython.native
def pixel_flash(t, i, l, xbgr):
  if t in (0, 5, 15, 18, 40, 43, 47) or t > 55:
    xbgr[1], xbgr[2], xbgr[3] = random.randint(0,1)*255, random.randint(0,1)*255, random.randint(0,1)*255
  else:
    xbgr[1], xbgr[2], xbgr[3] = 0, 0, 0

@micropython.native
def pixel_pulse(t, i, l, xbgr):
  x = WAVE[(t*4)%len(WAVE)]
  xbgr[1], xbgr[2], xbgr[3] = CURRENT_COLOUR1[1] * x // 128, CURRENT_COLOUR1[2] * x // 128, CURRENT_COLOUR1[3] * x // 128

@micropython.native
def pixel_rain(t, i, l, xbgr):
  x, y = COORDS_X[i], COORDS_Y[i]
  xbgr[1], xbgr[2], xbgr[3] = 0, 0, 0
  for j in range(3):
    d = (x * 37 + j*(x**3*23) + x + t - y) % 40
    if d < 8:
      xbgr[1] = max(xbgr[1], CURRENT_COLOUR1[1] // (1<<d))
      xbgr[2] = max(xbgr[2], CURRENT_COLOUR1[2] // (1<<d))
      xbgr[3] = max(xbgr[3], CURRENT_COLOUR1[3] // (1<<d))

@micropython.native
def frame_pulse(t):
  if t % 64 == 0:
    rainbow(random.randint(0,119), CURRENT_COLOUR1)

@micropython.native
def frame_rain(t):
  if t == 0:
    rainbow(random.randint(0,119), CURRENT_COLOUR1)

HEAT_X = bytearray(50)
HEAT_X2 = bytearray(50)

@micropython.native
def pixel_heat(t, i, l, xbgr):
  x = COORDS_X[i]
  xbgr[1] = HEAT_X[x]
  xbgr[3] = 255-HEAT_X[x]

@micropython.native
def lerp(x, x1, x2, y1, y2):
  return y1 + (y2-y1) * (x - x1) // (x2 - x1)

NORMALIZED_DISTANCE = [0]*4

@micropython.native
def frame_heat(t):
  for i in range(4):
    NORMALIZED_DISTANCE[i] = DISTANCE_SENSORS[i].mm
  dmin = min(500, min(NORMALIZED_DISTANCE))
  dmax = max(1500, max(NORMALIZED_DISTANCE))
  r = dmax - dmin
  if r == 0:
    for i in range(len(HEAT_X)):
      HEAT_X[i] = 0
    return
  for i in range(4):
    NORMALIZED_DISTANCE[i] = (NORMALIZED_DISTANCE[i] - dmin) * 255 // r

  for i in range(17):
    HEAT_X[i] = (HEAT_X[i] + lerp(i, 0, 17, NORMALIZED_DISTANCE[0], NORMALIZED_DISTANCE[1])) // 2
  for i in range(17, 33):
    HEAT_X[i] = (HEAT_X[i] + lerp(i, 17, 33, NORMALIZED_DISTANCE[1], NORMALIZED_DISTANCE[2])) // 2
  for i in range(33, 50):
    HEAT_X[i] = (HEAT_X[i] + lerp(i, 33, 50, NORMALIZED_DISTANCE[2], NORMALIZED_DISTANCE[3])) // 2
  for i in range(len(HEAT_X)):
    HEAT_X2[i] = max(50, 255-HEAT_X[i])

@micropython.native
def pixel_fade_dissolve(t, i, l, xbgr):
  if random.randint(0, 16) == 0:
    xbgr[1], xbgr[2], xbgr[3] = 0, 0, 0

@micropython.native
def pixel_fade_swipe_down(t, i, l, xbgr):
  if COORDS_Y[i] < t*2:
    xbgr[1], xbgr[2], xbgr[3] = 0, 0, 0

@micropython.native
def pixel_fade_swipe_up(t, i, l, xbgr):
  if COORDS_Y[i] > 40-t*2:
    xbgr[1], xbgr[2], xbgr[3] = 0, 0, 0

@micropython.native
def pixel_fade_swipe_left(t, i, l, xbgr):
  if COORDS_X[i] > 50-t*2:
    xbgr[1], xbgr[2], xbgr[3] = 0, 0, 0

@micropython.native
def pixel_fade_swipe_right(t, i, l, xbgr):
  if COORDS_X[i] < t*2:
    xbgr[1], xbgr[2], xbgr[3] = 0, 0, 0

@micropython.native
def pixel_fade_fade(t, i, l, xbgr):
  xbgr[1], xbgr[2], xbgr[3] = xbgr[1]//2, xbgr[2]//2, xbgr[3]//2

LETTER_INDEXES = [
  (80,  1,), # e
  (184, 2,), # d
  (288, 3,), # d
  (381, 4,), # y
  (470, 5,), # &
  (533, 6,), # j
  (540, 5,), # i.
  (547, 6,), # j.
  (587, 7,), # i
  (722, 0),  # m
]

NUM_MODES = const(12)

MODES = [
  (pixel_rainbow_letters, frame_nop, 35, 30000, False,),
  (pixel_fire, frame_nop, 35, 30000, False,),
  (pixel_red_sparkle, frame_heat, 35, 30000, True,),
  (pixel_green_sparkle, frame_heat, 35, 30000, True,),
  (pixel_blue_sparkle, frame_heat, 35, 30000, True,),
  (pixel_rain, frame_rain, 35, 30000, False,),
  (pixel_wave_green, frame_nop, 35, 30000, True,),
  (pixel_rainbow_x, frame_nop, 35, 30000, False,),
  (pixel_line, frame_line, 35, 30000, False,),
  (pixel_circles, frame_circles, 35, 30000, False,),
  (pixel_pulse, frame_pulse, 35, 30000, False,),
  (pixel_heat, frame_heat, 35, 30000, True,),

  (pixel_fade_dissolve, frame_nop, 0, 2000, False,),
  (pixel_fade_swipe_down, frame_nop, 0, 2000, False,),
  (pixel_fade_swipe_up, frame_nop, 0, 2000, False,),
  (pixel_fade_swipe_left, frame_nop, 0, 2000, False,),
  (pixel_fade_swipe_right, frame_nop, 0, 2000, False,),
  (pixel_fade_fade, frame_nop, 0, 2000, False,),
]

advance_mode = False
mode_index = 0

def on_switch():
  global advance_mode
  advance_mode = True

_USER_BUTTON.callback(on_switch)

@micropython.native
def update(t: int):
  #gc.disable()
  gc.collect()
  p = 4
  s = utime.ticks_ms()
  l = 0
  li = 0
  ln = LETTER_INDEXES[li][0]
  mode_pixel = MODES[mode_index][0]
  m = memoryview(pixeldata)
  for i in range(_LEDS):
    if i == ln:
      l = LETTER_INDEXES[li][1]
      li = (li + 1) % len(LETTER_INDEXES)
      ln = LETTER_INDEXES[li][0]
    mode_pixel(t, i, l, m[p:p+4])
    p += 4
  n = utime.ticks_diff(utime.ticks_ms(), s)
  #gc.enable()
  _STRIP.send(pixeldata)
  #print(n)

def clear():
  buf = pixeldata
  p = 4
  for i in range(_LEDS):
    buf[p] = _BRIGHTNESS
    p += 1
    buf[p] = 0
    p += 1
    buf[p] = 0
    p += 1
    buf[p] = 0
    p += 1
  _STRIP.send(pixeldata)

def vert(x):
  buf = pixeldata
  p = 4
  for i in range(_LEDS):
    buf[p] = _BRIGHTNESS
    p += 1
    buf[p] = 255 if COORDS_X[i] == x else 0
    p += 1
    buf[p] = 0
    p += 1
    buf[p] = 0
    p += 1
  _STRIP.send(pixeldata)

def horiz(y):
  buf = pixeldata
  p = 4
  for i in range(_LEDS):
    buf[p] = _BRIGHTNESS
    p += 1
    buf[p] = 255 if COORDS_Y[i] == y else 0
    p += 1
    buf[p] = 0
    p += 1
    buf[p] = 0
    p += 1
  _STRIP.send(pixeldata)

@micropython.native
def main():
  global closest_distance_sensor, mode_index, advance_mode
  for i in range(4):
    pixeldata[i] = 0
    for j in range(20):
      pixeldata[_LEDS*4 + j*4 + i] = 0xff

  p = 4
  for i in range(_LEDS):
    x,y = COORDS_X[i], COORDS_Y[i]
    #INV_COORDS[(x,y)] = i
    DIST[i] = int((x**2 + y**2)**0.5 * 20)
    DIST[i+_LEDS] = int(((x-17)**2 + y**2)**0.5 * 20)
    DIST[i+_LEDS*2] = int(((x-33)**2 + y**2)**0.5 * 20)
    DIST[i+_LEDS*3] = int(((x-50)**2 + y**2)**0.5 * 20)
    pixeldata[p] = _BRIGHTNESS
    p += 4

  for i in range(7):
    xbgr = [0, 0, 0, 0]
    rainbow(i * 120 // 7, xbgr)
    RAINBOW_COLORS.append(xbgr[1:])

  for i in range(len(WAVE)):
    WAVE[i] = int(32 * (1 + math.sin(math.pi * 2 * i / len(WAVE) - math.pi/2)))

  mode_time = utime.ticks_ms()
  mode_time_limit = MODES[mode_index][3]

  mode_index_last_pixel = mode_index
  mode_index_last_fade = -1

  t = 0
  di = 0
  while True:
    s = utime.ticks_ms()

    if MODES[mode_index][4]:
      DISTANCE_SENSORS[di].update()
      if DISTANCE_SENSORS[di].mm < DISTANCE_SENSORS[closest_distance_sensor].mm:
        closest_distance_sensor = di
      di = (di + 1) % len(DISTANCE_SENSORS)

    if utime.ticks_diff(utime.ticks_ms(), mode_time) > mode_time_limit or (advance_mode and not _USER_BUTTON.value()):
      if not advance_mode and mode_index < NUM_MODES:
        # Currently pixel, move to fade.
        while True:
          mode_index = random.randint(NUM_MODES, len(MODES)-1)
          if mode_index != mode_index_last_fade:
            break
        mode_index_last_fade = mode_index
      else:
        # Fade moving to pixel.
        while True:
          mode_index = random.randint(0, NUM_MODES-1)
          if mode_index != mode_index_last_pixel:
            break
        mode_index_last_pixel = mode_index
        clear()
      advance_mode = False
      mode_time = utime.ticks_ms()
      mode_time_limit = MODES[mode_index][3]
      t = 0

    MODES[mode_index][1](t)
    update(t)
    t += 1
    n = utime.ticks_diff(utime.ticks_ms(), s)
    utime.sleep_ms(max(1, MODES[mode_index][2] - n - 1))
    n = utime.ticks_diff(utime.ticks_ms(), s)
    #print(n)

main()
