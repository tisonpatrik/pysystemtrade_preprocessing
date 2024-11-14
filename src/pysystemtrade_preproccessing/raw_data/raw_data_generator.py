import numpy as np
import pandas as pd
from models.raw_data import DataFile, Directory


def create_roll_calendars_prices(directory: Directory):
    daily_dataframes = []
    columns = ["time", "current_contract", "next_contract", "carry_contract"]
    for file in directory.raw_data:
        df = _get_roll_calendar(file, columns)
        daily_dataframes.append(df)
    return pd.concat(daily_dataframes, ignore_index=True)


def _get_roll_calendar(file: DataFile, columns: list[str]) -> pd.DataFrame:
    df = pd.read_csv(file.local_path, parse_dates=True)
    if "FALSE" in df.columns:
        df = df.drop(columns=["FALSE"])
    if len(df.columns) != len(columns):
        raise ValueError(
            f"Mismatch in column count for file '{file.local_path}': " f"Expected {len(columns)} columns, found {df.head()} columns."
        )
    # Rename the headers based on the config
    df.columns = columns

    # Check if each column exists before converting
    if "carry_contract" in df.columns:
        df["carry_contract"] = _safe_convert_to_int(df["carry_contract"])
    if "next_contract" in df.columns:
        df["next_contract"] = _safe_convert_to_int(df["next_contract"])
    if "current_contract" in df.columns:
        df["current_contract"] = _safe_convert_to_int(df["current_contract"])

    symbol = file.local_path.stem
    if "BITCOIN" in symbol:
        symbol = "BITCOIN"
    elif "ETHEREUM" in symbol:
        symbol = "ETHEREUM"
    elif "EDOLLAR" in symbol:
        symbol = "EDOLLAR"
    elif "VIX" in symbol:
        symbol = "VIX"

    df["symbol"] = symbol
    return df


def create_fx_prices(directory: Directory):
    daily_dataframes = []
    columns = ["time", "price"]
    for file in directory.raw_data:
        df = _get_raw_dataframe(file, columns)
        daily_dataframes.append(df)
    return pd.concat(daily_dataframes, ignore_index=True)


def create_muliple_prices(directory: Directory):
    daily_dataframes = []
    columns = ["time", "carry", "carry_contract", "price", "price_contract", "forward", "forward_contract"]
    for file in directory.raw_data:
        df = _get_raw_dataframe(file, columns)
        daily_dataframes.append(df)
    return pd.concat(daily_dataframes, ignore_index=True)


def _get_raw_dataframe(file: DataFile, columns: list[str]) -> pd.DataFrame:
    df = pd.read_csv(file.local_path, parse_dates=True)

    if len(df.columns) != len(columns):
        raise ValueError(
            f"Mismatch in column count for file '{file.local_path}': " f"Expected {len(columns)} columns, found {len(df.columns)} columns."
        )
    # Rename the headers based on the config
    df.columns = columns

    # Check if each column exists before converting
    if "carry_contract" in df.columns:
        df["carry_contract"] = _safe_convert_to_int(df["carry_contract"])
    if "price_contract" in df.columns:
        df["price_contract"] = _safe_convert_to_int(df["price_contract"])
    if "forward_contract" in df.columns:
        df["forward_contract"] = _safe_convert_to_int(df["forward_contract"])

    symbol = file.local_path.stem
    df["symbol"] = symbol
    return df


def _safe_convert_to_int(series):
    series = series.replace([np.nan, np.inf, -np.inf], 0)
    return series.astype(int)
