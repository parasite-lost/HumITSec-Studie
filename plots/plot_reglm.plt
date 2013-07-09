set terminal pdfcairo enhanced fontscale 0.3
set output "reglm.pdf"
set yr [0:18]
set xtics rotate by -60
#set xtics "font,size"
plot "reglm.plot" using (column(0)):2:xtic(1) t '' w boxes fs solid 0.5 linecolor rgb "blue"
