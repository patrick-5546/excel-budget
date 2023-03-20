from argparse import _SubParsersAction

from excelbudget.commands.abstractcommand import AbstractCommand
from excelbudget.state import State


class Generate(AbstractCommand):
    """The `generate` command implementation."""

    @staticmethod
    def configure_args(subparsers: _SubParsersAction) -> None:
        """Configures the argument parser for the `generate` command.

        Args:
            subparsers (_SubParsersAction): The command `subparsers`.
        """
        parser = subparsers.add_parser(
            "generate", help="generate a new excelbudget file"
        )

        # positional arguments
        parser.add_argument("path", help="path to generate file")

        # optional arguments
        parser.add_argument(
            "-f", "--force", action="store_true", help="overwrite file if it exists"
        )

    def __init__(self, state: State) -> None:
        raise NotImplementedError

    def execute(self) -> None:
        raise NotImplementedError
