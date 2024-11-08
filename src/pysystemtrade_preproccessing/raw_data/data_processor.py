import logging
from collections import defaultdict
from pathlib import Path

from models.raw_data import RawDataFile
from raw_data.daily_data_generator import create_daily_dataframe
from raw_data.instrumentconfig_generator import create_instrumentconfig_dataframe
from raw_data.raw_data_generator import create_raw_dataframe
from utils.utils import load_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_files(root: Path, files: list[RawDataFile]):
    # Load the configuration
    config = load_config(root)
    valid_directories = {item.directory: item for item in config.items}

    # Group files using the private helper method, converting keys to a set
    grouped_files = _group_files_by_directory(files, set(valid_directories.keys()))

    for directory, file_list in grouped_files.items():
        if valid_directories[directory].daily_data:
            create_daily_dataframe(valid_directories, directory, file_list, root)
        if valid_directories[directory].raw_data:
            create_raw_dataframe(valid_directories, directory, file_list, root)
        if not valid_directories[directory].daily_data and not valid_directories[directory].raw_data:
            create_instrumentconfig_dataframe(valid_directories, directory, file_list, root)


def _group_files_by_directory(files: list[RawDataFile], valid_directories: set[str]) -> dict:
    grouped_files = defaultdict(list)
    for file in files:
        if file.directory in valid_directories:
            grouped_files[file.directory].append(file)
    return grouped_files
