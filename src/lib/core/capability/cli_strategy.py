
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from argparse import ArgumentParser
from rich.console import Console
from stack.src.lib.core.capability import Capability


class CapabilityCliStrategy(ABC):
    """
    Strategy interface for handling CLI execution and visualization of a Capability.
    This allows the CLI behavior to be decoupled from the Capability logic,
    and enables dependency injection of different visualization strategies.
    """

    @abstractmethod
    def setup_parser(self, parser: ArgumentParser) -> None:
        """
        Configures the argument parser with capability-specific arguments.
        """
        pass

    @abstractmethod
    def run(self, console: Console, args: Any, capability: Capability) -> None:
        """
        Executes the capability using the provided arguments and console.
        Handles the entire flow: Input preparation -> Execution -> Output rendering.
        """
        pass
