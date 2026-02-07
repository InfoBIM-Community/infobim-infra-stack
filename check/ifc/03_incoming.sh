#!/bin/bash

DESCRIPTION="Incoming Data Directory"

check() {
    if [ -d "data/incoming" ]; then
        return 0
    else
        return 1
    fi
}

hotfix() {
    mkdir -p "data/incoming"
    return $?
}

repair() {
    echo -e "      ${YELLOW}Please ensure 'data/incoming' directory exists.${RESET}"
}
