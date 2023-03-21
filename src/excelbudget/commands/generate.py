from argparse import Namespace, _SubParsersAction
from typing import List

from excelbudget.commands.abstractcommand import AbstractCommand, common_arg_config


class Generate(AbstractCommand):
    """The `generate` command implementation.

    Attributes:
        name (str): The command's CLI name.
        aliases (List[str]): The command's CLI aliases.
    """

    name: str = "generate"
    aliases: List[str] = ["g"]

    @classmethod
    def configure_args(cls, subparsers: _SubParsersAction) -> None:
        """Configures the argument parser for the `generate` command.

        Args:
            subparsers (_SubParsersAction): The command `subparsers`.
        """
        parser = common_arg_config(
            subparsers,
            name=cls.name,
            aliases=cls.aliases,
            help="generate a new excelbudget file",
            init=Generate,
        )

        parser.add_argument(
            "-f", "--force", action="store_true", help="overwrite file if it exists"
        )

    def __init__(self, args: Namespace) -> None:
        pass

    def run(self) -> None:
        raise NotImplementedError
