
from typing import Any, Dict
from abc import ABC, abstractmethod


class TerminalScreenOptionsPort(ABC):
    """
    Port defining the interface for screen footer options.
    """
    @abstractmethod
    def render(self, *args, **kwargs) -> str:
        """
        Renders the footer options as a string.
        """
        pass


class TerminalScreenContentPort(ABC):
    """
    Port defining the interface for screen content.
    """
    @abstractmethod
    def render(self, *args, **kwargs) -> str:
        """
        Renders the content as a string (or renderable object).
        """
        pass


class TerminalScreenSpinnerPort(ABC):
    """
    Port defining the interface for a loading spinner.
    """
    @abstractmethod
    def show(self, message: str) -> None:
        """
        Show the spinner with a message.
        """
        pass

    @abstractmethod
    def hide(self) -> None:
        """
        Hide the spinner.
        """
        pass


class TerminalScreenPort(ABC):
    @property
    @abstractmethod
    def title(self) -> str:
        """
        Returns the title of the screen.
        """
        pass

    @property
    @abstractmethod
    def subtitle(self) -> str:
        """
        Returns the subtitle of the screen.
        """
        pass

    @property
    @abstractmethod
    def template_author(self) -> str:
        """
        Returns the author of the screen.
        """
        pass

    @property
    @abstractmethod
    def footer_options(self) -> TerminalScreenOptionsPort:
        """
        Returns the footer options of the screen.
        """
        pass

    @property
    @abstractmethod
    def content(self) -> TerminalScreenContentPort:
        """
        Returns the content of the screen.
        """
        pass

    @abstractmethod
    def render(self, *args, **kwargs) -> None:
        """
        Renders the screen.
        """
        pass


class TerminalScreenTreeContentPort(TerminalScreenContentPort):
    """
    Port defining the interface for screen tree content.
    """
    pass
