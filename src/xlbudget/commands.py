"""The commands, implemented as implementations of the abstract class `Command`."""

import datetime
import os
import sys
from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace, _SubParsersAction
from logging import getLogger
from typing import List, Type

from openpyxl import Workbook

import xlbudget.xlfunctions as xlf

logger = getLogger(__name__)


class Command(ABC):
    """The abstract class that the command implementations implement.

    Attributes: Class Attributes
        default_path (str): The default path of the xlbudget file.

    Attributes:
        path (str): The path to the xlbudget file.
    """

    default_path: str = "xlbudget.xlsx"

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def aliases(self) -> List[str]:
        pass

    @classmethod
    def configure_common_args(cls, parser: ArgumentParser) -> None:
        """Configures the arguments that are used by all commands.

        Args:
            parser (ArgumentParser): The argument parser.
        """
        parser.add_argument(
            "-p",
            "--path",
            help="path to the xlbudget file (default: %(default)s)",
            default=cls.default_path,
        )

    @classmethod
    @abstractmethod
    def configure_args(cls, subparsers: _SubParsersAction) -> None:
        pass

    @abstractmethod
    def __init__(self, args: Namespace) -> None:
        self._check_path(args.path)
        self.path = args.path

    @staticmethod
    def _check_path(path: str) -> None:
        """Check that `path` is a valid path to an xlbudget file.

        Args:
            path (str): The xlbudget path.

        Raises:
            ValueError: If `path` is not a path to an XLSX file.
            FileNotFoundError: If `path` is not in an existing directory.
        """
        xlsx_ext = ".xlsx"
        if not path.endswith(xlsx_ext):
            raise ValueError(f"Path '{path}' does not end with '{xlsx_ext}'")

        dir = os.path.dirname(path)
        if dir and not os.path.isdir(dir):
            raise FileNotFoundError(f"Directory '{dir}' does not exist")

    @abstractmethod
    def run(self) -> None:
        pass


class Generate(Command):
    """The `generate` command generates a new xlbudget file.

    Attributes: Class Attributes
        name (str): The command's CLI name.
        aliases (List[str]): The command's CLI aliases.

    Attributes:
        force (bool): If True and file exists, will overwrite it.
    """

    name: str = "generate"
    aliases: List[str] = ["g"]

    @classmethod
    def configure_args(cls, subparsers: _SubParsersAction) -> None:
        """Configures the argument parser for the `generate` command.

        Args:
            subparsers (_SubParsersAction): The command `subparsers`.
        """
        parser = _add_parser(
            subparsers,
            name=cls.name,
            aliases=cls.aliases,
            help="generate a new xlbudget file",
            cmd_cls=Generate,
        )

        parser.add_argument(
            "-f", "--force", action="store_true", help="overwrite file if it exists"
        )

    def __init__(self, args: Namespace) -> None:
        super().__init__(args)

        if not args.force and os.path.exists(self.path):
            raise FileExistsError(
                f"File {self.path} exists, run with -f/--force to overwrite"
            )

        logger.debug(f"instance variables: {vars(self)}")

    def run(self) -> None:
        """Creates an empty xlbudget file populated with:

        - A sheet for the current year.

        Raises:
            FileExistsError: If `self.force` is false and the file exists.
        """
        logger.info("generating an empty xlbudget file")

        wb = Workbook()
        year = str(datetime.date.today().year)
        logger.info(f"creating {year} sheet")
        xlf.create_year_sheet(wb, year)
        logger.info(f"saving to {self.path}")
        wb.save(self.path)


class Update(Command):
    """The `update` command updates an existing xlbudget file.

    Attributes: Class Attributes
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
        _add_parser(
            subparsers,
            name=cls.name,
            aliases=cls.aliases,
            help="update an existing xlbudget file",
            cmd_cls=Update,
        )

    def __init__(self, args: Namespace) -> None:
        pass

    def run(self) -> None:
        raise NotImplementedError


def get_command_classes() -> List[Type[Command]]:
    """Gets all classes that implement the `Command` abstract class.

    Returns:
        A[n] `List[Type[Command]]` of all command classes.
    """
    command_module = sys.modules[__name__]
    return [getattr(command_module, c.__name__) for c in Command.__subclasses__()]


def _add_parser(
    subparsers: _SubParsersAction,
    name: str,
    aliases: List[str],
    help: str,
    cmd_cls: Type[Command],
) -> ArgumentParser:
    """Adds an argument parser for a command. Any configuration that is common
    across commands should go here.

    Args:
        subparsers (_SubParsersAction): The subparsers object.
        name (str): The command name.
        aliases (List[str]): The command aliases.
        help (str): The command help message.
        cmd_cls (Type[Command]): The command class.

    Returns:
        A[n] `ArgumentParser` for a command.
    """
    parser = subparsers.add_parser(name, aliases=aliases, help=help)

    # initialize the command with args.init(...)
    parser.set_defaults(init=cmd_cls)

    return parser
