from PIL import Image
import math
import sys
b = 0
p = 48*1.35/5
i = Image.open(sys.argv[1])
for x in range(i.width):
  for y in range(i.height):
    if i.getpixel((x, y,)) in [(0,0,0,255,), (0,0,0,)]:
      b += 1
print(b, i.width*i.height)
print(math.ceil(b/60)*p, b*0.02)
