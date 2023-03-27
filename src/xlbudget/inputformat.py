"""Input file format definitions."""

from argparse import Action
from typing import Dict, List, NamedTuple

import pandas as pd

from xlbudget.rwxlb import COL_NAMES


class InputFormat(NamedTuple):
    """Specifies the format of the input file.

    Attributes:
        header (int): The 0-indexed row of the header in the input file.
        names (List[str]): The column names.
        usecols (List[int]): The indices of columns that map to `COL_NAMES`
    """

    header: int
    names: List[str]
    usecols: List[int]

    def get_usecols_names(self):
        return [self.names[i] for i in self.usecols]


BMO_CC = InputFormat(
    header=2,
    names=[
        "Item #",
        "Card #",
        "Transaction Date",
        "Posting Date",
        "Transaction Amount",
        "Description",
    ],
    usecols=[3, 5, 4],
)


class GetInputFormats(Action):
    """Argparse action for the format argument.
    Adapted from [this Stack Overflow answer](https://stackoverflow.com/a/50799463).

    Attributes:
        input_formats (Dict[str, InputFormat]): Maps format names to values.
    """

    input_formats: Dict[str, InputFormat] = {"BMO_CC": BMO_CC}

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, self.input_formats[values])


def parse_input(path: str, format: InputFormat) -> pd.DataFrame:
    """Parses an input file.

    Args:
        path (str): The path to the input file.
        format (InputFormat): The input file format.

    Returns:
        A[n] `pd.DataFrame` where the columns match the xlbudget file's `COL_NAMES`.
    """
    df = pd.read_csv(
        path,
        header=format.header,
        usecols=format.usecols,
        parse_dates=[0],
        skip_blank_lines=False,
    )

    # order to match `COL_NAMES`
    df = df[format.get_usecols_names()]

    # rename to match `COL_NAMES`
    df = df.set_axis(COL_NAMES, axis="columns")

    return df
