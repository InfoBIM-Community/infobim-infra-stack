DESCRIPTION="Infra: Virtual Environment (venv)"
check() {
    if [[ -d "venv" && -f "venv/bin/activate" ]]; then
        return 0
    fi
    return 1
}

repair() {
    echo "Creating virtual environment..."
    if command -v python3 &>/dev/null; then
        python3 -m venv venv
    else
        echo "Python 3 is not installed. Cannot create venv."
    fi
}
