import pandas as pd
from models.configs import ConfigItem
from models.raw_data import RawDataFile


def create_raw_dataframe(valid_directories: dict[str, ConfigItem], directory: str, file_list: list[RawDataFile]):
    daily_dataframes = []
    columns = valid_directories[directory].columns
    for file in file_list:
        df = _get_raw_dataframe(file, columns)
        daily_dataframes.append(df)
    return pd.concat(daily_dataframes, ignore_index=True)


def _get_raw_dataframe(file: RawDataFile, columns: list[str]) -> pd.DataFrame:
    df = pd.read_csv(file.local_path, parse_dates=True)

    # Rename the headers based on the config
    df.columns = columns

    symbol = file.local_path.stem
    df["symbol"] = symbol
    return df
