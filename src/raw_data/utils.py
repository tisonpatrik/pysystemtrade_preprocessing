from typing import List

import pandas as pd


def fix_names_of_columns(
    data_frame: pd.DataFrame, symbol_name: str, new_columns: List[str]
) -> pd.DataFrame:
    data_frame["symbol"] = symbol_name
    data_frame.columns = new_columns
    return data_frame


# def covert_date_to_unix_time(df: pd.DataFrame) -> pd.DataFrame:
#     df["unix_date_time"] = pd.to_datetime(df["unix_date_time"], errors="coerce")
#     df["unix_date_time"] = df["unix_date_time"].map(pd.Timestamp.timestamp).astype(int)
#     return df


def convert_date_to_date_time(df: pd.DataFrame) -> pd.DataFrame:
    df["date_time"] = pd.to_datetime(df["date_time"], errors="coerce")
    return df


def aggregate_to_day_prices(df: pd.DataFrame, date_time_column: str) -> pd.DataFrame:
    df.set_index(date_time_column, inplace=True)
    resampled = df.resample("1B").last()
    resampled.reset_index(inplace=True)
    df_cleaned = resampled.dropna(subset=["price"])
    return df_cleaned


def round_values_in_column(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    df[column_name] = df[column_name].round(6)
    return df


def concatenate_data_frames(processed_data_frames: list) -> pd.DataFrame:
    huge_dataframe = pd.concat(processed_data_frames, ignore_index=True)
    return huge_dataframe
