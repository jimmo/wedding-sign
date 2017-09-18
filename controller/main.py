import pyb
import hcsr04
import utime
import math
import micropython
import random
import gc

strip = pyb.SPI(1, pyb.SPI.MASTER, baudrate=4000000, crc=None, bits=8, firstbit=pyb.SPI.MSB, phase=1)

DISTANCE_SENSORS = [hcsr04.HCSR04(machine.Pin(p), machine.Pin(p)) for p in ('X1', 'X2', 'X3', 'X4')]
closest_distance_sensor = 0

@micropython.native
def rainbow(h, xbgr):
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

COORDS_X = bytearray(b'\x00\x00\x00\x00\x00\x00\x01\x01\x01\x01\x01\x01\x01\x01\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x03\x03\x03\x04\x04\x04\x05\x05\x06\x06\x06\x07\x07\x07\x08\x08\x03\x03\x03\x03\x03\x03\x04\x04\x04\x05\x05\x05\x06\x06\x07\x07\x07\x08\x08\x08\x08\x08\x08\t\t\t\t\t\n\n\x07\x07\x07\x06\x06\x05\x05\x04\x04\x0c\x0c\x0c\x0c\x0c\r\r\r\r\r\r\r\r\r\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0f\x0f\x0f\x10\x10\x10\x11\x11\x12\x12\x12\x13\x13\x13\x13\x13\x13\x13\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x15\x15\x15\x15\x15\x15\x15\x15\x15\x15\x15\x15\x15\x15\x16\x16\x16\x16\x16\x16\x16\x16\x16\x16\x17\x17\x17\x17\x17\x17\x18\x13\x13\x13\x12\x12\x12\x11\x11\x11\x10\x10\x10\x10\x0f\x0f\x0f\x0f\x0f\x19\x19\x19\x19\x19\x1a\x1a\x1a\x1a\x1a\x1a\x1a\x1a\x1a\x1b\x1b\x1b\x1b\x1b\x1b\x1b\x1b\x1b\x1b\x1b\x1c\x1c\x1c\x1d\x1d\x1d\x1e\x1e\x1f\x1f\x1f       !!!!!!!!!!!!""""""""""""""##########$$$$$$%   \x1f\x1f\x1f\x1e\x1e\x1e\x1d\x1d\x1d\x1d\x1c\x1c\x1c\x1c\x1c###$$$$%%%&&&\'\'\'(((((((((((((((()))))))))))))******++++++,,,,,,-------......////00\'\'\'\'\'\'\'\'\'&&\x08\x08\t\t\t\t\t\t\n\n\n\n\x08\x08\x08\x07\x07\x06\x06\x06\x05\x05\x05\x05\x05\x05\x05\x06\x06\x06\x06\x06\x07\x07\x07\x07\x07\x07\x07\x07\x08\x08\x08\x08\x08\t\t\t\t\n\n\n\n\n\n\x0b\x0b\x0b\x0b\x0c\x0c\x0b\x0b\x06\x06\x05\x05\x04\x04\x04\x03\x03\x03\x03\x03\x03\x03\x02\x02\x02\x02\x02\x04\x04\x04\x04\x04\x04\x04\r\r\r\x0e\x0e\x0e\x0e\x0f\x0f\x0f\x10\x10\x10\x11\x11\x11\x11\x12\x12\x12\x12\x12\x12\x12\x12\x12\x13\x13\x13\x13\x13\x13\x13\x13\x13\x13\x13\x13\x13\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x15\x15\x15\x15\x15\x15\x15\x15\x16\x16\x16\x1c\x1c\x1d\x1d\x1d\x1e\x1e\x15\x15\x16\x16\x16\x17\x17\x18\x18\x19\x19\x19\x19\x19\x1a\x1a\x1a\x1a\x1a\x1a\x1a\x1a\x1a\x1a\x1b\x1b\x1b\x1b\x1b\x1b\x1b\x1b\x1b\x1b\x1b\x1b\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1d\x1d\x1d\x1f\x1f     !!!!!!!!!!""""""""""""########$$$%%%&&&\'\'\'\'\'\'\'\'\'&&(((((((((((()))))))))))******++,,,------,............////////////0000000001111')
COORDS_Y = bytearray(b'\t\n\x0b\x0c\r\x0e\x0f\x0e\r\x0c\x0b\n\t\x08\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x10\x0f\x0e\x0e\x0f\x10\x10\x0f\x0e\x0f\x10\x10\x0f\x0e\x0e\x0f\x0b\n\t\x08\x07\x06\x05\x06\x07\x07\x06\x05\x05\x06\x07\x06\x05\x05\x06\x07\x08\t\n\n\t\x08\x07\x06\x07\x08\t\n\x0b\x0b\n\n\x0b\x0b\n\n\x0b\x0c\r\x0e\x0f\x0e\r\x0c\x0b\n\t\x08\x07\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x10\x0f\x0e\x0e\x0f\x10\x0f\x0e\r\x0e\x0f\x10\x0f\x0e\r\x0c\x0b\n\x10\x0f\x0e\r\x0c\x0b\n\t\x08\x07\x06\x05\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\t\x08\x07\x06\x05\x04\x03\x02\x01\x00\x00\x01\x02\x03\x04\x05\x00\x06\x07\x08\x07\x06\x05\x05\x06\x07\x08\x07\x06\x05\x06\x07\x08\t\n\n\x0b\x0c\r\x0e\x0f\x0e\r\x0c\x0b\n\t\x08\x07\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x10\x0f\x0e\x0e\x0f\x10\x0f\x0e\r\x0e\x0f\x10\x0f\x0e\r\x0c\x0b\n\x10\x0f\x0e\r\x0c\x0b\n\t\x08\x07\x06\x05\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\t\x08\x07\x06\x05\x04\x03\x02\x01\x00\x00\x01\x02\x03\x04\x05\x00\x06\x07\x08\x07\x06\x05\x05\x06\x07\x08\x07\x06\x05\x06\x07\x08\t\n\x12\x13\x14\x15\x14\x13\x12\x13\x14\x15\x15\x14\x13\x12\x13\x14\x14\x13\x12\x11\x10\x0f\x0e\r\x0c\x0b\n\t\x08\x07\x06\x05\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x11\x10\x0f\x0e\r\x0c\n\x0b\x0c\r\x0e\x0f\r\x0c\x0b\n\t\x08\x06\x07\x08\t\n\x0b\x0c\n\t\x08\x07\x06\x05\x05\x06\x07\x08\x06\x05\r\x0c\x0b\n\t\x08\x07\x06\x05\x06\x07\x18\x19\x19\x18\x17\x16\x15\x14\x15\x16\x17\x18\x16\x15\x14\x14\x15\x16\x15\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1b\x1a\x19\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f \x1f\x1e\x1d\x1c\x1b\x1d\x1e\x1f  \x1f\x1e\x1d\x1c\x1b\x1a\x1b\x1c\x1d\x1b\x1a\x1f \x1f  \x1f\x1e\x1f  \x1f\x1e\x1d\x1c\x1b\x1a\x1b\x1c\x1d\x1e\x1f\x1c\x1b\x1a\x19\x18\x17\x16%&\'(\'&%&\'((\'&$%&\'\'&%$#"! \x1f\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&$#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x1a\x19\x18\x14\x15\x15\x14\x13\x13\x14\x14\x15\x15\x14\x13\x13\x14"##"! \x1f\x1a\x1b\x1c\x1d\x1e\x1f !"##"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x1a\x19\x18"##"! \x1f\x1a\x1b\x1c\x1d\x1e\x1f !"##"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x1c\x1b\x1a\x19\x1a\x1b\x1a\x19\x18\x18\x19\x1a\x1e\x1f !"##"#"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18\x18\x19\x1a\x1c\x1c\x1d\x1e\x1f !"\x1e\x1d\x1c\x1b\x1a\x19\x1a\x1b\x1b\x1a\x19\x18\x19\x1a!"###"! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x18\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#! \x1f\x1e\x1d\x1c\x1b\x1a\x19\x1a\x1b\x1c\x1d')

INV_COORDS = {}

DIST = bytearray(_LEDS)

WAVE = bytearray(256)

@micropython.native
def mode_blank(t, i, l, xbgr):
  xbgr[1], xbgr[2], xbgr[3] = 0, 0, 0

@micropython.native
def mode_rainbow_letters(t, i, l, xbgr):
  if l == t % 8:
    xbgr[1], xbgr[2], xbgr[3] = RAINBOW_COLORS[t%len(RAINBOW_COLORS)]
  else:
    xbgr[1], xbgr[2], xbgr[3] = 0, 0, 0

@micropython.native
def mode_fire(t, i, l, xbgr):
  i = (t + i) % 13827
  xbgr[3] = (i * 37 + i * i * 17 + i) % 200
  xbgr[2] = (i * 61 + i * i * 31 + i) % (1+xbgr[3]//2)
  xbgr[1] = 0

@micropython.native
def mode_green_sparkle(t, i, l, xbgr):
  xbgr[3], xbgr[2], xbgr[1] = 0, WAVE[(t*10 + i*400) % len(WAVE)], 0

@micropython.native
def mode_scan(t, i, l, xbgr):
  xbgr[1], xbgr[2], xbgr[3] = 0, 0, 0
  if COORDS_Y[i] == t%41:
    xbgr[3] = 255
  if COORDS_X[i] == t%50:
    xbgr[2] = 255

@micropython.native
def mode_wave(t, i, l, xbgr):
  xbgr[1], xbgr[2], xbgr[3] = 0, WAVE[(t + DIST[i]) % len(WAVE)], 0

@micropython.native
def mode_rainbow_x(t, i, l, xbgr):
  h = t*2 + COORDS_X[i]
  rainbow(h % 120, xbgr)

prev_l = -1

@micropython.native
def mode_distance(t, i, l, xbgr):
  global prev_l
  xbgr[1], xbgr[2], xbgr[3] = 0, 0, 0
  if l == prev_l:
    return

  prev_l = l
  if closest_distance_sensor == l:
    xbgr[2] = 255

CIRCLES = []

@micropython.native
def mode_circles(t, i, l, xbgr):
  x, y = COORDS_X[i], COORDS_Y[i]
  for cx, cy, cr2, h in CIRCLES:
    if (cx-x)**2 + (cy-y)**2 < cr2:
      rainbow(h, xbgr)

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

MODES = [
  mode_blank,
  mode_rainbow_letters,
  mode_fire,
  mode_green_sparkle,
  mode_scan,
  mode_wave,
  mode_rainbow_x,
  mode_distance,
  mode_circles,
]

MODE_DELAYS = [
  100,
  5,
  5,
  5,
  5,
  5,
  5,
  5,
  5,
  5,
]

mode_index = 8

def next_mode():
  global mode_index
  mode_index = (mode_index + 1) % len(MODES)

pyb.Switch().callback(next_mode)

@micropython.native
def update(t: int):
  gc.disable()
  gc.collect()
  p = 4
  s = pyb.millis()
  l = 0
  li = 0
  ln = LETTER_INDEXES[li][0]
  current_mode = MODES[mode_index]
  m = memoryview(pixeldata)
  for i in range(_LEDS):
    if i == ln:
      l = LETTER_INDEXES[li][1]
      li = (li + 1) % len(LETTER_INDEXES)
      ln = LETTER_INDEXES[li][0]
    current_mode(t, i, l, m[p:p+4])
    p += 4
  n = pyb.elapsed_millis(s)
  gc.enable()
  strip.send(pixeldata)
  print(n)

def clear():
  buf = pixeldata
  p = 4
  for i in range(_LEDS):
    buf[p] = 0b11100000
    p += 1
    buf[p] = 0
    p += 1
    buf[p] = 0
    p += 1
    buf[p] = 0
    p += 1
  strip.send(pixeldata)

def vert(x):
  buf = pixeldata
  p = 4
  for i in range(_LEDS):
    buf[p] = 0b11101000
    p += 1
    buf[p] = 255 if COORDS_X[i] == x else 0
    p += 1
    buf[p] = 0
    p += 1
    buf[p] = 0
    p += 1
  strip.send(pixeldata)

def horiz(y):
  buf = pixeldata
  p = 4
  for i in range(_LEDS):
    buf[p] = 0b11101000
    p += 1
    buf[p] = 255 if COORDS_Y[i] == y else 0
    p += 1
    buf[p] = 0
    p += 1
    buf[p] = 0
    p += 1
  strip.send(pixeldata)

@micropython.native
def main():
  global closest_distance_sensor
  for i in range(4):
    pixeldata[i] = 0
    for j in range(20):
      pixeldata[_LEDS*4 + j*4 + i] = 0xff

  p = 4
  for i in range(_LEDS):
    x,y = COORDS_X[i], COORDS_Y[i]
    INV_COORDS[(x,y)] = i
    DIST[i] = int((x**2 + y**2)**0.5 * 20)
    pixeldata[p] = 0b11100000 | 0b00100
    p += 4

  for i in range(7):
    xbgr = [0, 0, 0, 0]
    rainbow(i * 120 // 7, xbgr)
    RAINBOW_COLORS.append(xbgr[1:])

  for i in range(len(WAVE)):
    WAVE[i] = int(64 * (1 + math.sin(math.pi * 2 * i / len(WAVE))))

  t = 0
  di = 0
  while True:
    DISTANCE_SENSORS[di].update()
    if DISTANCE_SENSORS[di].mm < DISTANCE_SENSORS[closest_distance_sensor].mm:
      closest_distance_sensor = di
    di = (di + 1) % len(DISTANCE_SENSORS)

    if mode_index == 8:
      while len(CIRCLES) > 1:
        CIRCLES.pop(0)
      CIRCLES.append((random.randint(0, 50), random.randint(0, 40), random.randint(20, 40), random.randint(0, 120),))

    utime.sleep_ms(MODE_DELAYS[mode_index])
    update(t)
    t += 1

main()
