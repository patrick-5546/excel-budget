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


def test_command__check_xlbudget_path_invalid() -> None:
    # when not an XLSX file
    with pytest.raises(ValueError):
        commands.Command._check_xlbudget_path("test.xls")

    # when not in an existing directory
    new_dir = ".test_command__check_xlbudget_path"
    assert not os.path.exists(new_dir), f"Path {new_dir} exists, delete before running"
    with pytest.raises(FileNotFoundError):
        commands.Command._check_xlbudget_path(os.path.join(new_dir, "test.xlsx"))


@pytest.mark.parametrize("path", ["test.xlsx", os.path.join("tests", "tests.xlsx")])
def test_command__check_xlbudget_path_valid(path: str) -> None:
    print(path)
    try:
        commands.Command._check_xlbudget_path(path)
    except Exception as e:
        assert False, f"Path {path} raised an exception {e}"


def test_generate_file_exists() -> None:
    new_file = ".test_generate_file_exists.xlsx"

    parser = argparse.ArgumentParser()
    parser.set_defaults(path=new_file, force=False)
    args = parser.parse_args([])

    assert not os.path.exists(
        new_file
    ), f"Path {new_file} exists, delete before running"

    open(new_file, "w").close()
    with pytest.raises(FileExistsError):
        commands.Generate(args)
    os.remove(new_file)


def test_get_command_classes() -> None:
    command_classes = commands.get_command_classes()

    assert len(command_classes) == len(AVAILABLE_COMMANDS)
    for cmd in command_classes:
        assert cmd in AVAILABLE_COMMANDS
