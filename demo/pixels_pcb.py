from PIL import Image
import datetime
import math
import sys
i = Image.open(sys.argv[1])
nc = 1
t = int(datetime.datetime.now().timestamp())
tx = '{:08X}'.format(t)
w = 1000/72
for x in range(i.width):
  sy = -1
  for y in range(i.height):
    if i.getpixel((x, y,)) in [(0,0,0,255,), (0,0,0,)]:
      if sy == -1:
        sy = y
    else:
      if sy >= 0:
        cx = x*w+10
        n = y-sy
        w2 = w*n/2
        cy = sy*w+10+w2
        print(f'  (module apa102c_72m:APA102C_72m_x{n} (layer B.Cu) (tedit {tx}) (tstamp {tx})')
        print(f'    (at {cx:.4f} {cy:.4f} 90)')
        print(f'    (path /{t+nc:08X})')
        print(f'    (fp_text reference U{nc} (at 0 0.5 90) (layer B.SilkS)')
        print(f'      (effects (font (size 1 1) (thickness 0.15)))')
        print(f'    )')
        print(f'    (fp_text value APA102C_x{n} (at 0 -0.5 90) (layer B.Fab)')
        print(f'      (effects (font (size 1 1) (thickness 0.15)))')
        print(f'    )')
        print(f'    (fp_line (start -{w2:.4f} -5.08) (end -{w2:.4f} 5.08) (layer B.CrtYd) (width 0.15))')
        print(f'    (fp_line (start {w2:.4f} -5.08) (end -{w2:.4f} -5.08) (layer B.CrtYd) (width 0.15))')
        print(f'    (fp_line (start {w2:.4f} 5.08) (end {w2:.4f} -5.08) (layer B.CrtYd) (width 0.15))')
        print(f'    (fp_line (start -{w2:.4f} 5.08) (end {w2:.4f} 5.08) (layer B.CrtYd) (width 0.15))')
        print(f'    (pad 1 thru_hole oval (at -{w2:.4f} -3.81 90) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask))')
        print(f'    (pad 2 thru_hole oval (at -{w2:.4f} -1.27 90) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask))')
        print(f'    (pad 3 thru_hole oval (at -{w2:.4f} 1.27 90) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask))')
        print(f'    (pad 4 thru_hole oval (at -{w2:.4f} 3.81 90) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask))')
        print(f'    (pad 5 thru_hole oval (at {w2:.4f} -3.81 90) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask))')
        print(f'    (pad 6 thru_hole oval (at {w2:.4f} -1.27 90) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask))')
        print(f'    (pad 7 thru_hole oval (at {w2:.4f} 1.27 90) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask))')
        print(f'    (pad 8 thru_hole oval (at {w2:.4f} 3.81 90) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask))')
        print(f'  )')
        nc += 1
        sy = -1
