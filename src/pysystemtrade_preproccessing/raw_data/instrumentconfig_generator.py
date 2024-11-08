from pathlib import Path

import pandas as pd
from models.configs import ConfigItem
from models.raw_data import RawDataFile


def create_instrumentconfig_dataframe(valid_directories: dict[str, ConfigItem], directory: str, file_list: list[RawDataFile], root: Path):
    tradable_instruments_path = root / "tradable_instruments.csv"
    tradable_instruments = pd.read_csv(tradable_instruments_path, parse_dates=True)
    file = file_list[0]
    columns = valid_directories[directory].columns
    df = pd.read_csv(file.local_path, parse_dates=True)
    df.columns = columns
    df["tradable"] = df["symbol"].isin(tradable_instruments["symbol"])
    out_file = root / "data" / f"{valid_directories[directory].name}.csv"
    df.to_csv(out_file)


def _get_raw_dataframe(file: RawDataFile, columns: list[str]) -> pd.DataFrame:
    df = pd.read_csv(file.local_path, parse_dates=True)

    # Rename the headers based on the config
    df.columns = columns

    symbol = file.local_path.stem
    df["symbol"] = symbol
    return df
