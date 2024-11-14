import logging
from pathlib import Path

import pandas as pd
from models.raw_data import Directory
from raw_data.configs_generator import create_instrumentconfigs, create_rollconfig, create_spreadcosts
from raw_data.daily_data_generator import (
    create_daily_adjusted_prices,
    create_daily_multiple_prices,
)
from raw_data.raw_data_generator import create_fx_prices, create_muliple_prices, create_roll_calendars_prices
from utils.utils import create_dir, split_large_dataframe

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_files(root: Path, directories: list[Directory]):
    # Load the configuration
    adjusted_prices_directory = next(directory_item for directory_item in directories if directory_item.name == "adjusted_prices_csv")
    _create_tradeable_instruments_df(root, adjusted_prices_directory)
    for directory in directories:
        if directory.name == "multiple_prices_csv":
            daily_denom_prices = create_daily_multiple_prices(directory)
            _save_dataframe(daily_denom_prices, root, "daily_multiple_prices")

            multiple_prices = create_muliple_prices(directory)
            _save_dataframe(multiple_prices, root, "multiple_prices")
        if directory.name == "adjusted_prices_csv":
            daily_adjusted_prices = create_daily_adjusted_prices(directory)
            _save_dataframe(daily_adjusted_prices, root, "daily_adjusted_prices")

        if directory.name == "fx_prices_csv":
            fx_prices = create_fx_prices(directory)
            _save_dataframe(fx_prices, root, "fx_prices_csv")

        if directory.name == "roll_calendars_csv":
            roll_calendars = create_roll_calendars_prices(directory)
            _save_dataframe(roll_calendars, root, "roll_calendars_csv")

        if directory.name == "csvconfig":
            _process_config_files(root, directory)


def _process_config_files(root: Path, directory: Directory):
    for item in directory.raw_data:
        data = None
        if item.name == "instrumentconfig":
            data = create_instrumentconfigs(item.local_path)
        elif item.name == "rollconfig":
            data = create_rollconfig(item.local_path)
        elif item.name == "spreadcosts":
            data = create_spreadcosts(item.local_path)
        elif item.name == "moreinstrumentinfo":
            pass
        _save_dataframe(data, root, item.name)


def _create_tradeable_instruments_df(root: Path, adjusted_prices_dir: Directory):
    list_instruments = [file.local_path.stem for file in adjusted_prices_dir.raw_data]
    df = pd.DataFrame(list_instruments)
    df.columns = ["symbol"]
    _save_dataframe(df, root, "tradable_instruments")


def _save_dataframe(df, root: Path, filename: str):
    # Define the base output directory and ensure it exists
    if df is None:
        return
    out_path = root / "data" / filename
    create_dir(out_path)

    # Split the DataFrame into smaller parts
    files = split_large_dataframe(df)

    # Save each split DataFrame with an incremented suffix in the filename
    for i, part_df in enumerate(files):
        # Construct the filename with incremented suffix
        part_out_file = out_path / f"{out_path.stem}_{i + 1}.csv"
        part_df.to_csv(part_out_file, index=False)
        logger.info("Saved split file: %s", part_out_file)
