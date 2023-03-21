"""The configuration for excelbudget.

Warning: Logger usage in this file

    The logger can only be used after `_configure_logger` is called in
    `post_state_configuration`
"""

import logging
from argparse import ArgumentParser
from typing import NamedTuple

from excelbudget.commands import AbstractCommand, get_cmd_cls_from_str
from excelbudget.state import State

logger = logging.getLogger(__name__)


class PreStateConfiguration(NamedTuple):
    """A named tuple containing items that can be configured before state is set up.

    Attributes:
        parser (ArgumentParser): The argument parser.
    """

    parser: ArgumentParser


def pre_state_configuration() -> PreStateConfiguration:
    """Configuration before state is setup.

    Returns:
        A[n] `PreStateConfiguration` containing configured items.
    """
    parser = _configure_argument_parser()

    config = PreStateConfiguration(
        parser=parser,
    )
    return config


def post_state_configuration(state: State) -> None:
    """Configuration after state is set up.

    Args:
        state (State): The state.
    """
    _configure_logger(state.args.log_level)
    logger.info(f"{state=}")  # log state after `_configure_logger` is called


def _configure_argument_parser() -> ArgumentParser:
    """Configures the argument parser for all arguments.

    Returns:
        A[n] `ArgumentParser` configured for this package.
    """
    parser = ArgumentParser()

    parser.add_argument("-p", "--path", help="path to the excelbudget file")

    _configure_logger_args(parser)

    cmd_subparsers = parser.add_subparsers(
        title="command",
        required=True,
        description="The excelbudget command to run.",
    )
    for cls in AbstractCommand.__subclasses__():
        cmd_cls = get_cmd_cls_from_str(cls.__name__)
        cmd_cls.configure_args(cmd_subparsers)

    return parser


def _configure_logger_args(parser: ArgumentParser) -> None:
    """Configures the argument parser for logger arguments.
    The log level configuration was adapted from
    [this Stack Overflow answer](https://stackoverflow.com/a/20663028).

    Args:
        parser (ArgumentParser): The argument parser to update.
    """
    group_log = parser.add_argument_group(
        "logger configuration",
        description="Arguments that override the default logger configuration.",
    )
    group_log_lvl = group_log.add_mutually_exclusive_group()
    group_log_lvl.add_argument(
        "-d",
        "--debug",
        help="print lots of debugging statements; can't use with -v/--verbose",
        action="store_const",
        dest="log_level",
        const=logging.DEBUG,
        default=logging.WARNING,
    )
    group_log_lvl.add_argument(
        "-v",
        "--verbose",
        help="be verbose; can't use with -d/--debug",
        action="store_const",
        dest="log_level",
        const=logging.INFO,
    )


def _configure_logger(level: int) -> None:
    """Configures the logger.

    Since this configuration is global, there is no need to return the logger.
    To use the logger in a file, add `logger = logging.getLogger(__name__)` at the top.

    Args:
        level (int): The [logging level](https://docs.python.org/3/library/logging.html#logging-levels).
    """  # noqa
    logging.basicConfig(
        level=level,
        format="%(name)s:%(funcName)s() - %(levelname)s - %(message)s",
    )
