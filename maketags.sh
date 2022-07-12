#!/bin/bash
out="atagmain.py -i tag36h11_big_cropped_flipped -l"
while [ 0 -lt $# ]
do
    out="${out} $1"
    shift 1
done
echo "Running... python3" $out
python3 $out
exit