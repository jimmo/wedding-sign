from PIL import Image
import math
import sys
b = 0
p = 27*1.35
i = Image.open(sys.argv[1])
for x in range(i.width):
  for y in range(i.height):
    if i.getpixel((x, y,)) in [(0,0,0,255,), (0,0,0,)]:
      print(f'<div class="pixel" style="left:{x*10}px;top:{y*10}px;"></div>')
      b += 1
