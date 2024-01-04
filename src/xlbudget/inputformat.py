"""Input file format definitions."""

from argparse import Action
from typing import Dict, List, NamedTuple

import pandas as pd

from xlbudget.rwxlb import COLUMNS, df_drop_ignores, df_drop_na


class InputFormat(NamedTuple):
    """Specifies the format of the input file.

    Attributes:
        header (int): The 0-indexed row of the header in the input file.
        names (List[str]): The column names.
        usecols (List[int]): The indices of columns that map to `COLUMNS`.
        ignores (List[str]): Ignore transactions that contain with these regex patterns.
    """

    header: int
    names: List[str]
    usecols: List[int]
    ignores: List[str]

    def get_usecols_names(self):
        return [self.names[i] for i in self.usecols]


# define input formats below

BMO_ACCT = InputFormat(
    header=3,
    names=[
        "First Bank Card",
        "Transaction Type",
        "Date Posted",
        "Transaction Amount",
        "Description",
    ],
    usecols=[2, 4, 3],
    ignores=[r"^\[CW\] TF.*(?:285|593|625)$"],
)

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
    usecols=[2, 5, 4],
    ignores=[r"^TRSF FROM.*285"],
)


# define input formats above


class GetInputFormats(Action):
    """Argparse action for the format argument.
    Adapted from [this Stack Overflow answer](https://stackoverflow.com/a/50799463).

    Attributes:
        input_formats (Dict[str, InputFormat]): Maps format names to values.
    """

    input_formats: Dict[str, InputFormat] = {
        n: globals()[n] for n in globals() if isinstance(globals()[n], InputFormat)
    }

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, self.input_formats[values])


def parse_input(path: str, format: InputFormat) -> pd.DataFrame:
    """Parses an input file.

    Args:
        path (str): The path to the input file.
        format (InputFormat): The input file format.

    Raises:
        ValueError: If input file contains duplicate transactions.

    Returns:
        A[n] `pd.DataFrame` where the columns match the xlbudget file's column names.
    """
    df = pd.read_csv(
        path,
        header=format.header,
        usecols=format.usecols,
        parse_dates=[0],
        skip_blank_lines=False,
    )

    df = df_drop_na(df)

    # TODO: write issues to make ignoring duplicate transactions interactive
    # they might not be an error
    # TODO: investigate autocompletions
    if df.duplicated().any():
        raise ValueError("Input file contains duplicate transactions")

    df.columns = df.columns.str.strip()

    # order columns to match `COLUMNS`
    df = df[format.get_usecols_names()]

    # rename columns to match `COLUMNS`
    df = df.set_axis([c.name for c in COLUMNS], axis="columns")

    # sort rows by date
    df = df.sort_values(by="Date")

    # strip whitespace from descriptions
    df["Description"] = df["Description"].str.strip()

    # drop ignored transactions
    df = df_drop_ignores(df, "|".join(format.ignores))

    return df
