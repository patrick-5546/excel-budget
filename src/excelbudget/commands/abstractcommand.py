# from argparse import ArgumentParser, _SubParsersAction
from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace, _SubParsersAction
from typing import List, Type


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


def common_arg_config(
    subparsers: _SubParsersAction,
    name: str,
    aliases: List[str],
    help: str,
    init: Type[AbstractCommand],
) -> ArgumentParser:
    parser = subparsers.add_parser(name, aliases=aliases, help=help)
    parser.set_defaults(init=init)
    return parser
