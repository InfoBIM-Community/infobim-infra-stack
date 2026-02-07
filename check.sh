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

# --- Functions ---
source "$(dirname "$0")/message_box.sh"

REPAIR_MODE=false
SCOPE="all"

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --repair) REPAIR_MODE=true ;;
        --scope) SCOPE="$2"; shift ;;
        *) ;;
    esac
    shift
done

echo ""
echo -e "${GRAY}${FULL_HLINE}${RESET}"
echo -e "${CYAN}Running System Checks...${RESET}"
echo -e "${GRAY}${FULL_HLINE}${RESET}"
echo ""

ERRORS=()
WARNINGS=()

run_checks() {
    local DIR="$1"
    local NAME="$2"
    
    echo -e "${YELLOW}❯ ${WHITE}Checking ${CYAN}${NAME}${RESET}"
    
    # Check if directory exists
    if [ ! -d "$DIR" ]; then
         echo -e "  ${GRAY}• Directory not found: ${DIR}${RESET}"
         return
    fi

    for check_script in "$DIR"/*.sh; do
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
                             WARNINGS+=("${DESCRIPTION} (Hotfixed)")
                             HOTFIXED=true
                         fi
                     fi
                 fi

                 if [ "$HOTFIXED" = false ]; then
                     # Check failed
                     if [ "$REPAIR_MODE" = true ]; then
                         echo -e "  ${YELLOW}⚡ Attempting repair for: ${DESCRIPTION}...${RESET}"
                         if type repair &>/dev/null; then
                             repair
                             
                             # Re-check
                             if check; then
                                 echo -e "  ${GREEN}✓ ${DESCRIPTION} (Repaired)${RESET}"
                                 WARNINGS+=("${DESCRIPTION} (Repaired)")
                             else
                                 echo -e "  ${RED}✗ ${DESCRIPTION} (Repair failed)${RESET}"
                                 ERRORS+=("${DESCRIPTION}")
                             fi
                         else
                             echo -e "  ${RED}✗ ${DESCRIPTION} (No repair function)${RESET}"
                             ERRORS+=("${DESCRIPTION}")
                         fi
                     else
                         echo -e "  ${RED}✗ ${DESCRIPTION}${RESET}"
                         ERRORS+=("${DESCRIPTION}")
                     fi
                 fi
            fi
        fi
    done
}

# Run checks based on scope
if [[ "$SCOPE" == "all" || "$SCOPE" == "infra" ]]; then
    run_checks "./stack/check/infra" "Infra"
fi

# Activate virtual environment if it exists (for subsequent checks)
if [ -z "$VIRTUAL_ENV" ] && [ -f "venv/bin/activate" ]; then
    source "venv/bin/activate"
fi

echo ""
if [[ "$SCOPE" == "all" || "$SCOPE" == "project" ]]; then
    PROJECT_ENABLED=true
    CONFIG_FILE="./stack/infobim-ifc.yaml"
    
    # Check if project module is enabled in config
    if [ -f "$CONFIG_FILE" ]; then
        if command -v python3 &>/dev/null; then
            PY_SCRIPT=$(mktemp)
            cat <<EOF > "$PY_SCRIPT"
import sys
try:
    with open('$CONFIG_FILE', 'r') as f:
        lines = f.readlines()
    in_proj = False
    for line in lines:
        s = line.strip()
        if s.startswith('- proj:'):
            in_proj = True
            continue
        if in_proj:
            if s.startswith('-'): break
            if s.startswith('enabled:'):
                if s.split(':')[1].strip().lower() == 'false':
                    sys.exit(1)
except Exception:
    pass
sys.exit(0)
EOF
            if ! python3 "$PY_SCRIPT"; then
                PROJECT_ENABLED=false
            fi
            rm -f "$PY_SCRIPT"
        fi
    fi

    if [ "$PROJECT_ENABLED" = true ]; then
        run_checks "./stack/check/project" "Project"
    else
        echo -e "${YELLOW}❯ ${WHITE}Checking Project${RESET}"
        echo -e "  ${GRAY}• Skipped (Disabled in config)${RESET}"
    fi
fi
echo ""
if [[ "$SCOPE" == "all" || "$SCOPE" == "ifc" ]]; then
    run_checks "./stack/check/ifc" "IFC"
fi
echo ""



# Final Report
if [ ${#ERRORS[@]} -eq 0 ]; then
    MSG="All checks passed."
    if [ ${#WARNINGS[@]} -gt 0 ]; then
        MSG="${MSG}\n\nWarnings:"
        for w in "${WARNINGS[@]}"; do
            MSG="${MSG}\n• $w"
        done
    fi
    print_message_box "$GREEN" "Success" "System Operational" "$MSG"
else
    MSG="The following checks failed:"
    for e in "${ERRORS[@]}"; do
        MSG="${MSG}\n• $e"
    done
    
    if [ ${#WARNINGS[@]} -gt 0 ]; then
        MSG="${MSG}\n\nWarnings:"
        for w in "${WARNINGS[@]}"; do
            MSG="${MSG}\n• $w"
        done
    fi
    
    print_message_box "$RED" "Error" "System Check Failed" "$MSG"
fi

echo ""
