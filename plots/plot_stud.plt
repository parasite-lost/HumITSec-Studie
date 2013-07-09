set terminal pdfcairo enhanced fontscale 0.3
set output "stud.pdf"
set yr [0:45]
set xtics rotate by -60
#set xtics "font,size"
plot "stud.plot" using (column(0)):2:xtic(1) t '' w boxes fs solid 0.5 linecolor rgb "blue"
