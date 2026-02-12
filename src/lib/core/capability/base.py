
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from .metadata import CapabilityMetadata


class Capability(ABC):
    """
    The fundamental unit of functionality in InfoBIM.
    
    A Capability is a cataloged, versioned, and executable unit of logic
    that transforms inputs into outputs within the ecosystem.
    """
    
    def __init__(self, metadata: CapabilityMetadata = None):
        if metadata is None and hasattr(self, 'METADATA'):
            metadata = self.METADATA
            
        if metadata is None:
            raise ValueError(f"Capability {self.__class__.__name__} must have metadata defined either via constructor or METADATA class attribute.")
            
        self.metadata = metadata

    def get_default_cli_strategy(self) -> Optional[Any]:
        """
        Returns the default CLI strategy for this capability.
        Returns None by default, meaning no CLI support is provided out-of-the-box.
        Type is Any to avoid circular import with CapabilityCliStrategy, but implementers
        should return an instance of CapabilityCliStrategy.
        """
        return None

    @abstractmethod
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the capability logic.
        
        Args:
            inputs: A dictionary of input parameters.
            
        Returns:
            A dictionary of execution results/outputs.
        """
        pass

    def check(self, inputs: Dict[str, Any]) -> bool:
        """
        Lifecycle hook: Validates inputs before execution.
        Checks for language support if 'lang' is provided.
        
        Args:
            inputs: A dictionary of input parameters.
            
        Returns:
            bool: True if inputs are valid, False otherwise.
            
        Raises:
            ValueError: If the requested language is not supported.
        """
        lang = inputs.get("lang")
        # print(f"DEBUG: Checking language '{lang}' against supported {self.metadata.supported_languages}")
        if lang:
            if lang not in self.metadata.supported_languages:
                raise ValueError(
                    f"Language '{lang}' not supported by capability '{self.metadata.name}'. "
                    f"Supported: {self.metadata.supported_languages}"
                )
        return True

    def validate(self, outputs: Dict[str, Any]) -> None:
        """
        Lifecycle hook: Validates outputs after execution.
        
        Args:
            outputs: A dictionary of execution results/outputs.
            
        Raises:
            ValueError: If outputs are invalid.
        """
        pass

    @property
    def info(self) -> Dict[str, Any]:
        """Return capability information."""
        return self.metadata.__dict__
