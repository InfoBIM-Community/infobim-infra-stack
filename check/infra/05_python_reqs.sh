DESCRIPTION="Infra: Python Requirements"

REQ_FILE="$(dirname "${BASH_SOURCE[0]}")/requirements.txt"

check() {
    # Check for Colab environment
    IS_COLAB=false
    if [[ -f "infobim-ifc.env.yaml" ]] && grep -q "engine: colab" "infobim-ifc.env.yaml"; then
        IS_COLAB=true
    fi

    # If venv doesn't exist and not in Colab, we can't check
    if [ "$IS_COLAB" = false ] && [[ ! -f "venv/bin/python3" ]]; then
        return 1
    fi
    
    # If requirements file doesn't exist, fail
    if [[ ! -f "$REQ_FILE" ]]; then
        return 1
    fi

    PYTHON_CMD="./venv/bin/python3"
    if [ "$IS_COLAB" = true ]; then
        PYTHON_CMD="python3"
    fi

    # Use python to check installed packages
    $PYTHON_CMD -c "
import sys
import warnings
warnings.filterwarnings('ignore')
try:
    import pkg_resources
except ImportError:
    # setuptools not installed
    sys.exit(1)

try:
    with open('$REQ_FILE', 'r') as f:
        # Filter empty lines and comments
        reqs = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    # Check if requirements are satisfied
    pkg_resources.require(reqs)
except Exception:
    sys.exit(1)
"
}

hotfix() {
    # Check for Colab environment
    IS_COLAB=false
    if [[ -f "infobim-ifc.env.yaml" ]] && grep -q "engine: colab" "infobim-ifc.env.yaml"; then
        IS_COLAB=true
    fi

    if [ "$IS_COLAB" = false ] && [[ ! -f "venv/bin/python3" ]]; then
        echo "Virtual environment not found."
        return 1
    fi
    
    echo "Installing requirements..."
    PYTHON_CMD="./venv/bin/python3"
    if [ "$IS_COLAB" = true ]; then
        PYTHON_CMD="python3"
    fi

    $PYTHON_CMD -m pip install -r "$REQ_FILE"
}