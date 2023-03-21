"""The state of excelbudget.

Note: Logger usage in this file
    The logger shouldn't be used in this file because it hasn't been configured yet
"""

import logging
import typing
from argparse import Namespace

from excelbudget.commands.abstractcommand import AbstractCommand

logger = logging.getLogger(__name__)


class State(typing.NamedTuple):
    """A named tuple containing items that make up the state of the program.

    Attributes:
        args (Namespace): The parsed arguments.
        cmd (AbstractCommand): The command instance.
    """

    args: Namespace
    cmd: AbstractCommand


def setup_state(config) -> State:
    """Sets up the state for the program.

    Note: Statically typing `config`
        `config`, which is type `configure.PreStateConfiguration`, can't be statically
        typed in this file as it would cause a circular import

    Args:
        config (configure.PreStateConfiguration): The configuration before
            state is set up.

    Returns:
        A[n] `State` containing items that are set up.
    """
    args = config.parser.parse_args()
    cmd = args.init(args)

    state = State(
        args=args,
        cmd=cmd,
    )
    return state
