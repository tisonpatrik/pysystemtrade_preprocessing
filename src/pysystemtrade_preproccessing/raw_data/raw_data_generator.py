import numpy as np
import pandas as pd
from models.raw_data import ConfigItem, DataFile, Directory


def create_raw_dataframe(directory_config: ConfigItem, directory: Directory):
    daily_dataframes = []
    columns = directory_config.columns
    for file in directory.raw_data:
        df = _get_raw_dataframe(file, columns)
        daily_dataframes.append(df)
    return pd.concat(daily_dataframes, ignore_index=True)


def _get_raw_dataframe(file: DataFile, columns: list[str]) -> pd.DataFrame:
    df = pd.read_csv(file.local_path, parse_dates=True)

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
