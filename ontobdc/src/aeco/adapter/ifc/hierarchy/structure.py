from typing import List, Any
from ontobdc.src.aeco.adapters.ifc.element import IfcElementAdapter, IfcUnitAdapter
from ontobdc.src.aeco.ports.ifc import IfcFileResourceElementPort, IfcFileResourceElementUnitOfMeasurementPort


class IfcStructureElementAdapter(IfcElementAdapter):
    """Base class for spatial structure elements (Project, Site, Building, Storey)."""
    pass

class IfcProjectAdapter(IfcStructureElementAdapter):
    """Adapter for IfcProject."""
    @property
    def units(self) -> List[IfcFileResourceElementUnitOfMeasurementPort]:
        """Get the units of the IFC file.

        Returns:
            List[IfcFileResourceElementUnitOfMeasurementPort]: A list of units.
        """
        units = []
        # IfcProject has UnitsInContext (IfcUnitAssignment), which has Units
        if hasattr(self._entity, "UnitsInContext") and self._entity.UnitsInContext:
            if hasattr(self._entity.UnitsInContext, "Units"):
                units = self._entity.UnitsInContext.Units
        return [IfcUnitAdapter(unit) for unit in units]

class IfcSiteAdapter(IfcStructureElementAdapter):
    """Adapter for IfcSite."""
    pass

class IfcBuildingStoreyAdapter(IfcStructureElementAdapter):
    """Adapter for IfcBuildingStorey."""
    
    @property
    def Name(self) -> str:
        return getattr(self._entity, "Name", "Unnamed Storey")

    @property
    def GlobalId(self) -> str:
        return getattr(self._entity, "GlobalId", "No GlobalId")
        
    @property
    def Elevation(self) -> Any:
        return getattr(self._entity, "Elevation", None)
        
    @property
    def Description(self) -> str:
        return getattr(self._entity, "Description", "")

class IfcBuildingAdapter(IfcStructureElementAdapter):
    """Adapter for IfcBuilding."""
    @property
    def floors(self) -> List[IfcBuildingStoreyAdapter]:
        """Get the floors of the building.

        Returns:
            List[IfcBuildingStoreyAdapter]: A list of floors.
        """
        floors = []
        # Use IsDecomposedBy relationship to find building storeys
        if hasattr(self._entity, "IsDecomposedBy"):
            for rel in self._entity.IsDecomposedBy:
                if rel.is_a("IfcRelAggregates"):
                    for obj in rel.RelatedObjects:
                        if obj.is_a("IfcBuildingStorey"):
                            floors.append(obj)
                            
        return [IfcBuildingStoreyAdapter(floor, self._file_adapter) for floor in floors]
