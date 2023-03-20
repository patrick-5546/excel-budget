from argparse import _SubParsersAction

from excelbudget.commands.abstractcommand import AbstractCommand
from excelbudget.state import State


class Validate(AbstractCommand):
    @staticmethod
    def configure_args(subparsers: _SubParsersAction) -> None:
        parser = subparsers.add_parser(
            "validate", help="validate an existing excelbudget file"
        )

        parser.add_argument("path", help="path to file")

    def __init__(self, state: State) -> None:
        raise NotImplementedError

    def execute(self) -> None:
        raise NotImplementedError
