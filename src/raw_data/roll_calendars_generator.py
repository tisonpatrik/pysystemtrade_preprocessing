import os

import pandas as pd

from src.csv_utils.csv_generator import generate_csv_file, load_multiple_csv_files
from src.tradable_insturments.tradable_instruments_generator import (
    get_tradable_instruments,
)

source_name = "roll_calendars_csv"
target_name = "roll_calendars.csv"
new_columns = [
    "unix_date_time",
    "current_contract",
    "next_contract",
    "carry_contract",
    "symbol",
]


def generate_roll_calendars_sctructure(source_path: str, target_path: str):
    print("Generation of adjusted_prices structure")
    source_path = os.path.join(source_path, source_name)
    list_of_symbols = get_tradable_instruments()
    dataframes = load_multiple_csv_files(
        directory=source_path, list_of_symbols=list_of_symbols, ignore_symbols=False
    )
    processed_data_frames = []
    for symbol_name, data_frame in dataframes.items():
        renamed = fix_names_of_columns(data_frame, symbol_name)
        date_timed = convert_date_to_date_time(renamed)
        unixed = covert_date_to_unix_time(date_timed)
        processed_data_frames.append(unixed)

    result = concatenate_data_frames(processed_data_frames)
    target_path = os.path.join(target_path, target_name)

    generate_csv_file(result, target_path)


def fix_names_of_columns(data_frame: pd.DataFrame, symbol_name: str) -> pd.DataFrame:
    data_frame["symbol"] = symbol_name
    data_frame.columns = new_columns
    return data_frame


def covert_date_to_unix_time(df: pd.DataFrame) -> pd.DataFrame:
    df["unix_date_time"] = pd.to_datetime(df["unix_date_time"], errors="coerce")
    df["unix_date_time"] = df["unix_date_time"].map(pd.Timestamp.timestamp).astype(int)
    return df


def convert_date_to_date_time(df: pd.DataFrame) -> pd.DataFrame:
    df["unix_date_time"] = pd.to_datetime(df["unix_date_time"], errors="coerce")
    return df


def aggregate_to_day_based_prices(
    df: pd.DataFrame, date_time_column: str
) -> pd.DataFrame:
    df.set_index(date_time_column, inplace=True)
    resampled = df.resample("1B").last()
    resampled.reset_index(inplace=True)
    return resampled


def round_values_in_column(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    df[column_name] = df[column_name].astype(float)
    df[column_name] = df[column_name].round(3)
    return df


def concatenate_data_frames(processed_data_frames: list) -> pd.DataFrame:
    huge_dataframe = pd.concat(processed_data_frames, ignore_index=True)
    return huge_dataframe
