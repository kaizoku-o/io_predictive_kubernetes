set terminal png size 700,500 enhanced font "Times,26"
set title "I/O Utilization Prediction using ARIMA"
set ylabel "Disk I/O Utilization (%)"
set xlabel "Time in (Seconds)"
set term png
set output "arima_10s_pred_1m_results.png"
plot "ARIMA_10s_pred_1m_results.dat" using 1:2 title 'Actual' with lines lw 2,"ARIMA_10s_pred_1m_results.dat" using 1:3 title 'Predicted' with lines lw 2

