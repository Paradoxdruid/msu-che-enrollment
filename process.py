# -*- coding: utf-8 -*-

"""Data processing for Plotly Dash webapp to process SWRCGSR Enrollment Reports."""

# Import required libraries
from typing import Tuple, Dict
import pandas as pd
from pathlib import Path
from datetime import date


# Helper Functions
def parse_files(term: str) -> Dict[date, pd.DataFrame]:
    """Reads in a list of processed SWRCGSR files in .xlsx format
    and returns them as a dictionary of pandas Dataframe values with date keys.

    Args:
        term (str): term to analyze, e.g. "Spring2021"

    Returns:
        Dict[datetime.date,pd.DataFrame]
    """

    home = Path.cwd()
    directory = home / "count"
    term_pattern = f"{term}_*.xlsx"
    files = list(directory.rglob(term_pattern))
    files_dict = {f.stem.split("_")[1]: f for f in files}
    parse_dict = {}
    for key, value in files_dict.items():
        parse_dict[date(int(key[0:4]), int(key[4:6]), int(key[6:8]))] = pd.read_excel(
            value, header=0, usecols=list(range(0, 25))
        )

    return parse_dict


def parse_old(term: str) -> pd.DataFrame:
    """Grabs the dataframe of last years enrollment.

    Args:
        term (str): term to analyze, e.g. "Spring2020"

    Returns:
        pd.DataFrame: dataframe of old enrollment.
    """
    home = Path.cwd()
    directory = home / "count"
    term_pattern = f"{term}_*.xlsx"
    files = list(directory.rglob(term_pattern))
    files_dict = {f.stem.split("_")[1]: f for f in files}
    parse_dict = {}
    for key, value in files_dict.items():
        parse_dict[date(int(key[0:4]), int(key[4:6]), int(key[6:8]))] = pd.read_excel(
            value, header=0, usecols=list(range(0, 25))
        )

    return list(parse_dict.values())[0]


def process_data(
    parse_dict: Dict[date, pd.DataFrame]
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Read the parse dict to create dataframes for plotting.

    Args:
        parse_dict (Dict[pd.DataFrame])

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: tuple of dataframes for plotting enrollment.
    """

    final_df = pd.DataFrame(columns=["Date", "Enrolled", "CRN", "Course"])
    for key, value in parse_dict.items():
        temp_df = value[["CRN", "Enrolled", "Course"]].copy()
        temp_df["Date"] = key
        final_df = pd.concat([final_df, temp_df])

    max_df = pd.DataFrame(columns=["Date", "Enrolled", "CRN", "Course", "Max"])
    for key, value in parse_dict.items():
        temp_df = value[["CRN", "Enrolled", "Course", "Max"]].copy()
        temp_df["Date"] = key
        max_df = pd.concat([max_df, temp_df])

    test = final_df.groupby(["Course", "Date"])["Enrolled"].sum()
    test = pd.DataFrame(test)

    max_test = parse_dict[date(2020, 11, 30)][["Course", "Max"]]
    max_test2 = max_test.groupby("Course")["Max"].sum()

    test2 = test.reset_index().pivot(index="Course", columns="Date", values="Enrolled")
    test3 = test2.copy()

    for ix, value in test3.iteritems():
        for ind, each in value.items():
            beep = each / max_test2[ind]
            test3.loc[ind, ix] = float(beep)

    tester = test2[test2.columns[::-1]]
    tester3 = test3[test3.columns[::-1]]

    return tester, tester3


def process_vs_old(
    parse_dict: Dict[date, pd.DataFrame], old_df: pd.DataFrame
) -> pd.DataFrame:
    """Read the parse_dict and create a comparison of current vs previous year enrollment.

    Args:
        parse_dict (Dict[pd.DataFrame])
        old_df (pd.DataFrame)

    Returns:
        pd.DataFrame
    """

    final_df = pd.DataFrame(columns=["Date", "Enrolled", "CRN", "Course"])
    for key, value in parse_dict.items():
        temp_df = value[["CRN", "Enrolled", "Course"]].copy()
        temp_df["Date"] = key
        final_df = pd.concat([final_df, temp_df])

    test = final_df.groupby(["Course", "Date"])["Enrolled"].sum()
    test = pd.DataFrame(test)

    test2 = test.reset_index().pivot(index="Course", columns="Date", values="Enrolled")
    test3 = test2.copy()

    max_test = old_df[["Course", "Enrolled"]]
    max_test2 = max_test.groupby("Course")["Enrolled"].sum()

    max_test2 = max_test2.rename(index={"CHE3260": "CHE4460", "CHE3290": "CHE4490"})

    for ix, value in test3.iteritems():
        for ind, each in value.items():
            try:
                if max_test2[ind] == 0:
                    beep = 0
                else:
                    beep = each / max_test2[ind]
            except KeyError:
                beep = 0
            test3.loc[ind, ix] = float(beep)

    test_vs_old = test3[test3.columns[::-1]]

    return test_vs_old
