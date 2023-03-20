from argparse import _SubParsersAction

from excelbudget.commands.abstractcommand import AbstractCommand
from excelbudget.state import State


class Update(AbstractCommand):
    """The `update` command implementation."""

    @staticmethod
    def configure_args(subparsers: _SubParsersAction) -> None:
        """Configures the argument parser for the `update` command.

        Args:
            subparsers (_SubParsersAction): The command `subparsers`.
        """
        parser = subparsers.add_parser(
            "update", help="update an existing excelbudget file"
        )

        # positional arguments
        parser.add_argument("path", help="path to file")

    def __init__(self, state: State) -> None:
        raise NotImplementedError

    def run(self) -> None:
        raise NotImplementedError
