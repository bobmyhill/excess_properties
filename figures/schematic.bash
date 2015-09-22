#!/bin/bash

gmtset FONT_ANNOT_PRIMARY	   = 10p,4,black
gmtset FONT_LABEL        	   = 14p,4,black
base="schematic"

psbasemap -JX12/8 -R0/1/-2000/7000 -Ba1f0.5:"X@-B@-":/a1000f500:"Excess Gibbs free energy (J/mol)":SWen -K -P > ${base}.ps

awk '{print $1, $2}' schematic.dat | psxy -J -R -O -K -W0.5,black,- >> ${base}.ps
awk '{print $1, $3}' schematic.dat | psxy -J -R -O -K -W0.5,black >> ${base}.ps
awk '{print $1, $4}' schematic.dat | psxy -J -R -O -K -W0.5,black >> ${base}.ps
awk '{print $1, $5}' schematic.dat | psxy -J -R -O -K -W1,black >> ${base}.ps

awk '$1==0.5 {printf "%f %f\n%f %f", 0, 0, 1, 0}' schematic.dat | psxy -J -R -O -K -W0.5,black >> ${base}.ps

awk '$1==0.5 {printf "%f %f\n%f %f", $1-0.005, $2, $1-0.005, 0}' schematic.dat | psxy -J -R -O -K -W0.5,grey >> ${base}.ps

awk '$1==0.5 {printf "%f %f\n%f %f", $1, $2, $1, $3}' schematic.dat | psxy -J -R -O -K -W0.5,red >> ${base}.ps

awk '$1==0.5 {printf "%f %f\n%f %f", $1+0.005, $2, $1+0.005, $4}' schematic.dat | psxy -J -R -O -K -W0.5,blue >> ${base}.ps


awk '$1==0.5 {print $1, $2}' schematic.dat | psxy -J -R -O -K -Sx0.2c -W0.5,black >> ${base}.ps
awk '$1==0.5 {print $1, $3}' schematic.dat | psxy -J -R -O -K -Sc0.2c -Gred -W0.5,black >> ${base}.ps
awk '$1==0.5 {print $1, $4}' schematic.dat | psxy -J -R -O -K -Sc0.2c -Gblue -W0.5,black >> ${base}.ps

echo "0.48 -1000 TS@+conf@+" | pstext -J -R -O -K -F+jRM+fgrey >> ${base}.ps
echo "0.49 1500 G@-BA@-@+xs@+ = W@-BA@-/4" | pstext -J -R -O -K -F+jRM+fred >> ${base}.ps
echo "0.52 3000 G@-AB@-@+xs@+ = W@-AB@-/4" | pstext -J -R -O -K -F+jLM+fblue >> ${base}.ps

echo "0.32 5000 G@+xs@+" | pstext -J -R -O -F+jLM >> ${base}.ps

ps2epsi ${base}.ps
epstopdf ${base}.epsi

rm ${base}.ps ${base}.epsi

evince ${base}.pdf &

