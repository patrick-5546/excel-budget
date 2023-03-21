import argparse
import inspect

import pytest

from excelbudget.commands.validate import Validate


def test_config_args_static() -> None:
    """Check if `config_args` is static
    as this is not guaranteed by the current implementation.
    """
    assert isinstance(inspect.getattr_static(Validate, "configure_args"), staticmethod)


def test_validate() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    Validate.configure_args(subparsers)
    args = parser.parse_args(["validate", "."])

    with pytest.raises(NotImplementedError):
        Validate(args)
