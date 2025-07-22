# Output and input file definitions
DOCX_OUTPUT = main.docx
PDF_OUTPUT = main.pdf
TEX_INPUT = main.tex
BIB_FILE = library.bib
CSL_FILE = nature.csl

WATCH_FILES = $(TEX_INPUT) $(BIB_FILE) $(CSL_FILE)

# Default target
all: $(PDF_OUTPUT) $(DOCX_OUTPUT)

# Create DOCX from LaTeX using Pandoc
$(DOCX_OUTPUT): $(TEX_INPUT) $(BIB_FILE) $(CSL_FILE)
	pandoc \
		--filter pandoc-crossref \
		--citeproc \
		--bibliography=$(BIB_FILE) \
		-f latex \
		-t docx \
		--verbose \
		--number-sections \
		--csl=$(CSL_FILE) \
		$(TEX_INPUT) \
		-o $(DOCX_OUTPUT)

# Optional: also support building a PDF directly from LaTeX
$(PDF_OUTPUT): $(TEX_INPUT) $(BIB_FILE)
	pdflatex -shell-escape $(TEX_INPUT)
	bibtex main
	pdflatex -shell-escape $(TEX_INPUT)
	pdflatex -shell-escape $(TEX_INPUT)

# Watch for changes and rebuild
watch:
	ls $(WATCH_FILES) | entr -c make all

# Clean all generated files
clean:
	rm -f *.aux *.log *.out *.bbl *.blg *.glg *.glo *.gls *.ist *.toc *.acn *.acr *.alg *.pdf *.docx

.PHONY: all watch clean

