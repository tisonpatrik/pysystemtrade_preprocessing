import logging
from pathlib import Path

from models.raw_data import ConfigItem, Directory
from raw_data.daily_data_generator import create_daily_dataframe
from raw_data.instrumentconfig_generator import create_instrumentconfig_dataframe
from raw_data.raw_data_generator import create_raw_dataframe
from utils.utils import create_dir, load_config_items, split_large_dataframe

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_files(root: Path, directories: list[Directory]):
    # Load the configuration
    valid_sources = load_config_items(root)
    tuples = _match_directories_with_config(valid_sources, directories)
    adjusted_prices_directory = next(directory_item for directory_item in directories if directory_item.name == "adjusted_prices_csv")
    for directory_config, directory in tuples:
        if directory.name == "multiple_prices_csv":
            daily_denom_prices = create_daily_dataframe(directory_config, directory)
            _save_dataframe(daily_denom_prices, root, f"daily_{directory_config.name}")

            multiple_prices = create_raw_dataframe(directory_config, directory)
            _save_dataframe(multiple_prices, root, directory_config.name)
        if directory.name == "adjusted_prices_csv":
            daily_adjusted_prices = create_daily_dataframe(directory_config, directory)
            _save_dataframe(daily_adjusted_prices, root, f"daily_{directory_config.name}")

        if directory.name == "fx_prices_csv":
            fx_prices = create_raw_dataframe(directory_config, directory)
            _save_dataframe(fx_prices, root, directory_config.name)

        if directory.name == "csvconfig":
            instrument_config = create_instrumentconfig_dataframe(directory_config, directory, root, adjusted_prices_directory)
            _save_dataframe(instrument_config, root, directory_config.name)


def _save_dataframe(df, root: Path, filename: str):
    # Define the base output directory and ensure it exists
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


def _match_directories_with_config(valid_sources: list[ConfigItem], directories: list[Directory]) -> list[tuple[ConfigItem, Directory]]:
    matched_items = []
    for config_item in valid_sources:
        matching_directory = next((directory for directory in directories if directory.name == config_item.directory), None)
        if matching_directory:
            matched_items.append((config_item, matching_directory))

    return matched_items
