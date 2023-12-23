import os
from contextlib import nullcontext as does_not_raise
from typing import List, NamedTuple

import pytest

import xlbudget.inputformat as inputformat
from xlbudget.rwxlb import COLUMNS


class InputFormatSpecs(NamedTuple):
    name: str
    value: inputformat.InputFormat
    test_files: List[str]


def _get_test_files(input_format_name: str) -> List[str]:
    input_files_dir = os.path.join("tests", "inputs")
    input_files = os.listdir(input_files_dir)
    test_files = []
    for fn in input_files:
        file_path = os.path.join(input_files_dir, fn)
        if os.path.isfile(file_path) and fn.startswith(input_format_name.lower()):
            test_files.append(file_path)
    return test_files


INPUT_FORMATS = [
    InputFormatSpecs(
        name=n, value=getattr(inputformat, n), test_files=_get_test_files(n)
    )
    for n in {"BMO_ACCT", "BMO_CC"}
]
XLB_COL_NAMES = [c.name for c in COLUMNS]


@pytest.mark.parametrize("input_format_spec", INPUT_FORMATS)
def test_getinputformat_input_formats(input_format_spec: InputFormatSpecs) -> None:
    input_formats = inputformat.GetInputFormats.input_formats
    name, value, _ = input_format_spec
    assert name in input_formats, f"{name} not in input_formats"
    assert value == input_formats[name], "value mismatch"


@pytest.mark.parametrize("input_format_spec", INPUT_FORMATS)
def test_inputformatspecs_test_files(input_format_spec: InputFormatSpecs) -> None:
    name, _, test_files = input_format_spec
    assert len(test_files) >= 1, f"{name} has no test files"


@pytest.mark.parametrize("input_format", [i.value for i in INPUT_FORMATS])
def test_inputformat_get_usecols_names(input_format: inputformat.InputFormat) -> None:
    usecols_names = input_format.get_usecols_names()
    for i, name_ind in enumerate(input_format.usecols):
        assert (
            usecols_names[i] == input_format.names[name_ind]
        ), f"{i}th usecol name doesn't match {name_ind}th names ind"


@pytest.mark.parametrize(
    "test_file,input_format",
    [(t, i.value) for i in INPUT_FORMATS for t in i.test_files],
)
def test_parse_input(test_file: str, input_format: inputformat.InputFormat) -> None:
    with does_not_raise():
        df = inputformat.parse_input(test_file, input_format)
    assert not df.isna().all(axis=1).any(), f"df from {test_file} has NaN rows"
    assert not df.duplicated().any(), f"df from {test_file} contains duplicates"
    assert (
        list(df.columns) == XLB_COL_NAMES
    ), f"df from {test_file} doesn't have the right column names"
    for ignore in input_format.ignores:
        assert (
            not df["Description"].str.startswith(ignore).any()
        ), f"df from {test_file} contains descriptions that start with {ignore}"
