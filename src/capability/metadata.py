from typing import List, Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class CapabilityMetadata:
    """Metadata defining a Capability."""
    id: str
    version: str
    name: str
    description: str
    documentation: Optional[str] = None
    author: Optional[str] = None
    tags: List[str] = None
    supported_languages: List[str] = None
    supported_ifc_formats: List[str] = None
    input_schema: Optional[Dict[str, Any]] = None
    output_schema: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.supported_languages is None:
            self.supported_languages = ["en"]
