import argparse
import inspect

import pytest

from excelbudget.commands.update import Update


def test_config_args_is_classmethod() -> None:
    """Check if `config_args` is static
    as this is not guaranteed by the current implementation.
    """
    assert isinstance(inspect.getattr_static(Update, "configure_args"), classmethod)


def test_update() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    Update.configure_args(subparsers)
    args = parser.parse_args(["update"])

    with pytest.raises(NotImplementedError):
        Update(args)
