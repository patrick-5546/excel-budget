import argparse
import logging
import typing

logger = logging.getLogger(__name__)


class State(typing.NamedTuple):
    args: argparse.Namespace


def setup_state(pre_config) -> State:
    args = pre_config.parser.parse_args()

    state = State(
        args=args,
    )
    return state
