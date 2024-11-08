from pathlib import Path

import pandas as pd
from models.configs import ConfigItem
from models.raw_data import RawDataFile


def create_daily_dataframe(valid_directories: dict[str, ConfigItem], directory: str, file_list: list[RawDataFile], root: Path):
    daily_dataframes = []
    columns = valid_directories[directory].columns
    for file in file_list:
        df = _get_daily_data(file, columns)
        daily_dataframes.append(df)
    combined_df = pd.concat(daily_dataframes, ignore_index=True)
    out_file = root / "data" / f"daily_{valid_directories[directory].name}.csv"
    combined_df.to_csv(out_file)


def _get_daily_data(file: RawDataFile, columns: list[str]) -> pd.DataFrame:
    df = pd.read_csv(file.local_path, index_col=0, parse_dates=True)

    # Resample data to business day frequency
    resampled = df.resample("1B").last()
    resampled = resampled.reset_index()

    # Rename the headers based on the config
    resampled.columns = columns

    symbol = file.local_path.stem
    resampled["symbol"] = symbol
    return resampled
