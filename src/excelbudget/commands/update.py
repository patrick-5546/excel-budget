from argparse import Namespace, _SubParsersAction
from typing import List

from excelbudget.commands.abstractcommand import AbstractCommand, common_arg_config


class Update(AbstractCommand):
    """The `update` command implementation.

    Attributes:
        name (str): The command's CLI name.
        aliases (List[str]): The command's CLI aliases.
    """

    name: str = "update"
    aliases: List[str] = ["u"]

    @classmethod
    def configure_args(cls, subparsers: _SubParsersAction) -> None:
        """Configures the argument parser for the `update` command.

        Args:
            subparsers (_SubParsersAction): The command `subparsers`.
        """
        common_arg_config(
            subparsers,
            name=cls.name,
            aliases=cls.aliases,
            help="update an existing excelbudget file",
            init=Update,
        )

    def __init__(self, args: Namespace) -> None:
        pass

    def run(self) -> None:
        raise NotImplementedError
