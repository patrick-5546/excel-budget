"""The setup and configuration for xlbudget.

Warning: Logger usage in this file

    The logger can only be used after `_configure_logger` is called in `setup`.
"""

import logging
from argparse import ArgumentParser, Namespace

from .commands import get_command_classes


def setup() -> Namespace:
    """Package-level setup and configuration.

    Returns:
        A[n] `Namespace` containing the parsed CLI arguments.
    """
    parser = _configure_argument_parser()
    args = parser.parse_args()
    _configure_logger(args.log_level)

    # log args after call to _configure_logger
    logger = logging.getLogger(__name__)
    logger.info(args)

    return args


def _configure_argument_parser() -> ArgumentParser:
    """Configures the argument parser for all arguments.

    Returns:
        A[n] `ArgumentParser` configured for this package.
    """
    parser = ArgumentParser()

    parser.add_argument(
        "-p", "--path", help="path to the xlbudget file", default="xlbudget.xlsx"
    )

    _configure_logger_args(parser)

    cmd_subparsers = parser.add_subparsers(
        title="command",
        required=True,
        description="The xlbudget command to run.",
    )
    for cmd_cls in get_command_classes():
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
