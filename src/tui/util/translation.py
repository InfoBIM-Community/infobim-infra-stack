import os
import yaml
from typing import Any, Optional
from stack.src.tui.util.path import get_config_path

def get_translated_message(config: dict, key_path: str, default: str) -> str:
    """
    Retrieves a translated message based on the configuration language.
    
    Args:
        config: The configuration dictionary containing language and template settings.
        key_path: Dot-separated path to the translation key (e.g., "exception.message.not_found").
        default: Fallback message if translation is missing.
        
    Returns:
        The translated string or the default message.
    """
    lang = config.get("language", "en")
    
    # Resolve translation path
    # We need config path to resolve relative template path
    try:
        config_path = get_config_path()
        config_dir = os.path.dirname(config_path)
        
        template_rel_path = config.get("template", {}).get("path", "")
        if not template_rel_path:
            # Fallback if template path is not configured
            return default
            
        template_path = os.path.join(config_dir, template_rel_path)
        translation_dir = os.path.join(template_path, "translation")
        
        translation_file = os.path.join(translation_dir, f"{lang}.yaml")
        
        # Fallback to English if specific language file doesn't exist
        if not os.path.exists(translation_file) and lang != "en":
            translation_file = os.path.join(translation_dir, "en.yaml")
        
        if not os.path.exists(translation_file):
            return default
            
        with open(translation_file, 'r') as f:
            translations = yaml.safe_load(f)
            
        # Traverse the key path
        value = translations
        for key in key_path.split('.'):
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return default
                
        if value is None or not isinstance(value, str):
            return default
            
        return value
    except Exception:
        return default
