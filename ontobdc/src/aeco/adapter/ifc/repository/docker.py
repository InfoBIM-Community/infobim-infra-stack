

from ontobdc.src.aeco.adapter.ifc.repository.local import LocalIfcFileRepositoryAdapter


class DockerIfcFileRepositoryAdapter(LocalIfcFileRepositoryAdapter):
    """Adapter for accessing IFC files inside a Docker container."""

    def __init__(self):
        """Initialize the adapter.
        
        Args:
            root_path (str): The root directory to search for files.
        """
        self._root_path = '/incoming'
