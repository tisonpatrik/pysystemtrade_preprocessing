import logging
from collections import defaultdict
from pathlib import Path

from models.raw_data import RawDataFile
from raw_data.daily_data_generator import create_daily_dataframe
from raw_data.instrumentconfig_generator import create_instrumentconfig_dataframe
from raw_data.raw_data_generator import create_raw_dataframe
from utils.utils import create_dir, load_config, split_large_dataframe

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_files(root: Path, files: list[RawDataFile]):
    # Load the configuration
    config = load_config(root)
    valid_directories = {item.directory: item for item in config.items}
    # Group files using the private helper method, converting keys to a set
    grouped_files = _group_files_by_directory(files, set(valid_directories.keys()))

    for directory, file_list in grouped_files.items():
        directory_config = valid_directories[directory]

        if directory_config.daily_data:
            df = create_daily_dataframe(valid_directories, directory, file_list)
            _save_dataframe(df, root, directory_config.name)

        elif directory_config.raw_data:
            df = create_raw_dataframe(valid_directories, directory, file_list)
            _save_dataframe(df, root, directory_config.name)

        else:
            df = create_instrumentconfig_dataframe(valid_directories, directory, file_list, root)
            _save_dataframe(df, root, directory_config.name)


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


def _group_files_by_directory(files: list[RawDataFile], valid_directories: set[str]) -> dict:
    grouped_files = defaultdict(list)
    for file in files:
        if file.directory in valid_directories:
            grouped_files[file.directory].append(file)
    return grouped_files
