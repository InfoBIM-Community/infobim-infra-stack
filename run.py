#!/usr/bin/env python3
import sys
import os
import argparse
from rich.console import Console

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../"))
if project_root not in sys.path:
    sys.path.append(project_root)

# Registry of capabilities
# TODO: In the future, this should be auto-discovered
from stack.src.plugin.capability.base.list_pipes import ListPipesCapability
from stack.src.plugin.capability.base.list_sewage_pipes import ListSewagePipesCapability

REGISTRY = {
    "infobim.capability.list_pipes": ListPipesCapability,
    "infobim.capability.list_sewage_pipes": ListSewagePipesCapability
}

def main():
    # 1. Parse just the capability_id first
    # We use parse_known_args because we don't know the capability's arguments yet
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("capability_id", help="ID of the capability to run")
    
    # We look for --help manually because add_help=False suppresses it,
    # but we want to show our help if no capability is provided.
    if "--json" in sys.argv:
        # Dump Catalog in JSON for Agents
        import json
        catalog = []
        for cid, cls in REGISTRY.items():
            meta = cls.METADATA
            # Convert dataclass to dict
            meta_dict = meta.__dict__.copy()
            catalog.append(meta_dict)
        print(json.dumps(catalog, indent=2, default=str))
        sys.exit(0)

    if "-h" in sys.argv or "--help" in sys.argv:
        # If capability_id is present, we let the capability handle help
        # If not, we show our help
        if len(sys.argv) == 2: # script + help
             print("Usage: infobim run <capability_id> [args...]")
             print("\nAvailable capabilities:")
             for key in REGISTRY.keys():
                 print(f"  - {key}")
             sys.exit(0)

    try:
        args, remaining_args = parser.parse_known_args()
    except SystemExit:
        # If argparse fails (e.g. missing capability_id), it exits.
        # We can add custom error handling here if needed.
        sys.exit(1)
    
    cap_class = REGISTRY.get(args.capability_id)
    if not cap_class:
        console = Console()
        console.print(f"[bold red]Error:[/bold red] Capability '{args.capability_id}' not found.")
        console.print("\n[dim]Available capabilities:[/dim]")
        for key in REGISTRY.keys():
            console.print(f"  - [cyan]{key}[/cyan]")
        sys.exit(1)
        
    # 2. Instantiate Capability
    cap = cap_class()
    
    # 3. Get Strategy
    strategy = cap.get_default_cli_strategy()
    
    if not strategy:
        print(f"The capability '{cap.metadata.name}' does not support CLI execution.")
        sys.exit(1)
        
    # 4. Setup Real Parser
    # We include capability_id again to not break parsing, but it's already consumed
    real_parser = argparse.ArgumentParser(
        description=f"Run {cap.metadata.name}",
        fromfile_prefix_chars='@' # Allow reading args from file (e.g. @args.txt)
    )
    real_parser.add_argument("capability_id", help="ID of the capability to run")
    
    strategy.setup_parser(real_parser)
    
    # 5. Parse All Args
    final_args = real_parser.parse_args()
    
    # 6. Run
    console = Console()
    strategy.run(console, final_args, cap)

if __name__ == "__main__":
    main()
