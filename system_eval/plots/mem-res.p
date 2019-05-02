set terminal png size 850,550 enhanced font "Helvetica,18"
set output "mem-res.png"
set style fill pattern border -1
set style histogram errorbars gap 2 lw 2
set style data histograms

set boxwidth 0.8
set grid ytics
set title "MySQL Response time (Memory)"
set ylabel "Average Response Time (ms)" font "Helvetica,16"
set xlabel "System workload with number of memory stressors" font "Helvetica,16"
set key font ",8"
set key width -5
set yrange [0:0.8]



plot 'mem-res.dat' u 2:($2+$3):($2-$3):xtic(1) with histogram title "Default",\
    '' u 4:($4+$5):($4-$5):xtic(1) with histogram title "Tetris"
