echo 'EESchema-LIBRARY Version 2.3'
echo '#encoding utf-8'

for i in {1..20}; do
    cat <<EOF
#
# APA102C_x$i
#
DEF APA102C_x$i U 0 40 Y Y 1 F N
F0 "U" 0 250 60 H V C CNN
F1 "APA102C_x$i" 0 -250 60 H V C CNN
F2 "" 0 0 60 H I C CNN
F3 "" 0 0 60 H I C CNN
DRAW
S -$((i*300)) 200 $((i*300)) -200 0 1 0 N
X Vin 1 -$((i*300+200)) 150 200 R 50 50 1 1 W
X Cin 2 -$((i*300+200)) 50 200 R 50 50 1 1 I
X Din 3 -$((i*300+200)) -50 200 R 50 50 1 1 I
X Dout 3 $((i*300+200)) -50 200 L 50 50 1 1 O
X Gin 4 -$((i*300+200)) -150 200 R 50 50 1 1 W
X Gout 4 $((i*300+200)) -150 200 L 50 50 1 1 w
X Vout 5 $((i*300+200)) 150 200 L 50 50 1 1 w
X Cout 6 $((i*300+200)) 50 200 L 50 50 1 1 O
ENDDRAW
ENDDEF
EOF
done
