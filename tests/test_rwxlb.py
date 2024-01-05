import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

import xlbudget.rwxlb as rwxlb


def test_columns() -> None:
    for i, c in enumerate(rwxlb.MONTH_COLUMNS):
        assert isinstance(
            c, rwxlb.ColumnSpecs
        ), f"column {i} type isn't `ColumnSpecs`: {c}"


def test_TablePosition() -> None:
    t = rwxlb.TablePosition("A2:C4")
    vars = [d for d in dir(t) if not d.startswith("_") and not callable(getattr(t, d))]

    # variables
    num_vars = 3  # hardcoded: update manually
    assert len(vars) == num_vars, "not all variables are tested"
    assert t.first_col == 1, "`first_col` value unexpected"
    assert t.next_row == 3, "`next_row` value unexpected"
    assert t.initial_last_row == 4, "`initial_last_row` value unexpected"

    # __repr__()
    t_repr = str(t)
    repr_prefix = "TablePosition("
    assert t_repr.startswith(repr_prefix), f"repr does not start with {repr_prefix}"
    for name in vars:
        repr = f"{name}={getattr(t, name)}"
        assert repr in t_repr, f"repr does not represent {name} properly"

    # get_ref()
    assert t.get_ref() == "A2:C3", "`get_ref()` value 1 unexpected"
    t.next_row += 1
    assert t.get_ref() == "A2:C3", "`get_ref()` value 2 unexpected"
    t.next_row += 1
    assert t.get_ref() == "A2:C4", "`get_ref()` value 3 unexpected"
    t.next_row += 1
    assert t.get_ref() == "A2:C5", "`get_ref()` value 4 unexpected"


@pytest.mark.parametrize(
    "input_df, expected_df",
    [
        (
            pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}),
            pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}),
        ),
        (
            pd.DataFrame({"A": [1, 2, 2], "B": [3, 4, 4]}),
            pd.DataFrame({"A": [1, 2], "B": [3, 4]}),
        ),
        (
            pd.DataFrame({"A": [1, 1, 1], "B": [2, 2, 2]}),
            pd.DataFrame({"A": [1], "B": [2]}),
        ),
    ],
)
def test_df_drop_duplicates(input_df: pd.DataFrame, expected_df: pd.DataFrame) -> None:
    actual_df = rwxlb.df_drop_duplicates(input_df)
    assert_frame_equal(actual_df, expected_df)


@pytest.mark.parametrize(
    "input_df, ignore, expected_df",
    [
        (
            pd.DataFrame({"Description": ["ignore this", "keep this", "ignore that"]}),
            "drop",
            pd.DataFrame({"Description": ["ignore this", "keep this", "ignore that"]}),
        ),
        (
            pd.DataFrame({"Description": ["ignore this", "keep this", "ignore that"]}),
            "ignore",
            pd.DataFrame({"Description": ["keep this"]}),
        ),
        (
            pd.DataFrame({"Description": ["drop this", "keep this", "drop that"]}),
            "drop",
            pd.DataFrame({"Description": ["keep this"]}),
        ),
    ],
)
def test_df_drop_ignores(
    input_df: pd.DataFrame, ignore: str, expected_df: pd.DataFrame
) -> None:
    actual_df = rwxlb.df_drop_ignores(input_df, ignore)
    assert_frame_equal(actual_df, expected_df)


@pytest.mark.parametrize(
    "input_df, expected_df",
    [
        (
            pd.DataFrame({"A": [1.0, None, 3.0], "B": [None, 2.0, 4.0]}),
            pd.DataFrame({"A": [1.0, None, 3.0], "B": [None, 2.0, 4.0]}),
        ),
        (
            pd.DataFrame({"A": [1.0, None, 3.0], "B": [None, None, None]}),
            pd.DataFrame({"A": [1.0, 3.0], "B": [None, None]}),
        ),
        (
            pd.DataFrame({"A": [None, None, None], "B": [None, None, None]}),
            pd.DataFrame(columns=["A", "B"]),
        ),
    ],
)
def test_df_drop_na(input_df, expected_df):
    actual_df = rwxlb.df_drop_na(input_df)
    assert_frame_equal(actual_df, expected_df)


@pytest.mark.parametrize(
    "month, year, expected",
    [
        ("January", "2022", "_January2022"),
        ("February", "2021", "_February2021"),
        ("March", "2020", "_March2020"),
    ],
)
def test_get_table_name(month, year, expected):
    assert rwxlb._get_month_table_name(month, year) == expected
