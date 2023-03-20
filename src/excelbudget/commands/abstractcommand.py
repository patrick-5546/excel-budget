# from argparse import ArgumentParser, _SubParsersAction
from abc import ABC, abstractmethod
from argparse import _SubParsersAction

from excelbudget.state import State


class AbstractCommand(ABC):
    """The abstract class that the commands inherit."""

    @staticmethod
    @abstractmethod
    def configure_args(subparsers: _SubParsersAction) -> None:
        pass

    @staticmethod
    @abstractmethod
    def __init__(self, state: State) -> None:
        pass

    @abstractmethod
    def execute(self) -> None:
        pass
