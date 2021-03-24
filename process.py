# -*- coding: utf-8 -*-

"""Data processing for Plotly Dash webapp to process SWRCGSR Enrollment Reports."""

# Import required libraries
from typing import Tuple, Dict, Optional
import pandas as pd
from pathlib import Path
from datetime import date
import boto3
from botocore.exceptions import ClientError
import os
import pickle

# TERM DATA
CURRENT_TERM = "Summer2021"
PREVIOUS_TERM = "Summer2020"

# Load s3 environment variables
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_BUCKET_NAME = os.environ.get("AWS_BUCKET_NAME")


# Helper Functions
def upload_s3_file(file_name: str, bucket: str, object_name: Optional[str] = None):
    """Upload a file to an S3 bucket

    Args:
        filename (str): File to upload
        bucket (str): Bucket to upload to
        object_name (str): S3 object name. If not specified then file_name is used

    Returns:
        bool: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client("s3")
    try:
        _ = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError:
        return False
    return True


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

    max_test = parse_dict[date(2021, 2, 25)][["Course", "Max"]]
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


def process_max_old(parse_dict: Dict[date, pd.DataFrame]) -> pd.DataFrame:
    """Helper method to find max enrollment in previous term."""
    final_df = pd.DataFrame(columns=["Date", "Enrolled", "CRN", "Course"])
    for key, value in parse_dict.items():
        temp_df = value[["CRN", "Enrolled", "Course"]].copy()
        temp_df["Date"] = key
        final_df = pd.concat([final_df, temp_df])
    test = pd.DataFrame(final_df.groupby(["Course", "Date"])["Enrolled"].sum())

    max_test = list(parse_dict.values())[0][["Course", "Max"]]
    max_test2 = max_test.groupby("Course")["Max"].sum()

    test2 = test.reset_index().pivot(index="Course", columns="Date", values="Enrolled")
    test3 = test2.copy()

    for ix, value in test3.iteritems():
        for ind, each in value.items():
            beep = each / max_test2[ind]
            test3.loc[ind, ix] = float(beep)

    tester = test3[test3.columns[::-1]]
    return tester


def process_df_to_counts(parse_dict: Dict[date, pd.DataFrame]) -> pd.DataFrame:
    """Helper method to process and format a df into a count of enrollment"""
    final_df = pd.DataFrame(columns=["Date", "Enrolled", "CRN", "Course"])
    for key, value in parse_dict.items():
        temp_df = value[["CRN", "Enrolled", "Course"]].copy()
        temp_df["Date"] = key
        final_df = pd.concat([final_df, temp_df])
    test = pd.DataFrame(final_df.groupby(["Course", "Date"])["Enrolled"].sum())
    test2 = test.reset_index().pivot(index="Course", columns="Date", values="Enrolled")
    tester = test2[test2.columns[::-1]]
    return tester


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


def prepare_s3_pickle(filename: str = "data.pickle") -> None:
    parse_dict = parse_files(CURRENT_TERM)
    tester, tester3 = process_data(parse_dict)
    old_df = parse_old(PREVIOUS_TERM)
    old1 = parse_files(PREVIOUS_TERM)
    older = process_df_to_counts(old1)
    max_old = process_max_old(old1)
    test_vs_old = process_vs_old(parse_dict, old_df)

    data_dict = {
        "parse_dict": parse_dict,
        "tester": tester,
        "tester3": tester3,
        "old_df": old_df,
        "old1": old1,
        "older": older,
        "max_old": max_old,
        "test_vs_old": test_vs_old,
    }
    pickle.dump(data_dict, open(filename, "wb"))


if __name__ == "__main__":
    prepare_s3_pickle()
    upload_s3_file("data.pickle", AWS_BUCKET_NAME)
