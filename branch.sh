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
print_message_box() {
    local COLOR="$1"
    local TITLE_TYPE="$2"    # e.g., "Error", "Success", "Warning"
    local TITLE_TEXT="$3"
    local MSG_TEXT="$4"
    
    local TYPE_LEN=${#TITLE_TYPE}
    local TEXT_LEN=${#TITLE_TEXT}
    
    local TITLE_VISIBLE_LEN=$((4 + TYPE_LEN))
    if [ -n "$TITLE_TEXT" ]; then
        TITLE_VISIBLE_LEN=$((TITLE_VISIBLE_LEN + 1 + TEXT_LEN))
    fi

    local TITLE_PAD_LEN=$((INNER_WIDTH - TITLE_VISIBLE_LEN))
    if [ $TITLE_PAD_LEN -lt 0 ]; then TITLE_PAD_LEN=0; fi
    local TITLE_PAD=$(printf '%*s' "$TITLE_PAD_LEN" "")
    
    local MSG_LEN=${#MSG_TEXT}
    local MSG_PAD_LEN=$((INNER_WIDTH - MSG_LEN))
    if [ $MSG_PAD_LEN -lt 0 ]; then MSG_PAD_LEN=0; fi
    local MSG_PAD=$(printf '%*s' "$MSG_PAD_LEN" "")
    
    local EMPTY_PAD=$(printf '%*s' "$INNER_WIDTH" "")
    
    echo -e "${COLOR}╭${HLINE}╮${RESET}"
    if [ -n "$TITLE_TEXT" ]; then
        echo -e "${COLOR}│${RESET} >_ ${BOLD}${COLOR}${TITLE_TYPE}${RESET} ${TITLE_TEXT}${TITLE_PAD}${COLOR}│${RESET}"
    else
        echo -e "${COLOR}│${RESET} >_ ${BOLD}${COLOR}${TITLE_TYPE}${RESET}${TITLE_PAD}${COLOR}│${RESET}"
    fi
    echo -e "${COLOR}│${RESET}${EMPTY_PAD}${COLOR}│${RESET}"
    echo -e "${COLOR}│${RESET}${GRAY}${MSG_TEXT}${RESET}${MSG_PAD}${COLOR}│${RESET}"
    echo -e "${COLOR}╰${HLINE}╯${RESET}"
}

# Script to automate branch creation and checkout
# Usage: ./branch.sh <action> <branch_name>
# Actions: create, checkout

if [ -z "$1" ] || [ -z "$2" ]; then
    echo ""
    print_message_box "$RED" "Error" "Missing arguments" "Usage: $0 <create|checkout> <branch_name>"
    echo ""
    exit 1
fi

ACTION="$1"
BRANCH_NAME="$2"
ROOT_DIR=$(pwd)

echo ""
echo -e "${GRAY}${FULL_HLINE}${RESET}"
echo -e "${CYAN}Starting branch $ACTION...${RESET}"
echo -e "${GRAY}Branch: ${WHITE}$BRANCH_NAME${RESET}"
echo -e "${GRAY}${FULL_HLINE}${RESET}"
echo ""

git_branch() {
    local DIR="$1"

    if [ -d "$DIR" ]; then
        cd "$DIR" || { echo -e "${RED}Failed to enter $DIR${RESET}"; return; }

        # Check if it is a git repository
        if [ -d ".git" ] || git rev-parse --git-dir > /dev/null 2>&1; then
            echo -e "${YELLOW}❯ ${WHITE}Processing ${CYAN}${DIR}${RESET}"
            
            if [ "$ACTION" == "create" ]; then
                # Create branch (checks if it already exists to avoid error)
                if git show-ref --verify --quiet "refs/heads/$BRANCH_NAME"; then
                    echo -e "  ${YELLOW}! Branch '$BRANCH_NAME' already exists${RESET}"
                else
                    git checkout -b "$BRANCH_NAME" > /dev/null 2>&1
                    echo -e "  ${GREEN}✓ Created local branch${RESET}"
                    
                    if [ -n "$(git remote)" ]; then
                        git push --set-upstream origin "$BRANCH_NAME" > /dev/null 2>&1
                        if [ $? -eq 0 ]; then
                            echo -e "  ${GREEN}✓ Pushed upstream${RESET}"
                        else
                            echo -e "  ${RED}✗ Failed to push upstream${RESET}"
                        fi
                    fi
                fi
            elif [ "$ACTION" == "checkout" ]; then
                # Checkout branch
                # Check if branch exists (local or remote)
                if git show-ref --verify --quiet "refs/heads/$BRANCH_NAME" || \
                   git show-ref --verify --quiet "refs/remotes/origin/$BRANCH_NAME"; then
                    
                    git checkout "$BRANCH_NAME" > /dev/null 2>&1
                    if [ $? -eq 0 ]; then
                        echo -e "  ${GREEN}✓ Checked out${RESET}"
                    else
                        echo -e "  ${RED}✗ Checkout failed${RESET}"
                    fi
                else
                    echo -e "  ${YELLOW}! Warning: Branch '$BRANCH_NAME' does not exist in this repo${RESET}"
                fi
            else
                echo -e "  ${RED}Invalid action: $ACTION. Use 'create' or 'checkout'.${RESET}"
            fi
        fi
        
        # Return to root directory
        cd "$ROOT_DIR" || return
    fi
}

# Process sub-repositories (like infra) found by find command
# This covers both submodules (if initialized) and manual sub-repos
find . -maxdepth 2 -name ".git" | while read git_dir; do
    repo_dir=$(dirname "$git_dir")
    # Skip current directory (.) to avoid double processing (it's handled at the end)
    if [ "$repo_dir" != "." ] && [ "$repo_dir" != "./." ]; then
        # Remove ./ prefix if present for cleaner output
        clean_dir=${repo_dir#./}
        git_branch "$clean_dir"
    fi
done

# Process root repository
git_branch "."

echo ""
print_message_box "$GREEN" "Success!" "Branch process finished" "All repositories processed."
echo ""
