#!/bin/bash

DESCRIPTION="Docker Environment File (.env)"

ENV_FILE="stack/docker/compose/.env"

check() {
    if [ -f "$ENV_FILE" ]; then
        return 0
    else
        return 1
    fi
}

hotfix() {
    local ENV_DIR=$(dirname "$ENV_FILE")
    
    if [ ! -d "$ENV_DIR" ]; then
        mkdir -p "$ENV_DIR"
    fi
    
    # Defaults
    local PROJECT_NAME="infobim_project"
    local ENVIRONMENT="production"
    
    # Try to extract from infobim-ifc.yaml if available (basic extraction)
    # We can rely on python if needed, but for hotfix simple defaults are usually enough 
    # or we can assume ifc.sh context but we shouldn't depend on it too much inside the function logic 
    # unless we export variables.
    
    cat <<EOF > "$ENV_FILE"
PROJECT=$PROJECT_NAME
ENVIRONMENT=$ENVIRONMENT
EOF

    if [ -f "$ENV_FILE" ]; then
        return 0
    else
        return 1
    fi
}

repair() {
    echo -e "      ${YELLOW}Please create '$ENV_FILE' with PROJECT and ENVIRONMENT variables.${RESET}"
}
