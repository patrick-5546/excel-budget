import argparse
import inspect

import pytest

from excelbudget.commands.generate import Generate
from excelbudget.configure import Configuration


def test_config_args_static() -> None:
    """Check if `config_args` is static
    as this is not guaranteed by the current implementation.
    """
    assert isinstance(inspect.getattr_static(Generate, "configure_args"), staticmethod)


def test_generate() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    Generate.configure_args(subparsers)
    args = parser.parse_args(["generate", ".", "--force"])

    config = Configuration(args=args)
    with pytest.raises(NotImplementedError):
        Generate(config)
