#!/bin/sh

cd "$(dirname $(readlink -f "$0"))"


python ../slideio.py slides.drawio tmp.drawio
drawio --export -a tmp.drawio
rm tmp.drawio
mv tmp.pdf slides.pdf

