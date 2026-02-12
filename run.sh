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

# Source message box utility
source "$(dirname "$0")/message_box.sh"

# Check for Colab environment
IS_COLAB=false
if [[ -f "infobim-ifc.env.yaml" ]] && grep -q "engine: colab" "infobim-ifc.env.yaml"; then
    IS_COLAB=true
fi

# Activate venv if not in Colab
if [ "$IS_COLAB" = false ]; then
    if [[ -f "venv/bin/activate" ]]; then
        source venv/bin/activate
    else
        echo -e "${RED}Virtual environment not found in venv/${RESET}"
        echo -e "${YELLOW}Please run './infobim check --repair' to setup the environment.${RESET}"
        exit 1
    fi
fi

# Run Checks
echo ""
echo -e "${GRAY}${FULL_HLINE}${RESET}"
echo -e "${CYAN}Running IFC Checks...${RESET}"
echo -e "${GRAY}${FULL_HLINE}${RESET}"
echo ""

check() {
    if [ ! -d "$CHECK_DIR" ]; then
            echo -e "${RED}Directory not found: ${CHECK_DIR}${RESET}"
            deactivate
            exit 1
    fi

    for check_script in "$CHECK_DIR"/*.sh; do
        if [ -f "$check_script" ]; then
            # Reset variables
            DESCRIPTION=""
            unset -f check
            unset -f repair
            unset -f hotfix
            
            # Source the script
            source "$check_script"
            
            # Run check
            if check; then
                    echo -e "  ${GREEN}✓ ${DESCRIPTION}${RESET}"
            else
                    # Check failed, try hotfix first
                    HOTFIXED=false
                    if type hotfix &>/dev/null; then
                        if hotfix; then
                            if check; then
                                echo -e "  ${GREEN}✓ ${DESCRIPTION} (Hotfixed)${RESET}"
                                HOTFIXED=true
                            fi
                        fi
                    fi

                    if [ "$HOTFIXED" = false ]; then
                        if [ "$REPAIR_MODE" = true ]; then
                            echo -e "  ${YELLOW}⚡ Attempting repair for: ${DESCRIPTION}...${RESET}"
                            if type repair &>/dev/null; then
                                repair
                                # Re-check
                                if check; then
                                    echo -e "  ${GREEN}✓ ${DESCRIPTION} (Repaired)${RESET}"
                                else
                                    echo -e "  ${RED}✗ ${DESCRIPTION} (Repair failed)${RESET}"
                                    ANY_CHECK_FAILED=true
                                fi
                            else
                                echo -e "  ${RED}✗ ${DESCRIPTION} (No repair function)${RESET}"
                                ANY_CHECK_FAILED=true
                            fi
                        else
                            echo -e "  ${RED}✗ ${DESCRIPTION}${RESET}"
                            if type repair &>/dev/null; then
                                repair
                            fi
                            ANY_CHECK_FAILED=true
                        fi
                    fi
            fi
        fi
    done
}

ANY_CHECK_FAILED=false

CHECK_DIR="stack/check/infra"
check

CHECK_DIR="stack/check/ifc"
check

if [ "$ANY_CHECK_FAILED" = true ]; then
    echo ""
    print_message_box "$RED" "Error" "Checks Failed" "One or more checks failed.\n\n Please run ${CYAN}'./infobim check --repair'${GRAY} to fix the issues.${RESET}"
    echo ""
    deactivate
    exit 1
fi

# Check if project module is enabled
PROJ_ENABLED="true"
if [ -f "stack/infobim-ifc.yaml" ]; then
    PROJ_ENABLED=$(python3 -c "import yaml; config = yaml.safe_load(open('stack/infobim-ifc.yaml')); print(str(next((m['proj']['enabled'] for m in config.get('modules', []) if 'proj' in m), True)).lower())" 2>/dev/null)
fi

# Check if ./data exists and ./data/config.yaml exists
if [ "$PROJ_ENABLED" == "true" ] && [[ ! -d "./data" || ! -f "./data/config.yaml" ]]; then
    echo ""
    print_message_box "$RED" "Error" "Project not initialized" "Please use ./infobim init to initialize it."
    echo ""
    exit 1
fi

echo ""
echo -e "${CYAN}Starting InfoBIM...${RESET}"
echo ""

export PYTHONPATH=$PYTHONPATH:.
./venv/bin/python3 ./stack/src/tui/terminal/ifc.py "$@"
