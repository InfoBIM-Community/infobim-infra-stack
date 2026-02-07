from typing import List, Tuple, Optional, Any
from rich.table import Table
from rich.box import Box

# Custom box with dashed separator lines
# Defines characters to render boxes.
# ┌─┬┐ top
# │ ││ head
# ├─┼┤ head_row
# │ ││ mid
# ├─┼┤ row
# ├─┼┤ foot_row
# │ ││ foot
# └─┴┘ bottom
DASHED_HORIZONTALS = Box(
    " ── \n"
    "    \n"
    " ── \n"
    "    \n"
    " ╌╌ \n"
    " ── \n"
    "    \n"
    " ── \n"
)

class TableViewAdapter:
    """
    Adapter for creating standardized Rich Tables with consistent styling.
    """

    @staticmethod
    def create_table(
        title: str,
        columns: List[Tuple[str, Any]],  # List of (name, style_options_dict or kwargs)
        show_header: bool = True,
        header_style: str = "bold white",
        border_style: str = "grey35"
    ) -> Table:
        """
        Creates a Rich Table with the project's standard styling (dashed lines, grey borders).

        Args:
            title (str): Table title.
            columns (List[Tuple[str, dict]]): List of columns to add. 
                Each item is a tuple: (Header Name, {style="...", justify="...", ...})
            show_header (bool): Whether to show the header. Defaults to True.
            header_style (str): Style for the header. Defaults to "bold white".
            border_style (str): Style for the border. Defaults to "grey35".

        Returns:
            Table: Configured Rich Table object.
        """
        table = Table(
            title=title,
            box=DASHED_HORIZONTALS,
            border_style=border_style,
            show_lines=True,
            show_header=show_header,
            header_style=header_style
        )

        for col_name, col_kwargs in columns:
            table.add_column(col_name, **col_kwargs)

        return table
