from typing import List

import numpy as np
import pandas as pd


def fix_names_of_columns(
    data_frame: pd.DataFrame, new_columns: List[str]
) -> pd.DataFrame:
    data_frame.columns = new_columns
    return data_frame


def convert_date_to_time(df: pd.DataFrame) -> pd.DataFrame:
    df["time"] = pd.to_datetime(df["time"], errors="coerce")
    return df


def round_values_in_column(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    df[column_name] = df[column_name].round(6)
    return df


def concatenate_data_frames(processed_data_frames: list) -> pd.DataFrame:
    huge_dataframe = pd.concat(processed_data_frames, ignore_index=True)
    return huge_dataframe


def fill_symbol_name(
    df: pd.DataFrame,
    symbol_name: str,
):
    df["symbol"] = symbol_name
    return df


def safe_convert_to_int(series):
    series = series.replace([np.nan, np.inf, -np.inf], 0)
    return series.astype(int)
