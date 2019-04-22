set terminal png size 700,500 enhanced font "Helvetica,18"
set output 'tetris-write-SLO.png'
set style fill pattern border -1
set style histogram clustered gap 1
set style data histograms
set grid ytics
set boxwidth 0.8
set yrange [0:20]
set title "MySQL Write SLO Violations"
set ylabel "SLO Violation (%)" font "Helvetica,16"
set xlabel "System workload with number of I/O stressors" font "Helvetica,16"
set key font ",8"
set key width -5
xoffset=0.25
yoffset=0.03
plot 'tetris-output-write.dat' using 2:xtic(1) with histogram title "Default", '' u 3 with histogram title "Tetris", '' u 0:2:2 with labels font "Helvetica,10" offset -1.6,0.5 title " ", ''u 0:3:3 with labels font "Helvetica,10" offset 1.8,0.5 title " "