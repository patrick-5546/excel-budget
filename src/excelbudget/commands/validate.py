from argparse import Namespace, _SubParsersAction

from excelbudget.commands.abstractcommand import AbstractCommand


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
        parser.set_defaults(init=Validate)

        # positional arguments
        parser.add_argument("path", help="path to file")

    def __init__(self, args: Namespace) -> None:
        raise NotImplementedError

    def run(self) -> None:
        raise NotImplementedError
