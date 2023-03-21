import inspect
from typing import Type

import pytest

from excelbudget.commands import (
    Command,
    Generate,
    Update,
    Validate,
    get_command_classes,
)

AVAILABLE_COMMANDS = {
    Generate,
    Update,
    Validate,
}


@pytest.mark.parametrize("cmd_cls", AVAILABLE_COMMANDS)
def test_command_config_args_is_classmethod(cmd_cls: Type[Command]) -> None:
    assert isinstance(inspect.getattr_static(cmd_cls, "configure_args"), classmethod)


def test_get_command_classes() -> None:
    command_classes = get_command_classes()

    assert len(command_classes) == len(AVAILABLE_COMMANDS)
    for cmd in command_classes:
        assert cmd in AVAILABLE_COMMANDS
