#!/bin/bash

# Define colors
BOLD='\033[1m'
RESET='\033[0m'
CYAN='\033[36m'
GRAY='\033[90m'
WHITE='\033[37m'
YELLOW='\033[33m'
GREEN='\033[32m'
RED='\033[31m'

# Get terminal width
TERM_WIDTH=$(tput cols)
INNER_WIDTH=$((TERM_WIDTH - 2))

# Generate horizontal lines
HLINE=$(printf '─%.0s' $(seq 1 $INNER_WIDTH))
FULL_HLINE=$(printf '─%.0s' $(seq 1 $TERM_WIDTH))

source "$(dirname "$0")/message_box.sh"

echo ""
echo -e "${GRAY}${FULL_HLINE}${RESET}"
echo -e "  ${BOLD}Initializing Project...${RESET}"
echo -e "${GRAY}${FULL_HLINE}${RESET}"
echo ""

# Create directories
DIRS=("data" "data/incoming")

for dir in "${DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        echo -e "  ${CYAN}Creating directory: ${dir}...${RESET}"
        mkdir -p "$dir"
    else
        echo -e "  ${GRAY}Directory exists: ${dir}${RESET}"
    fi
done

# Create config.yaml
if [ ! -f "data/config.yaml" ]; then
    echo -e "  ${CYAN}Creating data/config.yaml...${RESET}"
    # Copy from template if available, else create basic one
    TEMPLATE_CONFIG="stack/src/tui/terminal/template/infobim-community-template/config.yaml"
    if [ -f "$TEMPLATE_CONFIG" ]; then
        cp "$TEMPLATE_CONFIG" "data/config.yaml"
    else
        echo "name: My Project" > "data/config.yaml"
    fi
else
    echo -e "  ${GRAY}Config exists: data/config.yaml${RESET}"
fi

echo ""
print_message_box "$GREEN" "Success" "Project Initialized" "You can now run ./infobim run"
echo ""
