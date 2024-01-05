"""Input file format definitions."""

import io
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
        pre_processing (Callable): The function to call before `pd.read_csv()`.
        post_processing (Callable): The function to call after `pd.read_csv()`.
        sep (str): The separator.
    """

    header: int
    names: List[str]
    usecols: List[int]
    ignores: List[str]
    pre_processing: Callable = lambda input, _: input
    post_processing: Callable = lambda df: df
    seperator: str = ","

    def get_usecols_names(self):
        return [self.names[i] for i in self.usecols[:3]]


# define pre-processing functions below


def bmo_cc_adobe_pre_processing(_input: Optional[str], year: str) -> io.StringIO:
    """Create CSV from input with each element on a new line.

    Args:
        _input (Optional[str]): The file to process, if `None` then read from stdin.
        year (str): The year of all transactions.

    Returns:
        A[n] `io.StringIO` CSV.
    """
    # get lines from stdin or file
    if _input is None:
        lines = []
        for line in sys.stdin:
            lines.append(line.strip())
    else:
        with open(_input) as f:
            lines = f.read().splitlines()

    rows = []
    i = 0
    while i < len(lines):
        elements = lines[i : i + 4]

        # add year to dates
        elements[0] += f" {year}"
        elements[1] += f" {year}"

        # add negative sign to amounts that are not credited (CR on next line)
        if i + 4 < len(lines) and lines[i + 4] == "CR":
            i += 5
        else:
            # check if amount is a float (header will not be float)
            is_float = True
            try:
                float(elements[-1])
            except ValueError:
                is_float = False

            if is_float:
                elements[-1] = "-" + elements[-1]

            i += 4

        row = ",".join(elements) + "\n"
        rows.append(row)

    new_input = "".join(rows)
    return io.StringIO(new_input)


# define post-processing functions below


def bmo_acct_web_post_processing(df: pd.DataFrame) -> pd.DataFrame:
    """Creates the "Amount" column.

    Args:
        df (pd.DataFrame): The dataframe to process.

    Returns:
        A[n] `pd.DataFrame` that combines "Amount" and "Money in" to create "Amount".
    """
    df["Amount"] = df["Amount"].replace("[$,]", "", regex=True).astype(float)
    df["Money in"] = df["Money in"].replace("[$,]", "", regex=True).astype(float)
    df["Amount"] = np.where(df["Money in"].isna(), df["Amount"], df["Money in"])
    df = df.drop("Money in", axis=1)
    return df


def bmo_cc_web_post_processing(df: pd.DataFrame) -> pd.DataFrame:
    """Formats the "Money in/out" column.

    Args:
        df (pd.DataFrame): The dataframe to process.

    Returns:
        A[n] `pd.DataFrame` that converts "Money in/out" to a float.
    """
    df["Money in/out"] = (
        df["Money in/out"].replace("[$,]", "", regex=True).astype(float)
    )
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

BMO_ACCT_WEB = InputFormat(
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
    post_processing=bmo_acct_web_post_processing,
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

BMO_CC_WEB = InputFormat(
    header=0,
    names=[
        "Transaction date",
        "Description",
        "Money in/out",
    ],
    usecols=[0, 1, 2],
    ignores=[r"^TRSF FROM.*285"],
    post_processing=bmo_cc_web_post_processing,
    seperator="\t",
)

BMO_CC_ADOBE = InputFormat(
    header=0,
    names=[
        "Transaction Date",
        "Posting Date",
        "Description",
        "Amount",
    ],
    usecols=[0, 2, 3],
    ignores=[r"^TRSF FROM.*285"],
    pre_processing=bmo_cc_adobe_pre_processing,
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


def parse_input(
    input: Optional[str], format: InputFormat, year: Optional[str]
) -> pd.DataFrame:
    """Parses an input.

    Args:
        input (Optional[str]): The path to the input file, if None parse from stdin.
        format (InputFormat): The input format.
        year (Optional[str]): The year of all transactions.

    Raises:
        ValueError: If input contains duplicate transactions.

    Returns:
        A[n] `pd.DataFrame` where the columns match the xlbudget file's column names.
    """
    input_initially_none = input is None
    if input_initially_none:
        print("Paste your transactions here (CTRL+D twice on a blank line to end):")

    input = format.pre_processing(input, year)

    df = pd.read_csv(
        input if input is not None else sys.stdin,
        sep=format.seperator,
        index_col=False,
        names=format.names,
        header=format.header if input is not None else None,
        usecols=format.usecols,
        parse_dates=[0],
        skip_blank_lines=False,
    )

    if input_initially_none:
        print("---End of transactions---")

    df = format.post_processing(df)

    # convert first column to datetime and replace any invalid values with NaT
    df[df.columns[0]] = pd.to_datetime(df[df.columns[0]], errors="coerce")

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
