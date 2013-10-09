TEXS=$(shell ls *.tex)
PDFS=$(TEXS:.tex=.pdf)


all: $(PDFS)


clean:
	-rm *~ $(PDFS) *.aux *.bbl *.blg *.log *.out


# At least two pdflatex runs for internal cross-referencing, plus
# another if running bibtex.

%.pdf: %.tex %.bib
	pdflatex $<
	bibtex $(<:.tex=)
	pdflatex $<
	pdflatex $<
