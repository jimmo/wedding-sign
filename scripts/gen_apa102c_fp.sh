
for i in {1..20}; do
  W=$(echo "scale=4;$i*1000/72/2" | bc)
  cat > apa102c_72m.pretty/APA102C_72m_x$i.kicad_mod <<EOF
(module APA102C_72m_x$i (layer F.Cu) (tedit $(printf %08X $(date +%s)))
  (fp_text reference REF** (at 0 0.5) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_text value APA102C_72m_x$i (at 0 -0.5) (layer F.Fab)
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (fp_line (start -${W} -5.08) (end -${W} 5.08) (layer F.CrtYd) (width 0.15))
  (fp_line (start ${W} -5.08) (end -${W} -5.08) (layer F.CrtYd) (width 0.15))
  (fp_line (start ${W} 5.08) (end ${W} -5.08) (layer F.CrtYd) (width 0.15))
  (fp_line (start -${W} 5.08) (end ${W} 5.08) (layer F.CrtYd) (width 0.15))
  (pad 1 thru_hole oval (at -${W} -3.81) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask))
  (pad 2 thru_hole oval (at -${W} -1.27) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask))
  (pad 3 thru_hole oval (at -${W} 1.27) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask))
  (pad 4 thru_hole oval (at -${W} 3.81) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask))
  (pad 5 thru_hole oval (at ${W} -3.81) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask))
  (pad 6 thru_hole oval (at ${W} -1.27) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask))
  (pad 7 thru_hole oval (at ${W} 1.27) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask))
  (pad 8 thru_hole oval (at ${W} 3.81) (size 3 1.524) (drill 0.762) (layers *.Cu *.Mask))
)
EOF
done
