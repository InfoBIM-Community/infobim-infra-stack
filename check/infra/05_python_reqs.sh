DESCRIPTION="Infra: Python Requirements"

REQ_FILE="$(dirname "${BASH_SOURCE[0]}")/requirements.txt"

check() {
    # If venv doesn't exist, we can't check
    if [[ ! -f "venv/bin/python3" ]]; then
        return 1
    fi
    
    # If requirements file doesn't exist, fail
    if [[ ! -f "$REQ_FILE" ]]; then
        return 1
    fi

    # Use python to check installed packages
    ./venv/bin/python3 -c "
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
    if [[ ! -f "venv/bin/python3" ]]; then
        echo "Virtual environment not found."
        return 1
    fi
    
    echo "Installing requirements..."
    ./venv/bin/python3 -m pip install -r "$REQ_FILE"
}