# from argparse import ArgumentParser, _SubParsersAction
from abc import ABC, abstractmethod
from argparse import _SubParsersAction


class AbstractCommand(ABC):
    @staticmethod
    @abstractmethod
    def configure_args(subparsers: _SubParsersAction) -> None:
        pass

    @abstractmethod
    def __init__(self, configuration) -> None:
        pass

    @abstractmethod
    def execute(self) -> None:
        pass
