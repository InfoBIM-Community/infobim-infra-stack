import os
import yaml

def get_stack_root() -> str:
    """Returns the absolute path to the 'stack' directory."""
    # This file is at stack/src/util/path.py
    # stack root is at stack/
    # .. -> stack/src
    # .. -> stack
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

def get_message_box_script() -> str:
    """Returns the absolute path to the message_box.sh script."""
    return os.path.join(get_stack_root(), "message_box.sh")

def get_config_path():
    # Config is at stack/infobim-ifc.yaml
    return os.path.abspath(os.path.join(get_stack_root(), "infobim-ifc.yaml"))

def load_config():
    config_path = get_config_path()
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at {config_path}")
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)
