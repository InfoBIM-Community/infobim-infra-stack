
from typing import Any, Dict, List
from abc import ABC, abstractmethod


class IfcFileResourcePropertySetPort(ABC):
    """Port for IfcFileResourcePropertySet."""
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the name of the property set.

        Returns:
            str: The property set name.
        """
        pass

    @property
    @abstractmethod
    def properties(self) -> Dict[str, Any]:
        """Get the properties of the property set.

        Returns:
            Dict[str, Any]: The properties.
        """
        pass


class IfcFileResourceElementUnitOfMeasurementPort(ABC):
    """Port for IfcFileResourceElementUnitOfMeasurement."""
    @property
    @abstractmethod
    def Dimensions(self) -> Any:
        """The dimensional exponents of the SI base units by which the named unit is defined.
        
        Returns:
            Any: The dimensions (IfcDimensionalExponents).
        """
        pass

    @property
    @abstractmethod
    def UnitType(self) -> str:
        """The type of the unit.
        
        Returns:
            str: The unit type (IfcUnitEnum).
        """
        pass


class IfcFileResourceElementPort(ABC):
    """Port for IfcFileResourceElement."""
    @property
    @abstractmethod
    def type(self) -> str:
        """Get the element type of the IFC file.

        Returns:
            str: The element type name.
        """
        pass

    @property
    @abstractmethod
    def attributes(self) -> Dict[str, Any]:
        """Get the attributes of the IFC file.

        Returns:
            Dict[str, Any]: The attributes.
        """
        pass

    @property
    @abstractmethod
    def propertySets(self) -> Dict[str, IfcFileResourcePropertySetPort]:
        """Get the property sets of the IFC file.

        Returns:
            Dict[str, IfcFileResourcePropertySetPort]: The property sets.
        """
        pass

    @property
    @abstractmethod
    def units(self) -> List[IfcFileResourceElementUnitOfMeasurementPort]:
        """Get the units of the IFC file.

        Returns:
            List[IfcFileResourceElementUnitOfMeasurementPort]: A list of units.
        """
        pass

class IfcFileResourcePort(ABC):
    """Port for IfcFileResource."""
    @property
    @abstractmethod
    def schema(self) -> str:
        """Get the schema of the IFC file.

        Returns:
            str: The schema name.
        """
        pass

    @property
    @abstractmethod
    def application(self) -> str:
        """Get the application of the IFC file.

        Returns:
            str: The application name.
        """
        pass
    
    @property
    @abstractmethod
    def author(self) -> str:
        """Get the author of the IFC file. 

        Returns:
            str: The author name.
        """
        pass

    @property
    @abstractmethod
    def Project(self) -> IfcFileResourceElementPort:
        """Get the project of the IFC file.

        Returns:
            IfcFileResourceElementPort: The project element.
        """
        pass

    @property
    @abstractmethod
    def Site(self) -> Dict[str, IfcFileResourceElementPort]:
        """Get the sites of the IFC file.

        Returns:
            Dict[str, IfcFileResourceElementPort]: A dictionary of sites indexed by GlobalId.
        """
        pass

    @property
    @abstractmethod
    def Building(self) -> Dict[str, IfcFileResourceElementPort]:
        """Get the buildings of the IFC file.

        Returns:
            Dict[str, IfcFileResourceElementPort]: A dictionary of buildings indexed by GlobalId.
        """
        pass

    @property
    @abstractmethod
    def units(self) -> List[IfcFileResourceElementUnitOfMeasurementPort]:
        """Get the units of the IFC file.

        Returns:
            List[IfcFileResourceElementUnitOfMeasurementPort]: A list of units.
        """
        pass

    @abstractmethod
    def is_valid_schema_class(self, name: str) -> bool:
        """Check if the name is a valid class in the IFC schema.

        Args:
            name (str): The class name to check.

        Returns:
            bool: True if valid, False otherwise.
        """
        pass

    @abstractmethod
    def get_elements_by_type(self, type_name: str) -> Dict[str, IfcFileResourceElementPort]:
        """Get elements by IFC type.

        Args:
            type_name (str): The IFC type name.

        Returns:
            Dict[str, IfcFileResourceElementPort]: A dictionary of elements.
        """
        pass

    def __getattr__(self, name: str) -> Dict[str, IfcFileResourceElementPort]:
        """
        Dynamic access to IFC elements by type name.
        Example: resource.IfcWall returns all walls.
        """
        if self.is_valid_schema_class(name):
            return self.get_elements_by_type(name)

        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
