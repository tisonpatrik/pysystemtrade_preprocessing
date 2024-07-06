from typing import List
import pandas as pd
import numpy as np

def fix_names_of_columns(
    data_frame: pd.DataFrame, new_columns: List[str]
) -> pd.DataFrame:
    data_frame.columns = new_columns
    return data_frame


def convert_date_to_date_time(df: pd.DataFrame) -> pd.DataFrame:
    df["date_time"] = pd.to_datetime(df["date_time"], errors="coerce")
    return df


def aggregate_to_day_prices(df: pd.DataFrame, date_time_column: str) -> pd.DataFrame:
    df.set_index(date_time_column, inplace=True)
    resampled = df.resample("1B").last()
    resampled.reset_index(inplace=True)
    return resampled


def round_values_in_column(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    df[column_name] = df[column_name].round(6)
    return df


def concatenate_data_frames(processed_data_frames: list) -> pd.DataFrame:
    huge_dataframe = pd.concat(processed_data_frames, ignore_index=True)
    return huge_dataframe

def fill_symbol_name(df: pd.DataFrame, symbol_name: str,):
    df["symbol"] = symbol_name
    return df

def safe_convert_to_int(series):
    series = series.replace([np.nan, np.inf, -np.inf], 0)
    return series.astype(int)