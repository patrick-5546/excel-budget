"""Input file format definitions."""

from argparse import Action
from typing import List, NamedTuple


class InputFormat(NamedTuple):
    """Specifies the format of the input file.

    Args:
        header (int): The 0-indexed row of the header in the input file.
        names (List[str]): The column names.
        usecols (List[int]): The indices of columns that map to `COL_NAMES`
    """

    header: int
    names: List[str]
    usecols: List[int]


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
    input_formats = {"BMO_CC": BMO_CC}

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, self.input_formats[values])
