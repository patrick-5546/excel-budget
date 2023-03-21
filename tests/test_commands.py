import argparse
import inspect

import pytest

from excelbudget.commands import Generate, Update, Validate


def test_config_args_is_classmethod() -> None:
    """Check if `config_args` is static
    as this is not guaranteed by the current implementation.
    """
    assert isinstance(inspect.getattr_static(Generate, "configure_args"), classmethod)
    assert isinstance(inspect.getattr_static(Update, "configure_args"), classmethod)
    assert isinstance(inspect.getattr_static(Validate, "configure_args"), classmethod)


def test_generate() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    Generate.configure_args(subparsers)
    args = parser.parse_args(["generate", "--force"])
    cmd = Generate(args)

    with pytest.raises(NotImplementedError):
        cmd.run()


def test_update() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    Update.configure_args(subparsers)
    args = parser.parse_args(["update"])
    cmd = Update(args)

    with pytest.raises(NotImplementedError):
        cmd.run()


def test_validate() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    Validate.configure_args(subparsers)
    args = parser.parse_args(["validate"])
    cmd = Validate(args)

    with pytest.raises(NotImplementedError):
        cmd.run()
