# Directories
SRC_DIR := writing/manuscript
OUT_DIR := $(SRC_DIR)/output

# Main files
TEX := $(SRC_DIR)/main.tex
PDF := $(OUT_DIR)/main.pdf
DOCX := $(OUT_DIR)/main.docx
TEMPLATE := $(SRC_DIR)/template.docx

# Tools
LATEXMK := latexmk
LATEXMK_FLAGS := -pdf -outdir=$(OUT_DIR) -interaction=nonstopmode -shell-escape
PANDOC := pandoc
BIB := $(SRC_DIR)/library.bib
CSL := $(SRC_DIR)/nature.csl

# Figures directory
FIGURES_DIR := figures

.PHONY: all pdf docx clean

all: pdf docx

pdf: $(PDF)

$(PDF): $(TEX) $(BIB)
	@mkdir -p $(OUT_DIR)
	$(LATEXMK) $(LATEXMK_FLAGS) $(TEX)

docx: $(DOCX)

$(DOCX): $(TEX) $(BIB) $(CSL)
	@mkdir -p $(OUT_DIR)
	$(PANDOC) $(TEX) \
		--bibliography=$(BIB) \
		--csl=$(CSL) \
		--output=$(DOCX) \
		--standalone \
		--citeproc \
		--toc \
		--filter pandoc-crossref \
		--resource-path=$(FIGURES_DIR) \
		--default-image-extension=png \
		--number-sections \
		--reference-doc=$(TEMPLATE)

clean:
	$(LATEXMK) -C -outdir=$(OUT_DIR)
	rm -f $(DOCX)
	rm -rf $(OUT_DIR)/media

