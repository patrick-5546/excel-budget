"""Tests the commands infrastructure: everything besides run and trivial methods."""

from argparse import Namespace
from contextlib import nullcontext as does_not_raise
from typing import ContextManager, NamedTuple, Type

import pytest

import xlbudget.commands as commands
from xlbudget.inputformat import BMO_CC


class CommandSpecs(NamedTuple):
    class_: Type[commands.Command]
    args: Namespace


COMMAND_ARGS = {
    "path": commands.Command.default_path,
    "trial": True,
}
COMMANDS = [
    CommandSpecs(class_=commands.Generate, args=Namespace(force=True, **COMMAND_ARGS)),
    CommandSpecs(
        class_=commands.Update,
        args=Namespace(input="statement-2022.csv", format=BMO_CC, **COMMAND_ARGS),
    ),
]
COMMAND_INSTS = [c.class_(c.args) for c in COMMANDS]
COMMAND_CLASS_ATTRIBUTES = [
    "name",
    "aliases",
]


def test_default_path() -> None:
    assert commands.Command.default_path.lower().endswith(
        ".xlsx"
    ), f"{commands.Command.default_path} should be an XLSX file"


@pytest.mark.parametrize(
    "path,expectation",
    [
        # raises `ValueError` when `path` is not a XLSX file
        ("test.txt", pytest.raises(ValueError)),
        ("test/", pytest.raises(ValueError)),
        ("test", pytest.raises(ValueError)),
        # raises `FileNotFoundError` if `path` is not in an existing directory
        ("test/test.xlsx", pytest.raises(FileNotFoundError)),
        ("tests/test/test.xlsx", pytest.raises(FileNotFoundError)),
        # otherwise does not raise any error
        ("test.xlsx", does_not_raise()),
    ],
)
def test_command__check_path(path: str, expectation: ContextManager) -> None:
    with expectation:
        commands.Command._check_path(path)


def test_get_command_classes() -> None:
    # check that the output of get_command_classes() == `COMMANDS`
    command_classes = commands.get_command_classes()
    commands_classes = [c.class_ for c in COMMANDS]
    assert len(command_classes) == len(commands_classes), "length mismatch"
    for cmd in command_classes:
        assert cmd in commands_classes, f"{cmd} not found"


def test_command_class_attributes() -> None:
    # in the current implementation, they are the abstract properties of `Command`
    command_class_attributes = [
        name
        for name in commands.Command.__abstractmethods__
        if isinstance(getattr(commands.Command, name), property)
    ]
    # check that `command_class_attributes == `COMMAND_CLASS_ATTRIBUTES`
    assert len(command_class_attributes) == len(
        COMMAND_CLASS_ATTRIBUTES
    ), "length mismatch"
    for cmd in command_class_attributes:
        assert cmd in COMMAND_CLASS_ATTRIBUTES, f"{cmd} not found"


@pytest.mark.parametrize("cmd_cls_attr", COMMAND_CLASS_ATTRIBUTES)
def test_abstract_class_attributes(cmd_cls_attr: str) -> None:
    """The current implementation of abstract class attributes requires two methods
    to be defined: an abstract property and a getter function.
    - The existence of the abstract property is implicitly tested by the definition of
        `command_class_attributes` in `test_command_class_attributes()`
    - The existence of the getter function is explicitly tested by this function
    """
    getter = f"get_{cmd_cls_attr}"
    assert hasattr(commands.Command, getter), f"{getter} isn't an attribute"
    assert callable(getattr(commands.Command, getter)), f"{getter} isn't an method"


@pytest.mark.parametrize("cmd_cls_attr", COMMAND_CLASS_ATTRIBUTES)
@pytest.mark.parametrize("cmd_inst", COMMAND_INSTS)
def test_class_attributes(cmd_cls_attr: str, cmd_inst: commands.Command) -> None:
    assert hasattr(
        cmd_inst, cmd_cls_attr
    ), f"{cmd_cls_attr} isn't an attribute of {cmd_inst}"
    attr = getattr(cmd_inst, cmd_cls_attr)
    assert not callable(attr), f"{cmd_cls_attr} is a method of {cmd_inst}"
    assert (
        attr == getattr(cmd_inst, f"get_{cmd_cls_attr}")()
    ), f"{cmd_cls_attr} class variable doesn't match getter in {cmd_inst}"


@pytest.mark.parametrize("cmd_inst", COMMAND_INSTS)
def test_name(cmd_inst: commands.Command) -> None:
    assert cmd_inst.get_name().isalpha(), f"{cmd_inst} isn't alphabetic"
    assert cmd_inst.get_name().islower(), f"{cmd_inst} isn't lowercase"


@pytest.mark.parametrize("cmd_inst", COMMAND_INSTS)
def test_aliases(cmd_inst: commands.Command) -> None:
    assert len(cmd_inst.get_aliases()) == 1, f"{cmd_inst} aliases length isn't 1"
    assert len(cmd_inst.get_aliases()[0]) == 1, f"{cmd_inst} alias length isn't 1"


@pytest.mark.parametrize(
    "input,expectation",
    [
        # raises `ValueError` when `input` is not a CSV file
        ("test.txt", pytest.raises(ValueError)),
        ("test/", pytest.raises(ValueError)),
        ("test", pytest.raises(ValueError)),
        # raises `ValueError` if `input` is not in an existing file
        ("test/test.csv", pytest.raises(ValueError)),
        ("tests/test/test.csv", pytest.raises(ValueError)),
        # otherwise does not raise any error
        ("statement-2022.csv", does_not_raise()),
    ],
)
def test_update__check_input(input: str, expectation: ContextManager) -> None:
    with expectation:
        commands.Update._check_input(input)
