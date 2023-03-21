# from argparse import ArgumentParser, _SubParsersAction
from abc import ABC, abstractmethod
from argparse import Namespace, _SubParsersAction
from typing import List


class AbstractCommand(ABC):
    """The abstract class that the commands inherit."""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def aliases(self) -> List[str]:
        pass

    @classmethod
    @abstractmethod
    def configure_args(cls, subparsers: _SubParsersAction) -> None:
        pass

    @abstractmethod
    def __init__(self, args: Namespace) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass
