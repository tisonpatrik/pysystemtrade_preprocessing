import pandas as pd
from models.raw_data import DataFile, Directory


def create_daily_multiple_prices(directory: Directory):
    daily_dataframes = []
    columns = ["time", "carry", "carry_contract", "price", "price_contract", "forward", "forward_contract"]
    for file in directory.raw_data:
        df = _get_daily_data(file, columns)
        daily_dataframes.append(df)
    return pd.concat(daily_dataframes, ignore_index=True)


def create_daily_adjusted_prices(directory: Directory):
    daily_dataframes = []
    columns = ["time", "price"]
    for file in directory.raw_data:
        df = _get_daily_data(file, columns)
        daily_dataframes.append(df)
    return pd.concat(daily_dataframes, ignore_index=True)


def _get_daily_data(file: DataFile, columns: list[str]) -> pd.DataFrame:
    df = pd.read_csv(file.local_path, index_col=0, parse_dates=True)

    # Resample data to business day frequency
    resampled = df.resample("1B").last()
    resampled = resampled.reset_index()

    resampled.columns = columns

    # Keep only "time" and "price" columns
    resampled = resampled[["time", "price"]]

    symbol = file.local_path.stem
    resampled["symbol"] = symbol
    return resampled
