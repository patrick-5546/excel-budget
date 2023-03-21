from argparse import Namespace, _SubParsersAction

from excelbudget.commands.abstractcommand import AbstractCommand


class Update(AbstractCommand):
    """The `update` command implementation."""

    @staticmethod
    def configure_args(subparsers: _SubParsersAction) -> None:
        """Configures the argument parser for the `update` command.

        Args:
            subparsers (_SubParsersAction): The command `subparsers`.
        """
        parser = subparsers.add_parser(
            "update", aliases=["u"], help="update an existing excelbudget file"
        )
        parser.set_defaults(init=Update)

        # positional arguments
        parser.add_argument("path", help="path to file")

    def __init__(self, args: Namespace) -> None:
        raise NotImplementedError

    def run(self) -> None:
        raise NotImplementedError
