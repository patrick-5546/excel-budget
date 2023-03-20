# from argparse import ArgumentParser, _SubParsersAction
from abc import ABC, abstractmethod
from argparse import _SubParsersAction

from excelbudget.configure import Configuration


class AbstractCommand(ABC):
    @staticmethod
    @abstractmethod
    def configure_args(subparsers: _SubParsersAction) -> None:
        pass

    @abstractmethod
    def __init__(self, configuration: Configuration) -> None:
        pass

    @abstractmethod
    def execute(self) -> None:
        pass
