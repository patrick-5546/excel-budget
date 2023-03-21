# from argparse import ArgumentParser, _SubParsersAction
from abc import ABC, abstractmethod
from argparse import Namespace, _SubParsersAction


class AbstractCommand(ABC):
    """The abstract class that the commands inherit."""

    @staticmethod
    @abstractmethod
    def configure_args(subparsers: _SubParsersAction) -> None:
        pass

    @staticmethod
    @abstractmethod
    def __init__(self, args: Namespace) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass
