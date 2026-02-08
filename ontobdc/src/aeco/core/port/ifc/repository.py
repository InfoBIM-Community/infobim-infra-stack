
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class IfcFileRepositoryPort(ABC):
    """Port for accessing IFC files repository."""
    
    @property
    @abstractmethod
    def base_path(self) -> str:
        """Get the base path of the repository.
        
        Returns:
            str: The base path of the repository.
        """
        pass
    
    @abstractmethod
    def list_files(self) -> List[str]:
        """List all available IFC files in the repository.
        
        Returns:
            List[str]: A list of file paths relative to the repository root.
        """
        pass
    
    @abstractmethod
    def get_file_content(self, file_path: str) -> str:
        """Get the content of a specific IFC file.
        
        Args:
            file_path (str): The relative path to the file.
            
        Returns:
            str: The content of the file.
        """
        pass
