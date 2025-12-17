#!/bin/bash
# Helper script to compile D&D LaTeX examples

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Directories
LATEX_DIR="$SCRIPT_DIR/latex"
OUTPUT_DIR="$SCRIPT_DIR/output"
TEMPLATE_DIR="$REPO_ROOT/DND-5e-LaTeX-Template"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Function to print usage
usage() {
    echo "Usage: $0 <filename_without_extension> | clean"
    echo ""
    echo "Examples:"
    echo "  $0 character_example    # Compiles examples/latex/character_example.tex"
    echo "  $0 npc_example         # Compiles examples/latex/npc_example.tex"
    echo "  $0 clean               # Remove auxiliary files"
    echo ""
    echo "Available files:"
    for file in "$LATEX_DIR"/*.tex; do
        basename="${file%.tex}"
        basename="${basename##*/}"
        echo "  - $basename"
    done
    exit 1
}

# Function to clean auxiliary files
clean() {
    echo -e "${YELLOW}Cleaning auxiliary files...${NC}"
    cd "$OUTPUT_DIR"
    rm -f *.aux *.log *.out *.toc *.fdb_latexmk *.fls *.synctex.gz
    echo -e "${GREEN}✓ Cleaned!${NC}"
    exit 0
}

# Check arguments
if [ $# -eq 0 ]; then
    usage
fi

# Handle clean command
if [ "$1" == "clean" ]; then
    clean
fi

# Get filename
FILENAME="$1"
TEX_FILE="$LATEX_DIR/${FILENAME}.tex"

# Check if file exists
if [ ! -f "$TEX_FILE" ]; then
    echo -e "${RED}Error: File not found: $TEX_FILE${NC}"
    echo ""
    usage
fi

# Check if DND template exists
if [ ! -d "$TEMPLATE_DIR" ]; then
    echo -e "${RED}Error: DND-5e-LaTeX-Template not found at: $TEMPLATE_DIR${NC}"
    echo ""
    echo "Please clone it with:"
    echo "  cd $REPO_ROOT"
    echo "  git clone https://github.com/rpgtex/DND-5e-LaTeX-Template.git"
    exit 1
fi

# Check if lualatex is installed
if ! command -v lualatex &> /dev/null; then
    echo -e "${RED}Error: lualatex not found${NC}"
    echo ""
    echo "Please install TeX Live:"
    echo "  sudo apt install texlive-full"
    exit 1
fi

# Compile the document
echo -e "${YELLOW}Compiling $FILENAME.tex...${NC}"
echo ""

# Set TEXINPUTS to find the DND template
export TEXINPUTS="$TEMPLATE_DIR//:"

# Change to output directory
cd "$OUTPUT_DIR"

# Compile twice (first pass for content, second pass for references)
echo -e "${YELLOW}First pass...${NC}"
lualatex -interaction=nonstopmode -output-directory="$OUTPUT_DIR" "$TEX_FILE" > /dev/null 2>&1 || {
    echo -e "${RED}Error during first compilation pass. Check the log file:${NC}"
    echo "  $OUTPUT_DIR/${FILENAME}.log"
    exit 1
}

echo -e "${YELLOW}Second pass (resolving references)...${NC}"
lualatex -interaction=nonstopmode -output-directory="$OUTPUT_DIR" "$TEX_FILE" > /dev/null 2>&1 || {
    echo -e "${RED}Error during second compilation pass. Check the log file:${NC}"
    echo "  $OUTPUT_DIR/${FILENAME}.log"
    exit 1
}

# Check if PDF was created
PDF_FILE="$OUTPUT_DIR/${FILENAME}.pdf"
if [ -f "$PDF_FILE" ]; then
    PDF_SIZE=$(du -h "$PDF_FILE" | cut -f1)
    echo ""
    echo -e "${GREEN}✓ Success!${NC}"
    echo -e "  PDF created: ${GREEN}$PDF_FILE${NC}"
    echo -e "  Size: ${PDF_SIZE}"
    echo ""
    echo "To view the PDF:"
    echo "  xdg-open $PDF_FILE"
    echo ""
    echo "To clean auxiliary files:"
    echo "  $0 clean"
else
    echo -e "${RED}Error: PDF was not created${NC}"
    exit 1
fi
