"""xlbudget file reading and writing."""

import calendar
from logging import getLogger
from typing import Dict

import pandas as pd
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.utils.cell import column_index_from_string, coordinate_from_string
from openpyxl.worksheet.table import Table, TableStyleInfo

logger = getLogger(__name__)

FORMAT_ACCOUNTING = '_($* #,##0.00_);_($* (#,##0.00);_($* "-"??_);_(@_)'
FORMAT_DATE = "MM/DD/YYYY"

MONTH_NAME_0_IND = calendar.month_name[1:]

COL_NAMES = ["Date", "Description", "Amount"]
COL_FORMATS = [FORMAT_DATE, None, FORMAT_ACCOUNTING]
COL_WIDTHS = [12, 20, 12]


class TablePosition:
    """The state and bounds of a worksheet table."""

    def __init__(self, ref: str) -> None:
        start, end = ref.split(":")

        self.__first_col, self.__header_row = coordinate_from_string(start)
        self.next_row = self.__header_row + 1
        self.__first_col_ind = column_index_from_string(self.__first_col)

        self.__last_col, self.__initial_last_row = coordinate_from_string(end)

    @property
    def first_col(self) -> int:
        return self.__first_col_ind

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(next_row={self.next_row}, "
            f"first_col={self.first_col})"
        )

    def get_ref(self) -> str:
        last_row = (
            self.__initial_last_row
            if self.__initial_last_row == self.next_row
            else self.next_row - 1
        )
        return f"{self.__first_col}{self.__header_row}:{self.__last_col}{last_row}"


def create_year_sheet(wb: Workbook, year: str):
    """Creates a year sheet, with a table for each month.

    Args:
        wb (openpyxl.workbook.workbook.Workbook): The workbook to create the sheet in.
        year (str): The year.
    """
    ws = wb.create_sheet(year)
    num_tables = len(MONTH_NAME_0_IND)

    for c_start in range(1, (len(COL_NAMES) + 1) * num_tables + 1, len(COL_NAMES) + 1):
        month_ind = c_start // (len(COL_NAMES) + 1)
        month = MONTH_NAME_0_IND[month_ind]
        logger.debug(f"creating {month} table")

        # table title
        ws.cell(row=1, column=c_start).value = month
        ws.merge_cells(
            start_row=1,
            start_column=c_start,
            end_row=1,
            end_column=c_start + len(COL_NAMES) - 2,
        )

        # table sum
        sum = ws.cell(row=1, column=c_start + len(COL_NAMES) - 1)
        sum.value = f"=SUM({month}[{COL_NAMES[-1]}])"
        sum.number_format = FORMAT_ACCOUNTING
        logger.debug(f"created sum cell {sum.coordinate}='{sum.value}'")

        # table header and formating
        for i in range(len(COL_NAMES)):
            c = c_start + i

            # header
            ws.cell(row=2, column=c).value = COL_NAMES[i]

            # column format
            cell = ws.cell(row=3, column=c)
            if COL_FORMATS[i]:
                cell.number_format = COL_FORMATS[i]

            # column width
            ws.column_dimensions[get_column_letter(c)].width = COL_WIDTHS[i]

        # create table
        c_start_ltr = get_column_letter(c_start)
        c_end_ltr = get_column_letter(c_start + len(COL_NAMES) - 1)
        ref = f"{c_start_ltr}2:{c_end_ltr}3"
        logger.debug(f"table {ref=}")
        tab = Table(displayName=month, ref=ref)

        # add a default style with striped rows and banded columns
        style = TableStyleInfo(
            name="TableStyleMedium9",
            showFirstColumn=False,
            showLastColumn=False,
            showRowStripes=True,
            showColumnStripes=True,
        )
        tab.tableStyleInfo = style

        ws.add_table(tab)


def update_xlbudget(wb: Workbook, df: pd.DataFrame):
    """Updates an xlbudget file.

    Args:
        wb (openpyxl.workbook.workbook.Workbook): The xlbudget workbook.
        df (pd.DataFrame): The input file dataframe.
    """
    # sort transactions to make the oldest transactions come first
    df = df.sort_values(by=COL_NAMES[0], ascending=True)

    oldest_date = df.iloc[0].Date
    newest_date = df.iloc[-1].Date
    logger.debug(f"{oldest_date=}, {newest_date=}")

    # initialize table positions dictionary
    # maps worksheet names to dictionaries that map table names to their position.
    table_pos: Dict[str, Dict[str, TablePosition]] = {}
    for year in range(oldest_date.year, newest_date.year + 1):
        year_name = str(year)
        table_pos[year_name] = {}

        start_month = oldest_date.month if year == oldest_date.year else 1
        end_month = newest_date.month if year == newest_date.year else 12

        for month in range(start_month, end_month + 1):
            month_name = calendar.month_name[month]
            logger.debug(f"Initializing table {month_name} in sheet {year_name}")
            ref = wb[year_name].tables[month_name].ref
            table_pos[year_name][month_name] = TablePosition(ref)

    # write input file to wb
    for row in df.itertuples(index=False):
        logger.debug(f"Writing transaction {row} to workbook")

        # get worksheet and table position
        year = str(row.Date.year)
        month = calendar.month_name[row.Date.month]
        ws, pos = wb[year], table_pos[year][month]

        # set date cell
        date_cell = ws.cell(row=pos.next_row, column=pos.first_col)
        date_cell.value = row.Date
        date_cell.number_format = FORMAT_DATE

        # set description cell
        ws.cell(row=pos.next_row, column=pos.first_col + 1).value = row.Description

        # set amount cell
        amount_cell = ws.cell(row=pos.next_row, column=pos.first_col + 2)
        amount_cell.value = row.Amount
        amount_cell.number_format = FORMAT_ACCOUNTING

        pos.next_row += 1

    # update table refs
    for year_name in table_pos.keys():
        for month_name, pos in table_pos[year_name].items():
            tab = wb[year_name].tables[month_name]
            ref = pos.get_ref()
            if ref != tab.ref:
                logger.debug(
                    f"Updating ref of table {tab.name} from {tab.ref} to {ref}"
                )
                tab.ref = pos.get_ref()
