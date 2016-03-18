#!/bin/bash

python ./debye.py

base=debye_excesses

psbasemap -JX12/8 -R0/1/0/0.10 -B0.2f0.1:"T / @~\121@~@-D@-":/0.02f0.01:"C@-V@-@+xs@+/Nk@-B@-":SWn -K -P > ${base}.ps
awk '{print $1, $2}' debye_excesses.dat | psxy -J -R -O -K -W1,black  >> ${base}.ps


psbasemap -JX12/8 -R0/1/0/0.15 -B0.2f0.1:"T / @~121@~@-D@-":/0.05f0.01:"S@+xs@+/Nk@-B@-":E -K -O >> ${base}.ps
awk '{print $1, $3}' debye_excesses.dat | psxy -J -R -O -W1,red  >> ${base}.ps


ps2epsi ${base}.ps
epstopdf ${base}.epsi

rm ${base}.ps ${base}.epsi
