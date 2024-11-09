from pathlib import Path

import pandas as pd
from models.configs import ConfigItem
from models.raw_data import RawDataFile


def create_instrumentconfig_dataframe(valid_directories: dict[str, ConfigItem], directory: str, file_list: list[RawDataFile], root: Path):
    tradable_instruments_path = root / "tradable_instruments.csv"
    tradable_instruments = pd.read_csv(tradable_instruments_path, parse_dates=True)
    expected_name = valid_directories[directory].name
    matching_file = next(f for f in file_list if f.local_path.stem == expected_name)
    columns = valid_directories[directory].columns
    df = pd.read_csv(matching_file.local_path, parse_dates=True)
    df.columns = columns
    df["tradable"] = df["symbol"].isin(tradable_instruments["symbol"])
    return df


def _get_raw_dataframe(file: RawDataFile, columns: list[str]) -> pd.DataFrame:
    df = pd.read_csv(file.local_path, parse_dates=True)

    # Rename the headers based on the config
    df.columns = columns

    symbol = file.local_path.stem
    df["symbol"] = symbol
    return df
