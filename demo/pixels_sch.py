from PIL import Image
import math
import sys
i = Image.open(sys.argv[1])
nc = 0
for x in range(i.width):
  sy = -1
  for y in range(i.height):
    if i.getpixel((x, y,)) in [(0,0,0,255,), (0,0,0,)]:
      if sy == -1:
        sy = y
    else:
      if sy >= 0:
        cx = x*600+300
        cy = sy*600+300+(y-sy)*300
        print(f'$Comp')
        print(f'L APA102C_x{y-sy} U?')
        print(f'U 1 1 {nc+0x5954F10D:8X}')
        print(f'P {cx} {cy}')
        print(f'F 0 "U?" H {cx} {cy+250} 60  0000 C CNN')
        print(f'F 1 "APA102C_x{y-sy}" H {cx} {cy-250} 60  0000 C CNN')
        print(f'F 2 "" H {cx} {cy} 60  0001 C CNN')
        print(f'F 3 "" H {cx} {cy} 60  0001 C CNN')
        print(f'\t1\t{cx}\t{cy}')
        print(f'\t0\t1\t1\t0')
        print(f'$EndComp')
        nc += 1
        sy = -1
