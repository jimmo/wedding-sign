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
        n = y-sy
        cy = sy*600+300+(y-sy)*300
        print(f'$Comp')
        print(f'L APA102C_x{y-sy} U{nc}')
        print(f'U 1 1 {nc+0x5954F10D:8X}')
        print(f'P {cx} {cy}')
        print(f'F 0 "U{nc}" H {cx} {cy+250} 60  0000 C CNN')
        print(f'F 1 "APA102C_x{y-sy}" H {cx} {cy-250} 60  0000 C CNN')
        print(f'F 2 "" H {cx} {cy} 60  0001 C CNN')
        print(f'F 3 "" H {cx} {cy} 60  0001 C CNN')
        print(f'\t1\t{cx}\t{cy}')
        print(f'\t0\t1\t1\t0')
        print(f'$EndComp')
        nc += 1
        sy = -1

print(f'(module apa102c_72m:APA102C_72m_x{n} (layer B.Cu) (tedit 595508FC) (tstamp 595518F8)')
print(f'  (at 136.5389 148.59 270)')
print(f'  (path /5954F17C)')
print(f'  (fp_text reference U112 (at 0 -0.5 270) (layer B.SilkS)')
print(f'    (effects (font (size 1 1) (thickness 0.15)) (justify mirror))')
print(f'  )')
print(f'  (fp_text value APA102C_x16 (at 0 0.5 270) (layer B.Fab)')
print(f'    (effects (font (size 1 1) (thickness 0.15)) (justify mirror))')
print(f'  )')
print(f'  (fp_line (start -111.1111 5.08) (end -111.1111 -5.08) (layer B.CrtYd) (width 0.15)')
print(f'  (fp_line (start 111.1111 5.08) (end -111.1111 5.08) (layer B.CrtYd) (width 0.15)')
print(f'  (fp_line (start 111.1111 -5.08) (end 111.1111 5.08) (layer B.CrtYd) (width 0.15)')
print(f'  (fp_line (start -111.1111 -5.08) (end 111.1111 -5.08) (layer B.CrtYd) (width 0.15)')
print(f'  (pad 1 thru_hole oval (at -111.1111 3.81 270) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask)')
print(f'    (net 810 "Net-(U112-Pad1)"))')
print(f'  (pad 2 thru_hole oval (at -111.1111 1.27 270) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask)')
print(f'    (net 811 "Net-(U112-Pad2)"))')
print(f'  (pad 3 thru_hole oval (at -111.1111 -1.27 270) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask)')
print(f'    (net 812 "Net-(U112-Pad3)"))')
print(f'  (pad 4 thru_hole oval (at -111.1111 -3.81 270) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask)')
print(f'    (net 813 "Net-(U112-Pad4)"))')
print(f'  (pad 5 thru_hole oval (at 111.1111 3.81 270) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask)')
print(f'    (net 814 "Net-(U112-Pad5)"))')
print(f'  (pad 6 thru_hole oval (at 111.1111 1.27 270) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask)')
print(f'    (net 815 "Net-(U112-Pad6)"))')
print(f'  (pad 7 thru_hole oval (at 111.1111 -1.27 270) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask)')
print(f'    (net 816 "Net-(U112-Pad7)"))')
print(f'  (pad 8 thru_hole oval (at 111.1111 -3.81 270) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask)')
print(f'    (net 817 "Net-(U112-Pad8)"))')
  (fp_text reference U{nc} (at 0 -0.5 270) (layer B.SilkS)
    (effects (font (size 1 1) (thickness 0.15)) (justify mirror))
  )
  (fp_text value APA102C_72m_x{n} (at 0 -0.5 270) (layer B.Fab)
    (effects (font (size 1 1) (thickness 0.15)) (justify mirror))
  )
  (fp_line (start -${W} -5.08) (end -${W} 5.08) (layer B.CrtYd) (width 0.15))
  (fp_line (start ${W} -5.08) (end -${W} -5.08) (layer B.CrtYd) (width 0.15))
  (fp_line (start ${W} 5.08) (end ${W} -5.08) (layer B.CrtYd) (width 0.15))
  (fp_line (start -${W} 5.08) (end ${W} 5.08) (layer B.CrtYd) (width 0.15))
  (pad 1 thru_hole oval (at -${W} -3.81) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask))
  (pad 2 thru_hole oval (at -${W} -1.27) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask))
  (pad 3 thru_hole oval (at -${W} 1.27) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask))
  (pad 4 thru_hole oval (at -${W} 3.81) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask))
  (pad 5 thru_hole oval (at ${W} -3.81) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask))
  (pad 6 thru_hole oval (at ${W} -1.27) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask))
  (pad 7 thru_hole oval (at ${W} 1.27) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask))
  (pad 8 thru_hole oval (at ${W} 3.81) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask))
print(f')')
