import glob
import os
from typing import List

import pandas as pd


def generate_csv_file(df: pd.DataFrame, path_with_name: str):
    """
    Generates a CSV file from a pandas DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to write to CSV.
    path_with_name (str): The complete path including the file name where the CSV will be saved.
    """
    # Writing the DataFrame to a CSV file at the specified path
    df.to_csv(path_with_name, index=False)


def load_multiple_csv_files(
    directory: str, list_of_symbols: List[str], ignore_symbols: bool = False
):
    """
    Loads multiple CSV files from a given directory and returns a list of DataFrames.
    Optionally ignores symbol filtering based on the 'ignore_symbols' flag.
    """
    data_frames_dict = {}
    for filepath in glob.glob(os.path.join(directory, "*.csv")):
        symbol_name = os.path.splitext(os.path.basename(filepath))[0]

        # Load CSV if ignore_symbols is True or symbol is in list_of_symbols
        if ignore_symbols or symbol_name in list_of_symbols:
            df = pd.read_csv(filepath)
            data_frames_dict[symbol_name] = df

    return data_frames_dict
