from argparse import _SubParsersAction

from excelbudget.commands.abstractcommand import AbstractCommand
from excelbudget.state import State


class Validate(AbstractCommand):
    """The `validate` command implementation."""

    @staticmethod
    def configure_args(subparsers: _SubParsersAction) -> None:
        """Configures the argument parser for the `validate` command.

        Args:
            subparsers (_SubParsersAction): The command `subparsers`.
        """
        parser = subparsers.add_parser(
            "validate", aliases=["v"], help="validate an existing excelbudget file"
        )

        # positional arguments
        parser.add_argument("path", help="path to file")

    def __init__(self, state: State) -> None:
        raise NotImplementedError

    def run(self) -> None:
        raise NotImplementedError
