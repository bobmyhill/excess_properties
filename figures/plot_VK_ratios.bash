#!/bin/bash

base="VK_ratio"
psbasemap -JX12/8 -R0.98/1.01/0.9/1.3 -K -B0.01f0.005:'V/V@-ideal@-':/0.1f0.05:'K/K@-T ideal@-':SWen -P > ${base}.ps

echo "0.98 1.01 100 2.33333" | awk '{for (i=$1; i<=$2; i=i+($2-$1)/$3) {print i, i^-$4}}' | psxy -J -R -O -K -W1,black >> ${base}.ps
echo "0.98 1.01 100 7" | awk '{for (i=$1; i<=$2; i=i+($2-$1)/$3) {print i, i^-$4}}' | psxy -J -R -O -K -W1,black >> ${base}.ps
echo "0.98 1.01 100 14" | awk '{for (i=$1; i<=$2; i=i+($2-$1)/$3) {print i, i^-$4}}' | psxy -J -R -O -K -W1,black >> ${base}.ps
echo "0.98 1.01 100 21" | awk '{for (i=$1; i<=$2; i=i+($2-$1)/$3) {print i, i^-$4}}' | psxy -J -R -O -K -W1,black >> ${base}.ps

echo "0.9898 1.265 @~\170@~=21" | pstext -J -R -O -K -F+f12,4,black+jLM >> ${base}.ps
echo "0.9847 1.26 @~\170@~=14" | pstext -J -R -O -K -F+f12,4,black+jLM >> ${base}.ps
echo "0.9806 1.17 @~\170@~=7" | pstext -J -R -O -K -F+f12,4,black+jLM >> ${base}.ps
echo "0.9806 1.07 @~\170@~=7/3" | pstext -J -R -O -K -F+f12,4,black+jLM >> ${base}.ps

python Fort_Moore_excesses.py | psxy -J -R -O -K -Sc0.1c >> ${base}.ps

echo 1.009 1.28 | psxy -J -R -O -K -Sc0.2c -Gred >> ${base}.ps
echo 1.009 1.26 | psxy -J -R -O -K -Sc0.2c -Gblue >> ${base}.ps
echo 1.009 1.24 | psxy -J -R -O -K -Sa0.2c -Ggreen >> ${base}.ps
echo 1.009 1.22 | psxy -J -R -O -K -Sd0.2c -Gblack >> ${base}.ps
echo 1.009 1.20 | psxy -J -R -O -K -Sh0.2c -Gpurple >> ${base}.ps
echo 1.009 1.18 | psxy -J -R -O -K -Ss0.2c -Gorange >> ${base}.ps

echo 1.008 1.28 pyrope - grossular | pstext -J -R -O -K -F+f12,4,black+jRM >> ${base}.ps
echo 1.008 1.26 jadeite - aegirine | pstext -J -R -O -K -F+f12,4,black+jRM >> ${base}.ps
echo 1.008 1.24 benzene - cyclohexane | pstext -J -R -O -K -F+f12,4,black+jRM >> ${base}.ps
echo 1.008 1.22 s-tetrachloroethane - acetone | pstext -J -R -O -K -F+f12,4,black+jRM >> ${base}.ps
echo 1.008 1.20 o-chlorphenol - dioxane | pstext -J -R -O -K -F+f12,4,black+jRM >> ${base}.ps
echo 1.008 1.18 dimethyl-sulfoxide - acetic acid | pstext -J -R -O -F+f12,4,black+jRM >> ${base}.ps
ps2epsi ${base}.ps 
epstopdf ${base}.epsi 
evince ${base}.pdf
