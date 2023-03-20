"""Package-level configuration."""

import argparse
import logging
import typing

logger = logging.getLogger(__name__)


class Configuration(typing.NamedTuple):
    args: argparse.Namespace


def configure() -> Configuration:
    parser = configure_argument_parser()
    args = parser.parse_args()

    # don't log anything before `configure_logger` is called
    configure_logger(args.log_level)

    configuration = Configuration(
        args=args,
    )
    logger.debug(f"{configuration = }")
    return configuration


def configure_logger(level: int) -> None:
    """Configures the logger using
    [`logging.basicConfig`](https://docs.python.org/3/library/logging.html#logging.basicConfig).

    Since this configuration is global, there is no need to return the logger.
    To use the logger in a file, add `logger = logging.getLogger(__name__)` at the top.

    Args:
        level (int): The [logging level](https://docs.python.org/3/library/logging.html#logging-levels).
    """  # noqa
    logging.basicConfig(
        level=level,
        format="%(name)s:%(funcName)s() - %(levelname)s - %(message)s",
    )


def configure_argument_parser() -> argparse.ArgumentParser:
    """Configures the argument parser using
    [`argparse.ArgumentParser`](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser).

    Returns:
        A[n] `argparse.ArgumentParser` configured for this package.
    """
    parser = argparse.ArgumentParser()

    configure_logger_args(parser)

    cmd_subparsers = parser.add_subparsers(
        title="command",
        dest="cmd",
        required=True,
        description="The excelbudget command to run.",
    )
    configure_generate_args(cmd_subparsers)
    configure_update_args(cmd_subparsers)
    configure_validate_args(cmd_subparsers)

    return parser


def configure_logger_args(parser: argparse.ArgumentParser) -> None:
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


def configure_generate_args(subparsers) -> None:
    parser = subparsers.add_parser("generate", help="generate a new excelbudget file")
    parser.add_argument("path", help="path to generate file")
    parser.add_argument("-f", "--force", type=bool, help="overwrite file if it exists")


def configure_update_args(subparsers) -> None:
    parser = subparsers.add_parser("update", help="update an existing excelbudget file")
    parser.add_argument("path", help="path to file")


def configure_validate_args(subparsers) -> None:
    parser = subparsers.add_parser(
        "validate", help="validate an existing excelbudget file"
    )
    parser.add_argument("path", help="path to file")
