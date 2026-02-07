
import os
import math
import argparse
from rich.console import Console
from typing import Dict, Any, Optional
from stack.src.lib.core.capability.executor import CapabilityExecutor
from stack.src.tui.terminal.adapter.table_view import TableViewAdapter
from stack.src.lib.core.capability import CapabilityMetadata, Capability
from stack.src.plugin.capability.base.list_pipes import ListPipesCapability
from stack.src.lib.core.capability.cli_strategy import CapabilityCliStrategy


class ListSewagePipesCliStrategy(CapabilityCliStrategy):
    """
    CLI Strategy for ListSewagePipesCapability.
    Includes specific columns for Slopes and conditional formatting (Red/Yellow alerts).
    """

    def __init__(self, default_ifc_path: Optional[str] = None):
        self.default_ifc_path = default_ifc_path

    I18N = {
        "en": {
            "title": "Sewage Pipe List",
            "col_guid": "GlobalId",
            "col_name": "Name",
            "col_dn": "Nominal Diameter (mm)",
            "col_material": "Material",
            "col_z_start": "Start Elevation (m)",
            "col_z_end": "End Elevation (m)",
            "col_length": "Length (m)",
            "col_slope_uhc": "UHC Slope (%)",
            "col_slope_real": "Actual Slope (%)",
            "success": "Success! Found {count} pipes.",
            "executing": "Executing capability...",
            "running": "Running ListSewagePipesCapability on:",
            "error": "Error executing capability:"
        },
        "pt_BR": {
            "title": "Lista de Tubos de Esgoto",
            "col_guid": "GlobalId",
            "col_name": "Nome",
            "col_dn": "DN (mm)",
            "col_material": "Material",
            "col_z_start": "Cota Inicial (m)",
            "col_z_end": "Cota Final (m)",
            "col_length": "Comprimento (m)",
            "col_slope_uhc": "Declividade UHC (%)",
            "col_slope_real": "Declividade Real (%)",
            "success": "Sucesso! Encontrados {count} tubos.",
            "executing": "Executando capability...",
            "running": "Executando ListSewagePipesCapability em:",
            "error": "Erro ao executar capability:"
        }
    }

    def get_text(self, key, lang="en"):
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
        
        if args.show_guid and getattr(cap, "supports_global_id", False):
            columns.append((self.get_text("col_guid", lang), {"style": "dim", "width": 24, "no_wrap": True}))

        columns.extend([
            (self.get_text("col_name", lang), {"style": "cyan"}),
            (self.get_text("col_dn", lang), {"justify": "right"}),
            (self.get_text("col_material", lang), {"style": "dim"}),
            (self.get_text("col_z_start", lang), {"justify": "right"}),
            (self.get_text("col_z_end", lang), {"justify": "right"}),
            (self.get_text("col_length", lang), {"justify": "right"}),
            (self.get_text("col_slope_uhc", lang), {"justify": "right"}),
            (self.get_text("col_slope_real", lang), {"justify": "right"}),
        ])

        table = TableViewAdapter.create_table(
            title=self.get_text("title", lang),
            columns=columns
        )
        
        for row in pipes:
            # Logic for styling
            len_val = row["length"]
            len_style = "red" if len_val > 15.0 else ""
            len_str = f"[{len_style}]{len_val:.2f}[/{len_style}]" if len_style else f"{len_val:.2f}"
            
            s_real = row.get("slope_real", 0.0)
            s_uhc = row.get("slope_uhc", 0.0)
            
            slope_style = ""
            if s_uhc > 0:
                if s_real < (s_uhc - 0.1):
                    slope_style = "red"
                elif s_real > (s_uhc + 0.1):
                    slope_style = "yellow"
            
            slope_real_str = f"[{slope_style}]{s_real:.2f}[/{slope_style}]" if slope_style else f"{s_real:.2f}"
            
            dn_disp = f"{int(row['dn'])}"
            uhc_disp = f"{s_uhc:.1f}" if s_uhc else "-"
            
            row_values = []
            if args.show_guid and getattr(cap, "supports_global_id", False):
                row_values.append(row["guid"])

            row_values.extend([
                row["name"],
                dn_disp,
                row["material"],
                f"{row['z_start']:.2f}",
                f"{row['z_end']:.2f}",
                len_str,
                uhc_disp,
                slope_real_str
            ])
            
            table.add_row(*row_values)
            
        console.print(table)


class ListSewagePipesCapability(ListPipesCapability):
    
    METADATA = CapabilityMetadata(
        id="infobim.capability.list_sewage_pipes",
        version="1.0.0",
        name="List Sewage Pipes",
        description="Extracts sewage pipes with specific slopes (Real vs UHC/NBR8160).",
        author="InfoBIM Team",
        tags=["ifc", "pipes", "sewage", "extraction", "reporting"],
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
                    "description": "Total number of sewage pipes found"
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
                            "length": {"type": "number"},
                            "slope_uhc": {"type": "number", "description": "Minimum slope defined by NBR8160 (%)"},
                            "slope_real": {"type": "number", "description": "Actual geometric slope (%)"}
                        }
                    }
                }
            }
        }
    )

    def get_default_cli_strategy(self, **kwargs) -> Optional[Any]:
        return ListSewagePipesCliStrategy(**kwargs)

    def _process_pipe(self, pipe, unit_scale) -> Dict[str, Any]:
        """
        Extend base processing to add Slope Real and Slope UHC.
        """
        # Get base data
        data = super()._process_pipe(pipe, unit_scale)
        if not data:
            return None
            
        psets = data.pop("psets", {}) # Retrieve and remove psets from final output if not needed, or keep?
        # We can keep psets if we want, but let's just use it here.
        
        # 1. Slope UHC
        slope_uhc = 0.0
        if "Pset_BR_NBR8160" in psets and "MinimalSlope" in psets["Pset_BR_NBR8160"]:
            val = psets["Pset_BR_NBR8160"]["MinimalSlope"]
            if val: slope_uhc = float(val)
            
        # 2. Slope Real
        # We need geometry info. Base class provides z_start, z_end, length (in meters)
        # We can re-calculate using the raw data in `data` which is already scaled.
        z1 = data["z_start"]
        z2 = data["z_end"]
        # Length in data is also scaled.
        # However, to be precise, slope is usually calculated on the horizontal projection.
        # But if the pipe is not vertical, length ~ horizontal length for small slopes.
        # Let's use the logic: slope = abs(dz) / dist_2d * 100
        # We don't have dist_2d easily here without re-doing geometry math or assuming length^2 = dist_2d^2 + dz^2
        
        length = data["length"]
        slope_real = 0.0
        
        dz = abs(z1 - z2)
        if length > dz:
            dist_2d = math.sqrt(length**2 - dz**2)
            if dist_2d > 0.001:
                slope_real = dz / dist_2d * 100.0
        elif length > 0:
             # Fallback if length ~ dz (vertical pipe)
             slope_real = 0.0 # Or infinity? Usually 0 for listing purposes or handle vertical
             
        data["slope_uhc"] = slope_uhc
        data["slope_real"] = slope_real
        
        return data
