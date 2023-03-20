"""The state of excelbudget.

Notes:

- The logger shouldn't be used in this file because it hasn't been configured yet
"""

import argparse
import logging
import typing

logger = logging.getLogger(__name__)


class State(typing.NamedTuple):
    """A named tuple containing items that make up the state of the program.

    Attributes:
        args (argparse.Namespace): The parsed arguments.
    """

    args: argparse.Namespace


def setup_state(config) -> State:
    """Sets up the state for the program.

    Args:
        config (configure.PreStateConfiguration): The configuration before state is set up.

    Returns:
        A[n] `State` containing items that are set up.
    """
    args = config.parser.parse_args()

    state = State(
        args=args,
    )
    return state
