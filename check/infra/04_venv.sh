DESCRIPTION="Infra: Virtual Environment (venv)"

check() {
    # Check for Colab environment
    if [[ -f "infobim-ifc.env.yaml" ]] && grep -q "engine: colab" "infobim-ifc.env.yaml"; then
        DESCRIPTION="Infra: Virtual Environment (Skipped: Colab Mode)"
        return 0
    fi

    if [[ -d "venv" && -f "venv/bin/activate" ]]; then
        return 0
    fi
    return 1
}

repair() {
    if [[ -f "infobim-ifc.env.yaml" ]] && grep -q "engine: colab" "infobim-ifc.env.yaml"; then
        echo "Colab detected. Skipping venv creation."
        return 0
    fi

    echo "Creating virtual environment..."
    if command -v python3 &>/dev/null; then
        python3 -m venv venv
    else
        echo "Python 3 is not installed. Cannot create venv."
    fi
}
