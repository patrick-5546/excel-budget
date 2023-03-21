from argparse import Namespace, _SubParsersAction

from excelbudget.commands.abstractcommand import AbstractCommand


class Generate(AbstractCommand):
    """The `generate` command implementation."""

    @staticmethod
    def configure_args(subparsers: _SubParsersAction) -> None:
        """Configures the argument parser for the `generate` command.

        Args:
            subparsers (_SubParsersAction): The command `subparsers`.
        """
        parser = subparsers.add_parser(
            "generate", aliases=["g"], help="generate a new excelbudget file"
        )
        parser.set_defaults(init=Generate)

        # positional arguments
        parser.add_argument("path", help="path to generate file")

        # optional arguments
        parser.add_argument(
            "-f", "--force", action="store_true", help="overwrite file if it exists"
        )

    def __init__(self, args: Namespace) -> None:
        raise NotImplementedError

    def run(self) -> None:
        raise NotImplementedError
