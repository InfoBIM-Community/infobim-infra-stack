
from rich.tree import Tree
from ontobdc.src.aeco.core.port.ifc.tree import IfcFileTreePort
from ontobdc.src.aeco.core.port.ifc.repository import IfcFileRepositoryPort


class IfcFileTreeAdapter(IfcFileTreePort):
    """Adapter for creating a Rich Tree from IFC files."""
    
    def __init__(self, repository: IfcFileRepositoryPort):
        """Initialize the adapter.
        
        Args:
            repository (IfcFileRepositoryPort): The repository to fetch files from.
        """
        self._repository: IfcFileRepositoryPort = repository

    def get_files(self) -> list[str]:
        """Get the list of IFC files.
        
        Returns:
            list[str]: List of file paths.
        """
        return self._repository.list_files()

