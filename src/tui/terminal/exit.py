
import os
import subprocess
from rich.align import Align
from rich.panel import Panel
from rich.console import Console
from stack.src.tui.util.path import get_message_box_script


def main(message: str = "Thank you for choosing InfoBIM!"):
    script_path = get_message_box_script()

    if os.path.exists(script_path):
        subprocess.run(["clear"])
        subprocess.run(["bash", script_path, "CYAN", "Info", "Exit", message])
    else:
        console = Console()
        console.clear()
        console.print(Panel(Align.center(f"\n{message}\n"), border_style="green"))
