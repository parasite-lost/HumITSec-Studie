set terminal pdfcairo enhanced fontscale 0.3
set output "noplan.pdf"
set yr [0:11]
set xtics rotate by -60
#set xtics "font,size"
plot "noplan.plot" using (column(0)):2:xtic(1) t '' w boxes fs solid 0.5 linecolor rgb "blue"
