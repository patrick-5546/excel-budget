import argparse
import logging

import pytest

import xlbudget.configure as configure


def test__configure_logger_args() -> None:
    parser = argparse.ArgumentParser()
    configure._configure_logger_args(parser)

    # -d/--debug should set log level to debug
    args = parser.parse_args(["--debug"])
    assert args.log_level == logging.DEBUG

    # -v/--verbose should set log level to verbose
    args = parser.parse_args(["--verbose"])
    assert args.log_level == logging.INFO

    # should not be able to specify -d/--debug and -v/--verbose together
    with pytest.raises(SystemExit):
        args = parser.parse_args(["--debug", "--verbose"])
