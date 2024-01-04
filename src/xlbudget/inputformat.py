"""Input file format definitions."""

import sys
from argparse import Action
from logging import getLogger
from typing import Callable, Dict, List, NamedTuple, Optional

import numpy as np
import pandas as pd

from xlbudget.rwxlb import COLUMNS, df_drop_ignores, df_drop_na

logger = getLogger(__name__)


class InputFormat(NamedTuple):
    """Specifies the format of the input file.

    Attributes:
        header (int): The 0-indexed row of the header in the input file.
        names (List[str]): The column names.
        usecols (List[int]): The first len(`COLUMNS`) elements are indices of columns
            that map to `COLUMNS`, there may indices after for columns required for
            post-processing.
        ignores (List[str]): Ignore transactions that contain with these regex patterns.
        post_processing (Callable): The function to call after processing.
        sep (str): The separator.
    """

    header: int
    names: List[str]
    usecols: List[int]
    ignores: List[str]
    post_processing: Callable = lambda df: df
    seperator: str = ","

    def get_usecols_names(self):
        return [self.names[i] for i in self.usecols[:3]]


# define post processing functions below


def bmo_acct_tsv_post_processing(df: pd.DataFrame) -> pd.DataFrame:
    """Creates the "Amount" column.

    Args:
        df (pd.DataFrame): The dataframe with "Amount" and "Money in" columns.

    Returns:
        A[n] `pd.DataFrame` that combines "Amount" and "Money in" to create "Amount".
    """
    df["Amount"] = df["Amount"].replace("[$,]", "", regex=True).astype(float)
    df["Money in"] = df["Money in"].replace("[$,]", "", regex=True).astype(float)
    df["Amount"] = np.where(df["Money in"].isna(), df["Amount"], df["Money in"])
    df = df.drop("Money in", axis=1)
    return df


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

BMO_ACCT_TSV = InputFormat(
    header=0,
    names=[
        "Date",
        "Description",
        "Amount",  # actually named "Money out", but matches after post-processing
        "Money in",
        "Balance",
    ],
    usecols=[0, 1, 2, 3],
    ignores=[r"^TF.*(?:285|593|625)$"],
    post_processing=bmo_acct_tsv_post_processing,
    seperator="\t",
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


def parse_input(input: Optional[str], format: InputFormat) -> pd.DataFrame:
    """Parses an input.

    Args:
        input (Optional[str]): The path to the input file, if None parse from stdin.
        format (InputFormat): The input format.

    Raises:
        ValueError: If input contains duplicate transactions.

    Returns:
        A[n] `pd.DataFrame` where the columns match the xlbudget file's column names.
    """
    if input is None:
        print("Paste your transactions here (CTRL+D twice to end):")

    df = pd.read_csv(
        input if input is not None else sys.stdin,
        sep=format.seperator,
        index_col=False,
        names=format.names,
        header=format.header if input is not None else 0,
        usecols=format.usecols,
        parse_dates=[0],
        skip_blank_lines=False,
    )

    df = format.post_processing(df)

    df = df_drop_na(df)

    df.columns = df.columns.str.strip()

    # order columns to match `COLUMNS`
    df = df[format.get_usecols_names()]

    # rename columns to match `COLUMNS`
    df = df.set_axis([c.name for c in COLUMNS], axis="columns")

    # sort rows by date
    df = df.sort_values(by=list(df.columns), ascending=True)

    # strip whitespace from descriptions
    df["Description"] = df["Description"].str.strip()

    # drop ignored transactions
    df = df_drop_ignores(df, "|".join(format.ignores))

    # TODO: write issues to make ignoring identical transactions interactive
    # TODO: investigate autocompletions
    if df.duplicated().any():
        logger.warning(
            "The following transactions are identical:\n"
            f"{df[df.duplicated(keep=False)]}"
        )

    return df
