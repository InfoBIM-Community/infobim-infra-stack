
import os
from typing import List
from ontobdc.src.aeco.core.port.ifc.repository import IfcFileRepositoryPort


class LocalIfcFileRepositoryAdapter(IfcFileRepositoryPort):
    """Adapter for accessing IFC files from the local filesystem."""
    
    def __init__(self, root_path: str):
        """Initialize the adapter.
        
        Args:
            root_path (str): The root directory to search for files.
        """
        self._root_path = root_path

    @property
    def base_path(self) -> str:
        """Get the absolute path of a specific IFC file.
        
        Args:
            file_path (str): The relative path to the file.
            
        Returns:
            str: The absolute path of the file.
        """
        return self._root_path

    def list_files(self) -> List[str]:
        """List all available IFC files in the repository.
        
        Returns:
            List[str]: A list of file paths relative to the repository root.
        """
        if not os.path.exists(self._root_path):
            return []
            
        files = []
        for root, _, filenames in os.walk(self._root_path):
            for filename in filenames:
                if filename.lower().endswith(('.ifc', '.ifcxml', '.ifczip')):
                    full_path = os.path.join(root, filename)
                    rel_path = os.path.relpath(full_path, self._root_path)
                    files.append(rel_path)
        return sorted(files)

    def get_file_content(self, file_name: str) -> str:
        """Get the content of a specific IFC file.
        
        Args:
            file_name (str): The name of the file.
            
        Returns:
            str: The content of the file.
        """
        full_path = os.path.join(self._root_path, file_name)
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()

    def get_ifc_content(self, file_name: str) -> str:
        """Get the content of a specific IFC file.
        
        Args:
            file_name (str): The name of the file.
            
        Returns:
            str: The content of the file.
        """
        return self.get_file_content(file_name)
