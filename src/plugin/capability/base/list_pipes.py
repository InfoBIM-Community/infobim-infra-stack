
import os
import math
import argparse
import numpy as np
import ifcopenshell
import ifcopenshell.util.unit
from rich.console import Console
import ifcopenshell.util.element
import ifcopenshell.util.placement
from typing import Dict, Any, Tuple, Optional
from stack.src.lib.core.capability.executor import CapabilityExecutor
from stack.src.tui.terminal.adapter.table_view import TableViewAdapter
from stack.src.lib.core.capability import Capability, CapabilityMetadata
from stack.src.lib.core.capability.cli_strategy import CapabilityCliStrategy


class ListPipesCliStrategy(CapabilityCliStrategy):
    """
    Default CLI Strategy for ListPipesCapability.
    Handles argument parsing and Rich table output.
    """
    
    def __init__(self, default_ifc_path: Optional[str] = None):
        self.default_ifc_path = default_ifc_path

    I18N = {
        "en": {
            "title": "Generic Pipe List",
            "col_guid": "GlobalId",
            "col_name": "Name",
            "col_dn": "Nominal Diameter (mm)",
            "col_material": "Material",
            "col_z_start": "Start Elevation (m)",
            "col_z_end": "End Elevation (m)",
            "col_length": "Length (m)",
            "success": "Success! Found {count} pipes.",
            "executing": "Executing capability...",
            "running": "Running Generic ListPipesCapability on:",
            "error": "Error executing capability:"
        },
        "pt_BR": {
            "title": "Lista Genérica de Tubos",
            "col_guid": "GlobalId",
            "col_name": "Nome",
            "col_dn": "DN (mm)",
            "col_material": "Material",
            "col_z_start": "Cota Inicial (m)",
            "col_z_end": "Cota Final (m)",
            "col_length": "Comprimento (m)",
            "success": "Sucesso! Encontrados {count} tubos.",
            "executing": "Executando capability...",
            "running": "Executando Generic ListPipesCapability em:",
            "error": "Erro ao executar capability:"
        }
    }

    def get_text(self, key, lang="en"):
        # Default to English if lang not found, or key not found
        lang_dict = self.I18N.get(lang, self.I18N["en"])
        return lang_dict.get(key, key)

    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("ifc_path", nargs="?", default=self.default_ifc_path, help="Path to IFC file")
        parser.add_argument("--show-guid", action="store_true", help="Show GlobalId column")
        parser.add_argument("--lang", default="pt_BR", help="Language code (e.g. en, pt_BR)")

    def run(self, console: Console, args: Any, capability: Capability) -> None:
        ifc_path = args.ifc_path
        lang = args.lang

        if not ifc_path or not os.path.exists(ifc_path):
            console.print(f"[yellow]Warning: File not found: {ifc_path}[/yellow]")
            console.print("[dim]Please provide a valid IFC path as argument.[/dim]")
            console.print("\n[bold]Example:[/bold]")
            console.print(f"[dim]  ./infobim run {capability.metadata.id} ./data/incoming/examples/sewage_project.ifc[/dim]")
            console.print("\n")
            return

        console.print(f"[bold blue]{self.get_text('running', lang)}[/bold blue] {ifc_path}")

        executor = CapabilityExecutor()
        inputs = {"ifc_path": ifc_path}
        if lang:
            inputs["lang"] = lang
        
        try:
            with console.status(f"[bold green]{self.get_text('executing', lang)}"):
                result = executor.execute(capability, inputs)
        except Exception as e:
            console.print(f"[red]{self.get_text('error', lang)}[/red] {e}")
            return

        pipes = result["pipes"]
        console.print(f"[green]{self.get_text('success', lang).format(count=result['count'])}[/green]")

        self._render_table(console, pipes, args, capability)

    def _render_table(self, console: Console, pipes: list, args: Any, cap: Capability) -> None:
        lang = args.lang
        columns = []

        # Conditional GlobalId
        if args.show_guid and getattr(cap, "supports_global_id", False):
            columns.append((self.get_text("col_guid", lang), {"style": "dim", "width": 24, "no_wrap": True}))

        columns.extend([
            (self.get_text("col_name", lang), {"style": "cyan"}),
            (self.get_text("col_dn", lang), {"justify": "right"}),
            (self.get_text("col_material", lang), {"style": "dim"}),
            (self.get_text("col_z_start", lang), {"justify": "right"}),
            (self.get_text("col_z_end", lang), {"justify": "right"}),
            (self.get_text("col_length", lang), {"justify": "right"}),
        ])

        table = TableViewAdapter.create_table(
            title=self.get_text("title", lang),
            columns=columns
        )
        
        for row in pipes:
            len_val = row["length"]
            dn_disp = f"{int(row['dn'])}"
            
            row_values = []
            if args.show_guid and getattr(cap, "supports_global_id", False):
                row_values.append(row["guid"])

            row_values.extend([
                row["name"],
                dn_disp,
                row["material"],
                f"{row['z_start']:.2f}",
                f"{row['z_end']:.2f}",
                f"{len_val:.2f}"
            ])
            
            table.add_row(*row_values)
            
        console.print(table)



DOCS = """
# List Pipes Capability

Extracts and lists pipe segments with their geometric and property data.

## Features

- **Multi-Schema Support**: Works with both IFC4 (`IfcPipeSegment`) and IFC2X3 (`IfcFlowSegment`).
- **Smart DN Extraction**: Automatically detects units (meters vs mm) for Nominal Diameter.
- **Geometry Parsing**: Calculates true length and start/end elevations (Z) from local placement or axis representation.
- **Material Resolution**: Resolves material names from associations.

## Outputs

- `pipes`: List of dictionaries containing `guid`, `name`, `dn`, `material`, `z_start`, `z_end`, `length`.
- `count`: Total number of pipes found.
"""

class ListPipesCapability(Capability):

    METADATA = CapabilityMetadata(
        id="infobim.capability.list_pipes",
        version="1.0.0",
        name="List Pipes",
        description="Extracts and lists pipe segments with their geometric and property data (DN, Length, Z).",
        documentation=DOCS,
        author="Elias M. P. Junior",
        tags=["ifc", "pipes", "extraction", "reporting"],
        supported_languages=["en", "pt_BR"],
        supported_ifc_formats=["IFC2X3", "IFC4"],
        input_schema={
            "type": "object",
            "properties": {
                "ifc_path": {
                    "type": "string",
                    "description": "Absolute path to the IFC file"
                },
                "lang": {
                    "type": "string",
                    "enum": ["en", "pt_BR"],
                    "default": "en",
                    "description": "Language for output messages and columns"
                }
            },
            "required": ["ifc_path"]
        },
        output_schema={
            "type": "object",
            "properties": {
                "count": {
                    "type": "integer",
                    "description": "Total number of pipes found"
                },
                "pipes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "guid": {"type": "string"},
                            "name": {"type": "string"},
                            "dn": {"type": "number"},
                            "material": {"type": "string"},
                            "z_start": {"type": "number"},
                            "z_end": {"type": "number"},
                            "length": {"type": "number"}
                        }
                    }
                }
            }
        }
    )

    @property
    def supports_global_id(self) -> bool:
        """Indicates if this capability supports returning GlobalId."""
        return True

    def get_default_cli_strategy(self, **kwargs) -> Optional[Any]:
        return ListPipesCliStrategy(**kwargs)

    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the pipe listing logic.
        
        Args:
            inputs: Dict containing:
                - ifc_path (str): Path to the IFC file.
                
        Returns:
            Dict containing:
                - pipes (List[Dict]): List of extracted pipe data.
                - count (int): Number of pipes found.
        """
        # Input validation handled by check() lifecycle method
        ifc_path = inputs.get("ifc_path")
        
        ifc_file = ifcopenshell.open(ifc_path)
        unit_scale = ifcopenshell.util.unit.calculate_unit_scale(ifc_file)
        
        # Support both IFC4 and IFC2X3
        if ifc_file.schema == "IFC2X3":
            pipes = ifc_file.by_type("IfcFlowSegment")
        else:
            pipes = ifc_file.by_type("IfcPipeSegment")
            
        data = []
        
        for pipe in pipes:
            item_data = self._process_pipe(pipe, unit_scale)
            if item_data:
                data.append(item_data)
            
        # Sort: DN Desc, Name Asc
        data.sort(key=lambda x: (-x.get("dn", 0), x.get("name", "")))
        
        return {
            "pipes": data,
            "count": len(data)
        }

    def check(self, inputs: Dict[str, Any]) -> bool:
        """
        Checks if the inputs are valid for this capability.

        Args:
            inputs: Dict containing:
                - ifc_path (str): Path to the IFC file.

        Returns:
            bool: True if inputs are valid, False otherwise.
        """
        # Call base check for language validation
        try:
            super().check(inputs)
        except ValueError as e:
            raise e

        ifc_path = inputs.get("ifc_path")
        return ifc_path and os.path.exists(ifc_path)

    def validate(self, outputs: Dict[str, Any]) -> None:
        """
        Validates the outputs for this capability.
        
        Args:
            outputs: Dict containing:
                - pipes (List[Dict]): List of extracted pipe data.
                - count (int): Number of pipes found.
                
        Raises:
            ValueError: If outputs are invalid.
        """
        if not outputs or "pipes" not in outputs or "count" not in outputs:
            raise ValueError("Invalid outputs for ListPipesCapability.")
        
        pipes = outputs["pipes"]
        count = outputs["count"]
        
        if count != len(pipes):
            raise ValueError(f"Mismatch between count ({count}) and number of pipes ({len(pipes)}).")

    def _process_pipe(self, pipe, unit_scale) -> Dict[str, Any]:
        """
        Process a single pipe element. Can be overridden by subclasses.
        """
        name = pipe.Name if pipe.Name else "Unnamed"
        
        # Psets
        psets = ifcopenshell.util.element.get_psets(pipe)
        
        # 1. DN
        dn = 0.0
        
        # Check common Psets for NominalDiameter (IFC4 vs IFC2X3)
        dn_val = None
        if "Pset_PipeSegmentTypeCommon" in psets and "NominalDiameter" in psets["Pset_PipeSegmentTypeCommon"]:
            dn_val = psets["Pset_PipeSegmentTypeCommon"]["NominalDiameter"]
        elif "Pset_PipeCommon" in psets and "NominalDiameter" in psets["Pset_PipeCommon"]:
            dn_val = psets["Pset_PipeCommon"]["NominalDiameter"] # IFC2X3 common
            
        if dn_val:
            dn_float = float(dn_val)
            # Heuristic: If < 5.0, assume meters and convert to mm
            if dn_float < 5.0: 
                dn = dn_float * 1000.0
            else:
                dn = dn_float
        
        # 2. Material
        material = self._get_material_name(pipe)
        
        # 3. Geometry
        length, z_start, z_end = self._get_geometry_info(pipe)
        
        # Adjust Length unit if necessary (display in meters)
        length_m = length * unit_scale
        
        # Adjust Z to meters
        z_start_m = z_start * unit_scale
        z_end_m = z_end * unit_scale
        
        return {
            "guid": pipe.GlobalId,
            "name": name,
            "dn": dn,
            "material": material,
            "z_start": z_start_m,
            "z_end": z_end_m,
            "length": length_m,
            "psets": psets # Pass psets for subclasses to use without re-extracting
        }

    def _get_material_name(self, element) -> str:
        if hasattr(element, "HasAssociations"):
            for rel in element.HasAssociations:
                if rel.is_a("IfcRelAssociatesMaterial"):
                    mat = rel.RelatingMaterial
                    if mat.is_a("IfcMaterial"):
                        return mat.Name
                    elif mat.is_a("IfcMaterialLayerSetUsage"):
                        return "LayerSet" 
                    elif mat.is_a("IfcMaterialProfileSetUsage"):
                        return "ProfileSet"
        return "-"

    def _get_geometry_info(self, element) -> Tuple[float, float, float]:
        """
        Returns length, start_z, end_z
        """
        # 1. Get Length (Quantity or BBox or Pset)
        length = 0.0
        psets = ifcopenshell.util.element.get_psets(element)
        if "Qto_DistributionElement" in psets and "Length" in psets["Qto_DistributionElement"]:
            length = float(psets["Qto_DistributionElement"]["Length"])
        
        # 2. Get Endpoints for Z
        start_z = 0.0
        end_z = 0.0
        
        try:
            m = ifcopenshell.util.placement.get_local_placement(element.ObjectPlacement)
            
            # 1. Try to find Axis representation
            axis_rep = None
            body_rep = None
            
            if element.Representation:
                for rep in element.Representation.Representations:
                    if rep.RepresentationIdentifier == "Axis":
                        axis_rep = rep
                    elif rep.RepresentationIdentifier == "Body":
                        body_rep = rep
            
            length_geom = 0.0
            z1 = 0.0
            z2 = 0.0
            found_geom = False
            
            if axis_rep and axis_rep.Items:
                item = axis_rep.Items[0]
                if item.is_a("IfcPolyline"):
                    points = item.Points
                    pt_start = points[0].Coordinates
                    pt_end = points[-1].Coordinates
                    
                    def to_3d(pt):
                        return list(pt) + [0.0]*(3-len(pt))
                    
                    v_start = to_3d(pt_start) + [1.0]
                    v_end = to_3d(pt_end) + [1.0]
                    
                    w_start = m @ np.array(v_start)
                    w_end = m @ np.array(v_end)
                    
                    z1 = w_start[2]
                    z2 = w_end[2]
                    length_geom = math.dist(w_start[:3], w_end[:3])
                    found_geom = True
                    
            if not found_geom and body_rep and body_rep.Items:
                item = body_rep.Items[0]
                if item.is_a("IfcExtrudedAreaSolid"):
                    placement = item.Position
                    depth = item.Depth
                    direction = item.ExtrudedDirection.DirectionRatios
                    
                    m_ext = ifcopenshell.util.placement.get_axis2placement(placement)
                    m_combined = m @ m_ext
                    
                    v_start = [0.0, 0.0, 0.0, 1.0]
                    w_start = m_combined @ np.array(v_start)
                    
                    d_vec = np.array(list(direction) + [0.0])
                    d_norm = np.linalg.norm(d_vec[:3])
                    if d_norm > 0:
                        d_vec = d_vec / d_norm
                    
                    rot_mat = m_combined[:3, :3]
                    d_world = rot_mat @ d_vec[:3]
                    
                    w_end_3 = w_start[:3] + d_world * depth
                    
                    z1 = w_start[2]
                    z2 = w_end_3[2]
                    length_geom = depth
                    found_geom = True

            if found_geom:
                if length == 0.0:
                    length = length_geom
                return length, z1, z2
            
            z1 = m[2, 3]
            return length, z1, 0.0
                    
        except Exception as e:
            print(f"Error processing geometry for {element.GlobalId}: {e}")
            pass
        
        return length, 0.0, 0.0

