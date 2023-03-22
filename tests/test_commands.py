import argparse
import inspect
import os
from typing import Type

import pytest

import xlbudget.commands as commands

AVAILABLE_COMMANDS = {
    commands.Generate,
    commands.Update,
}


@pytest.mark.parametrize("cmd_cls", AVAILABLE_COMMANDS)
def test_command_config_args_is_classmethod(cmd_cls: Type[commands.Command]) -> None:
    assert isinstance(inspect.getattr_static(cmd_cls, "configure_args"), classmethod)


def test_generate_file_exists() -> None:
    test_file = ".test_generate_file_exists"

    parser = argparse.ArgumentParser()
    parser.set_defaults(path=test_file, force=False)
    args = parser.parse_args([])
    cmd = commands.Generate(args)

    assert not os.path.exists(
        test_file
    ), f"File {test_file} exists, delete before running"

    open(test_file, "w").close()
    with pytest.raises(FileExistsError):
        cmd.run()
    os.remove(test_file)


def test_get_command_classes() -> None:
    command_classes = commands.get_command_classes()

    assert len(command_classes) == len(AVAILABLE_COMMANDS)
    for cmd in command_classes:
        assert cmd in AVAILABLE_COMMANDS
