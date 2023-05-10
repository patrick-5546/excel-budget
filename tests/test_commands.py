import inspect
from typing import Type

import pytest

import xlbudget.commands as commands

AVAILABLE_COMMANDS = {
    commands.Generate,
    commands.Update,
}


@pytest.mark.parametrize("cmd_cls", AVAILABLE_COMMANDS)
def test_config_args(cmd_cls: Type[commands.Command]) -> None:
    # each command class should implement configure_args() as a classmethod
    assert isinstance(inspect.getattr_static(cmd_cls, "configure_args"), classmethod)


def test_get_command_classes() -> None:
    # the output of get_command_classes() should be the same as `AVAILABLE_COMMANDS`
    command_classes = commands.get_command_classes()
    assert len(command_classes) == len(AVAILABLE_COMMANDS)
    for cmd in command_classes:
        assert cmd in AVAILABLE_COMMANDS
