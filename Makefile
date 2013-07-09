all:
	@rubber -d -f slides.tex

clean:
	@rubber --clean slides.tex
	@rm slides.vrb
