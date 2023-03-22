"""The commands, implemented as implementations of the abstract class `Command`."""

import sys
from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace, _SubParsersAction
from logging import getLogger
from typing import List, Type

logger = getLogger(__name__)


class Command(ABC):
    """The abstract class that the command implementations implement.

    Attributes:
        path (str): The path to the xlbudget file.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """The command's CLI name. Should be implemented as a class attribute"""
        pass

    @property
    @abstractmethod
    def aliases(self) -> List[str]:
        """The command's CLI aliases. Should be implemented as a class attribute"""
        pass

    @classmethod
    @abstractmethod
    def configure_args(cls, subparsers: _SubParsersAction) -> None:
        """Adds the command's CLI arguments to the argument parser.

        Args:
            subparsers (_SubParsersAction): The command `subparsers`.
        """
        pass

    @abstractmethod
    def __init__(self, args: Namespace) -> None:
        """Initializes the command instance, storing the relevant CLI arguments as
        instance variables.

        Args:
            args (Namespace): The CLI arguments.
        """
        self.path = args.path

    @abstractmethod
    def run(self) -> None:
        """Runs the command."""
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
            cls=Generate,
        )

        parser.add_argument(
            "-f", "--force", action="store_true", help="overwrite file if it exists"
        )

    def __init__(self, args: Namespace) -> None:
        super().__init__(args)
        self.force = args.force

        logger.info(f"instance variables: {vars(self)}")

    def run(self) -> None:
        raise NotImplementedError


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
            cls=Update,
        )

    def __init__(self, args: Namespace) -> None:
        pass

    def run(self) -> None:
        raise NotImplementedError


class Validate(Command):
    """The `validate` command validates an existing xlbudget file.

    Attributes: Class Attributes
        name (str): The command's CLI name.
        aliases (List[str]): The command's CLI aliases.
    """

    name: str = "validate"
    aliases: List[str] = ["v"]

    @classmethod
    def configure_args(cls, subparsers: _SubParsersAction) -> None:
        """Configures the argument parser for the `validate` command.

        Args:
            subparsers (_SubParsersAction): The command `subparsers`.
        """
        _add_parser(
            subparsers,
            name=cls.name,
            aliases=cls.aliases,
            help="validate an existing xlbudget file",
            cls=Validate,
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
    return [getattr(command_module, cls.__name__) for cls in Command.__subclasses__()]


def _add_parser(
    subparsers: _SubParsersAction,
    name: str,
    aliases: List[str],
    help: str,
    cls: Type[Command],
) -> ArgumentParser:
    """Adds an argument parser for a command. Any configuration that is common
    across commands should go here.

    Args:
        subparsers (_SubParsersAction): The subparsers object.
        name (str): The command name.
        aliases (List[str]): The command aliases.
        help (str): The command help message.
        cls (Type[Command]): The command class.

    Returns:
        A[n] `ArgumentParser` for a command.
    """
    parser = subparsers.add_parser(name, aliases=aliases, help=help)

    # initialize the command with args.init(...)
    parser.set_defaults(init=cls)

    return parser
