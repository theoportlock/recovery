# Paths
DIR = writing/manuscript
OUTDIR = $(DIR)/output
DOCX_OUTPUT = $(OUTDIR)/main.docx
PDF_OUTPUT = $(OUTDIR)/main.pdf
TEX_INPUT = $(DIR)/main.tex
BIB_FILE = $(DIR)/library.bib
CSL_FILE = $(DIR)/nature.csl

WATCH_FILES = $(TEX_INPUT) $(BIB_FILE) $(CSL_FILE)

# Default target
all: $(PDF_OUTPUT) $(DOCX_OUTPUT)

# Create DOCX from LaTeX using Pandoc
$(DOCX_OUTPUT): $(TEX_INPUT) $(BIB_FILE) $(CSL_FILE)
	mkdir -p $(OUTDIR)
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

# Build PDF with all intermediate and output files in OUTDIR
$(PDF_OUTPUT): $(TEX_INPUT) $(BIB_FILE)
	mkdir -p $(OUTDIR)
	pdflatex -shell-escape -output-directory=$(OUTDIR) $(TEX_INPUT)
	bibtex $(OUTDIR)/main
	pdflatex -shell-escape -output-directory=$(OUTDIR) $(TEX_INPUT)
	pdflatex -shell-escape -output-directory=$(OUTDIR) $(TEX_INPUT)

# Watch for changes and rebuild
watch:
	ls $(WATCH_FILES) | entr -c make all

# Clean all generated files
clean:
	rm -f $(OUTDIR)/*.{aux,log,out,bbl,blg,glg,glo,gls,ist,toc,acn,acr,alg,pdf,docx}

.PHONY: all watch clean


