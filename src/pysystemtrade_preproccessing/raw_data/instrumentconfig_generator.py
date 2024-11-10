from pathlib import Path

import pandas as pd
from models.raw_data import ConfigItem, DataFile, Directory


def create_instrumentconfig_dataframe(
    directory_config: ConfigItem, directory: Directory, root: Path, adjusted_prices_dir: Directory
) -> pd.DataFrame:
    tradable_instruments_path = root / "tradable_instruments.csv"
    tradable_instruments = pd.read_csv(tradable_instruments_path, parse_dates=True)
    expected_name = directory_config.name

    # Attempt to find the matching file or return None if not found
    matching_file = next(f for f in directory.raw_data if f.local_path.stem == expected_name)
    # Proceed with the DataFrame processing
    columns = directory_config.columns
    df = pd.read_csv(matching_file.local_path, parse_dates=True)
    df.columns = columns
    df["is_tradable"] = df["symbol"].isin(tradable_instruments["symbol"])

    # Extract file stems from adjusted_prices_dir.raw_data into list_instruments
    list_instruments = [file.local_path.stem for file in adjusted_prices_dir.raw_data]

    # Create a 'have_data' column in df based on the presence of symbols in list_instruments
    df["have_data"] = df["symbol"].isin(list_instruments)
    return df


def _get_raw_dataframe(file: DataFile, columns: list[str]) -> pd.DataFrame:
    df = pd.read_csv(file.local_path, parse_dates=True)

    # Rename the headers based on the config
    df.columns = columns

    symbol = file.local_path.stem
    df["symbol"] = symbol
    return df
