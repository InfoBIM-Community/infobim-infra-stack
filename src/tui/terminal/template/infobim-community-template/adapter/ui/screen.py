
import os
import sys
import tty
import yaml
import time
import threading
import select
import termios
from rich.live import Live
from typing import Any, Dict
from rich.panel import Panel
from rich.align import Align
from rich.spinner import Spinner
from rich.tree import Tree
from stack.src.tui.terminal.exit import main as exit_main
from rich.console import Console, ConsoleOptions, RenderResult
from stack.src.tui.core.port.ui.screen import TerminalScreenPort, TerminalScreenOptionsPort, TerminalScreenContentPort, TerminalScreenSpinnerPort, TerminalScreenTreeContentPort


class TerminalScreenSpinnerAdapter(TerminalScreenSpinnerPort):
    def __init__(self, message: str):
        self._spinner = Spinner("material", text=message)

    def show(self, message: str) -> None:
        self._spinner.update(text=message)

    def hide(self) -> None:
        pass

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        yield Align.center(self._spinner)


class TerminalScreenOptionsAdapter(TerminalScreenOptionsPort):
    def __init__(self, translations: dict = None):
        self._translations = translations or {}

    def render(self, *args, **kwargs) -> str:
        exit_label = self._translations.get("exit", {}).get("label", "Exit")
        return f"[cyan]ESC[/] [dim]{exit_label}[/]"


class TerminalScreenContentAdapter(TerminalScreenContentPort):
    def render(self, **kwargs) -> Any:
        # Filter out known control parameters first
        filtered_kwargs = {
            k: v for k, v in kwargs.items() 
            if k not in ['work', 'duration']
        }

        if len(filtered_kwargs.keys()) == 0:
            return "No content to display."
        elif len(filtered_kwargs.keys()) == 1:
            return filtered_kwargs[list(filtered_kwargs.keys())[0]]
        else:
            adapters: Dict[str, Any] = {}
            for param_key, param_value in filtered_kwargs.items():
                if param_value is None:
                    continue
                elif isinstance(param_value, (str, int, float)):
                    continue
                elif callable(param_value):
                    continue
                else:
                    adapters[param_key] = param_value

            if len(adapters.keys()) == 1:
                return adapters[list(adapters.keys())[0]]

            return f"Multiple content items provided. Please provide only one. Number of items provided: {len(adapters.keys())}"


class TerminalScreenTreeContentAdapter(TerminalScreenTreeContentPort):
    def __init__(self, tree_adapter: Any = None):
        self.tree_adapter = tree_adapter

    def render(self, **kwargs) -> Any:
        # Use provided tree_adapter or fall back to kwargs
        tree_obj = self.tree_adapter or kwargs.get('tree')
        
        if tree_obj:
             # If it's an IfcFileTreeAdapter, use it to build the tree
             # It might have build_tree (legacy/direct) or we use our own builder
             if hasattr(tree_obj, 'build_tree'):
                 return tree_obj.build_tree()
             
             # Fallback: Build tree ourselves using data from adapter
             return self._build_tree_from_adapter(tree_obj)
             
        return "No tree content provided."

    def _build_tree_from_adapter(self, adapter: Any) -> Any:
        """Builds and returns a Rich Tree representation of the IFC files.
        
        Args:
            adapter: The adapter providing access to files.
            
        Returns:
            Tree: The rich Tree object.
        """
        files = []
        if hasattr(adapter, 'get_files'):
            files = adapter.get_files()
        elif hasattr(adapter, '_repository') and hasattr(adapter._repository, 'list_files'):
             # Fallback to accessing repository directly if get_files missing
             files = adapter._repository.list_files()
             
        tree = Tree("📁 IFC Files")
        
        # Simple flat structure for now, or nested if paths contain slashes
        for file_path in files:
            parts = file_path.split('/')
            current_node = tree
            
            # Navigate/Create branches
            for part in parts[:-1]:
                found = False
                for child in current_node.children:
                    if str(child.label) == f"📂 {part}": # Check against formatted label
                        current_node = child
                        found = True
                        break
                if not found:
                    current_node = current_node.add(f"📂 {part}")
            
            # Add file leaf
            current_node.add(f"📄 {parts[-1]}")
            
        return tree


class TerminalScreenAdapter(TerminalScreenPort):
    def __init__(self, title: str = ">_ [blue]InfoBIM[/]", subtitle: str = None):
        self._title: str = title
        self._subtitle: str = subtitle
        self._console: Console = Console()
        self._translations = self._load_translations()

    def _load_translations(self) -> dict:
        try:
            # base_dir is infobim-community-template root
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            
            # Find global config to determine language
            # We are at stack/src/tui/terminal/template/infobim-community-template/adapter/ui/screen.py
            # Global config is at stack/src/tui/config.yaml
            # ../../../../../config.yaml
            global_config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../config.yaml"))
            
            lang_code = "en"
            if os.path.exists(global_config_path):
                try:
                    with open(global_config_path, 'r') as f:
                        config = yaml.safe_load(f)
                        lang_code = config.get("language", "en")
                except Exception:
                    lang_code = "en"

            translation_dir = os.path.join(base_dir, "translation")
            translation_file = os.path.join(translation_dir, f"{lang_code}.yaml")
            
            if os.path.exists(translation_file):
                 with open(translation_file, 'r') as f:
                     return yaml.safe_load(f)
            
            # Fallback to en if specific lang not found
            if lang_code != "en":
                  translation_file = os.path.join(translation_dir, "en.yaml")
                  if os.path.exists(translation_file):
                      with open(translation_file, 'r') as f:
                          return yaml.safe_load(f)

            return {
                "exit": {
                    "label": "Exit",
                    "thank_you": "Thank you for choosing InfoBIM!"
                },
                "exception": {
                    "message": {
                        "ifc_engine_not_found": "IFC engine not found. Let's set it up."
                    }
                }
            }
        except Exception:
            return {
                "exit": {
                    "label": "Exit",
                    "thank_you": "Thank you for choosing InfoBIM!"
                },
                "exception": {
                    "message": {
                        "ifc_engine_not_found": "IFC engine not found. Let's set it up."
                    }
                }
            }

    @property
    def title(self) -> str:
        return self._title

    @property
    def subtitle(self) -> str:
        return self._subtitle

    @property
    def template_author(self) -> str:
        return 'Elias M. P. Junior'

    @property
    def footer_options(self) -> TerminalScreenOptionsPort:
        return TerminalScreenOptionsAdapter(self._translations)

    @property
    def content(self) -> TerminalScreenContentPort:
        return TerminalScreenContentAdapter()

    def render(self, *args, **kwargs) -> None:
        # Prepare content
        content_obj = self.content.render(*args, **kwargs)
        duration = kwargs.get('duration', None)
        work = kwargs.get('work', None)
        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        
        should_exit = False
        thank_you_msg = ""
        start_time = time.time()
        
        # Start background work if provided
        work_result = None
        work_thread = None
        work_done_time = None
        
        if work:
            def work_wrapper():
                nonlocal work_result
                try:
                    work_result = work()
                except Exception as e:
                    work_result = e
            
            work_thread = threading.Thread(target=work_wrapper)
            work_thread.daemon = True
            work_thread.start()

        try:
            tty.setcbreak(fd)
            with Live(
                self._get_screen_panel(content_obj),
                console=self._console,
                screen=True,
                refresh_per_second=20
            ) as live:
                while True:
                    current_time = time.time()
                    
                    # Logic for work-based duration + 5s delay
                    if work_thread:
                        if not work_thread.is_alive():
                            if work_done_time is None:
                                work_done_time = current_time
                            elif current_time - work_done_time > 2.0:
                                break
                    # Fallback to simple duration if no work
                    elif duration is not None:
                        if current_time - start_time > duration:
                            break

                    # Check for input
                    if select.select([sys.stdin], [], [], 0.02)[0]:
                        ch = sys.stdin.read(1)
                        if ord(ch) == 27: # ESC
                            should_exit = True
                            thank_you_msg = self._translations.get("exit", {}).get("thank_you", "Thank you for choosing InfoBIM!")
                            break
                    
                    pass
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            
        if should_exit:
            exit_main(thank_you_msg)
            
        # If we had a work result (and didn't exit via ESC), return it if caller expects it?
        # But render returns None in signature. 
        # The caller might need the result.
        # We can attach it to the console object or return it if we change signature.
        # Given the interface, we might need a way to pass it back.
        # For now, let's assume the work function has side effects or updates an external object.
        # But looking at usage, we are initializing an adapter.
        # We can update the passed mutable object or...
        # Let's change signature of render to return Any? The interface says None.
        # However, Python allows returning value even if type hint says None (at runtime).
        return work_result

    def _get_screen_panel(self, content: str) -> Panel:
        return Panel(
            content,
            title=self.title,
            subtitle=self.footer_options.render(),
            title_align="center",
            subtitle_align="left",
            padding=(2, 4),
            expand=True,
        )
