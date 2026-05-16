# =============================================================================
#  OADF :: Oral Adiabatic Decompression Fog — Master Build Orchestrator
# -----------------------------------------------------------------------------
#  Targets:
#    make            -> alias for `make paper`
#    make paper      -> compile LaTeX -> PDF (latexmk preferred, pdflatex fallback)
#    make web        -> serve docs/web on http://localhost:8000
#    make validate   -> run HTML structural validator
#    make clean      -> remove transient build artifacts
#    make distclean  -> clean + remove compiled PDF output
#    make help       -> list available targets
# =============================================================================

SHELL          := /bin/sh
.DEFAULT_GOAL  := paper

# ---- Configuration ----------------------------------------------------------
PAPER_DIR      := docs/paper
PAPER_SRC      := $(PAPER_DIR)/OADF_academic_paper.tex
PAPER_PDF      := $(PAPER_DIR)/OADF_academic_paper.pdf
BUILD_DIR      := $(PAPER_DIR)/.build

WEB_DIR        := docs/web
WEB_PORT       ?= 8000

SCRIPTS_DIR    := scripts
PYTHON         ?= python3

# Tool detection (executed lazily; expanded at recipe time only)
HAVE_LATEXMK   := $(shell command -v latexmk 2>/dev/null)
HAVE_PDFLATEX  := $(shell command -v pdflatex 2>/dev/null)
HAVE_PYTHON    := $(shell command -v $(PYTHON) 2>/dev/null)

# ---- Phony targets ----------------------------------------------------------
.PHONY: all paper paper-latexmk paper-pdflatex web validate clean distclean help

all: paper

# ---- Paper compilation ------------------------------------------------------
paper:
	@if [ -n "$(HAVE_LATEXMK)" ]; then \
		$(MAKE) paper-latexmk; \
	elif [ -n "$(HAVE_PDFLATEX)" ]; then \
		$(MAKE) paper-pdflatex; \
	else \
		echo "[FATAL] Neither latexmk nor pdflatex found on PATH." >&2; \
		exit 127; \
	fi

paper-latexmk:
	@echo "[BUILD] latexmk -> $(PAPER_PDF)"
	@mkdir -p $(BUILD_DIR)
	@latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error \
		-output-directory=$(BUILD_DIR) $(PAPER_SRC)
	@cp $(BUILD_DIR)/$(notdir $(basename $(PAPER_SRC))).pdf $(PAPER_PDF)
	@echo "[OK]    $(PAPER_PDF)"

paper-pdflatex:
	@echo "[BUILD] pdflatex (3-pass) -> $(PAPER_PDF)"
	@mkdir -p $(BUILD_DIR)
	@pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
		-output-directory=$(BUILD_DIR) $(PAPER_SRC)
	@pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
		-output-directory=$(BUILD_DIR) $(PAPER_SRC)
	@pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
		-output-directory=$(BUILD_DIR) $(PAPER_SRC)
	@cp $(BUILD_DIR)/$(notdir $(basename $(PAPER_SRC))).pdf $(PAPER_PDF)
	@echo "[OK]    $(PAPER_PDF)"

# ---- Web preview ------------------------------------------------------------
web:
	@if [ -z "$(HAVE_PYTHON)" ]; then \
		echo "[FATAL] $(PYTHON) not found on PATH." >&2; exit 127; \
	fi
	@echo "[SERVE] http://localhost:$(WEB_PORT)  (Ctrl-C to stop)"
	@cd $(WEB_DIR) && $(PYTHON) -m http.server $(WEB_PORT)

# ---- Validation -------------------------------------------------------------
validate:
	@if [ -z "$(HAVE_PYTHON)" ]; then \
		echo "[FATAL] $(PYTHON) not found on PATH." >&2; exit 127; \
	fi
	@$(PYTHON) $(SCRIPTS_DIR)/validate_html.py $(WEB_DIR)

# ---- Cleanup ----------------------------------------------------------------
clean:
	@echo "[CLEAN] Removing transient LaTeX artifacts"
	@rm -rf $(BUILD_DIR)
	@find $(PAPER_DIR) -maxdepth 1 -type f \( \
		-name '*.aux' -o -name '*.bbl' -o -name '*.blg' -o \
		-name '*.log' -o -name '*.out' -o -name '*.toc' -o \
		-name '*.fls' -o -name '*.fdb_latexmk' -o -name '*.synctex.gz' \
	\) -delete
	@echo "[OK]    transient artifacts purged"

distclean: clean
	@echo "[CLEAN] Removing compiled PDF"
	@rm -f $(PAPER_PDF)

# ---- Help -------------------------------------------------------------------
help:
	@echo "OADF :: Make targets"
	@echo "  paper       compile docs/paper/*.tex -> PDF"
	@echo "  web         serve docs/web on :$(WEB_PORT)"
	@echo "  validate    run HTML structural validator"
	@echo "  clean       remove LaTeX build artifacts"
	@echo "  distclean   clean + remove final PDF"
	@echo "  help        this message"
