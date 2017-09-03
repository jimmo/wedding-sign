import pyb
import utime
import math
import micropython

strip = pyb.SPI(1, pyb.SPI.MASTER, baudrate=2000000, crc=None, bits=8, firstbit=pyb.SPI.MSB, phase=1)

def hsv_to_rgb(h, s, v):
  i = int(h * 6)
  f = h * 6 - i
  p = v * (1 - s)
  q = v * (1 - f * s)
  t = v * (1 - (1 - f) * s)

  i = i % 6
  if i == 0:
    return (v, t, p)
  elif i == 1:
    return (q, v, p)
  elif i == 2:
    return (p, v, t)
  elif i == 3:
    return (p, q, v)
  elif i == 4:
    return (t, p, v)
  elif i == 5:
    return (v, p, q)

LEDS = 700
pixeldata = bytearray(LEDS*4 + 8)
for i in range(4):
  pixeldata[i] = 0
  pixeldata[i + LEDS*4] = 0xff

#@micropython.native
#def f(x: int) -> int:
#  return x % int#(7 * x**4 + 11 * x**3 + 29 * x**2 + 3 * x) % LEDS

#@micropython.native
#def pixel(i: int, t: int) -> (int, int, int):
#  return 30, 80, 10

n = 0

@micropython.native
def update(t: int):
  #print('frame')
  buf = pixeldata
  p = int(4)
  s = pyb.millis()
  for i in range(int(LEDS)):
  #  #r, g, b = hsv_to_rgb(((t + i) % 7) / 7, 1, 1)
    #x = int(255* (math.sin(4 * math.pi * f(i) // int(LEDS) + t // 100) + 1) // 2)
    #r = x# if n == 0 else 0
    #b = 0#x if n == 1 else 0
    #g = 0#x if n == 2 else 0
    if i == t % LEDS:
      r = 255
    else:
      r = 0
    if i == (t+200) % LEDS:
      g = 255
    else:
      g = 0
    if i == (t+400) % LEDS:
      b = 255
    else:
      b = 0
    buf[p] = 0b11100000 | 0b00100#int(brightness * 0b11111)
    p += 1
    buf[p] = b
    p += 1
    buf[p] = g
    p += 1
    buf[p] = r
    p += 1
  #print(pyb.elapsed_millis(s))
  s = pyb.millis()
  strip.send(pixeldata)
  #print(pyb.elapsed_millis(s))
  #print('frame')

t = 0

def mode():
  global n
  n = (n + 1) % 3

pyb.Switch().callback(mode)

while True:
  utime.sleep_ms(2)
  update(t)
  t += 1
