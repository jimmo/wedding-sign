from PIL import Image
import datetime
from collections import defaultdict
import math
import sys
i = Image.open(sys.argv[1])
nc = 1
t = int(datetime.datetime.now().timestamp())
tx = '{:08X}'.format(t)
W = 1000/72

def is_led(xx, yy):
  return i.getpixel((xx, yy,)) in [(0,0,0,255,), (0,0,0,)]

cc = defaultdict(lambda: (set(), set()))

for x in range(i.width):
  sy = -1
  for y in range(i.height):
    if is_led(x, y):
      cc[(x,y)][1].update(range(0, 12))

      cc[(x-1,y)][0].update((1, 9, 4))
      cc[(x-1,y)][1].update((2, 3,))

      cc[(x-1,y-1)][0].update((3, 4))
      cc[(x-1,y-1)][1].update()

      cc[(x,y-1)][0].update((6, 10, 3))
      cc[(x,y-1)][1].update((5, 4,))

      cc[(x+1,y-1)][0].update((6, 5))
      cc[(x+1,y-1)][1].update()

      cc[(x+1,y)][0].update((0, 11, 5))
      cc[(x+1,y)][1].update((7, 6,))

      cc[(x+1,y+1)][0].update((0, 7))
      cc[(x+1,y+1)][1].update()

      cc[(x,y+1)][0].update((7, 8, 2))
      cc[(x,y+1)][1].update((0, 1,))

      cc[(x-1,y+1)][0].update((1, 2))
      cc[(x-1,y+1)][1].update()

M = 2
for y in range(i.height):
  row = []
  for x in range(i.width):
    k, r = cc[(x,y)]

    cx = x*W+10-W/2
    cy = y*W+10
    for e in k - r:
      if e == 0:
        sx, sy, fx, fy = cx + M, cy, cx + M, cy + M
      if e == 1:
        sx, sy, fx, fy = cx + W - M, cy, cx + W - M, cy + M
      if e == 2:
        sx, sy, fx, fy = cx + W - M, cy + M, cx + W, cy + M
      if e == 3:
        sx, sy, fx, fy = cx + W - M, cy + W - M, cx + W, cy + W - M
      if e == 4:
        sx, sy, fx, fy = cx + W - M, cy + W - M, cx + W - M, cy + W
      if e == 5:
        sx, sy, fx, fy = cx + M, cy + W - M, cx + M, cy + W
      if e == 6:
        sx, sy, fx, fy = cx, cy + W - M, cx + M, cy + W - M
      if e == 7:
        sx, sy, fx, fy = cx, cy + M, cx + M, cy + M
      if e == 8:
        sx, sy, fx, fy = cx + M, cy + M, cx + W - M, cy + M
      if e == 9:
        sx, sy, fx, fy = cx + W - M, cy + M, cx + W - M, cy + W - M
      if e == 10:
        sx, sy, fx, fy = cx + M, cy + W - M, cx + W - M, cy + W - M
      if e == 11:
        sx, sy, fx, fy = cx + M, cy + M, cx + M, cy + W - M

      print(f'  (gr_line (start {sx:.4f} {sy:.4f}) (end {fx:.4f} {fy:.4f}) (layer Edge.Cuts) (width 0.15))')
    #n = len(k - r)
    #row.append(' ' if n == 0 else str(n))
  print(''.join(row))
