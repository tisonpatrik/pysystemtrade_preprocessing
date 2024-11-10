import json
from pathlib import Path

import numpy as np
import pandas as pd
from models.raw_data import ConfigItem, DataFile, Directory


def get_project_root() -> Path:
    """Gets the root directory of the project."""
    return Path(__file__).resolve().parent.parent.parent.parent


def create_dir(dir_path: Path) -> Path:
    """Creates the specified directory if it doesn't exist and returns its path."""
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def check_and_confirm_directory(directory: Path) -> bool:
    """Checks if the directory is empty. If not, asks for user confirmation to overwrite."""
    if directory.exists() and any(directory.iterdir()):  # Directory is not empty
        user_input = input(f"The directory {directory} is not empty. Do you want to overwrite its contents? (y/N): ")
        if user_input.lower() != "y":
            return False  # Cancel operation
    return True  # Proceed with operation


def load_existing_content(directory: Path) -> list[Directory]:
    """Loads existing CSV files and directories in the given directory into a structured list of Directory with associated DataFile."""
    directories: dict[str, Directory] = {}
    for file_path in directory.rglob("*"):
        if file_path.is_file() and file_path.suffix == ".csv":
            dir_name = file_path.parent.name
            if dir_name not in directories:
                directories[dir_name] = Directory(name=dir_name)

            data_file = DataFile(name=file_path.name, local_path=file_path)
            directories[dir_name].add_file(data_file)

        elif file_path.is_dir() and file_path.name not in directories:
            directories[file_path.name] = Directory(name=file_path.name)

    return list(directories.values())


def load_config_items(root: Path) -> list[ConfigItem]:
    config_path = root / "config.json"

    if not config_path.is_file():
        raise FileNotFoundError(f"Config file not found at {config_path}")

    with config_path.open("r") as file:
        config_data = json.load(file)

    return [ConfigItem(**item) for item in config_data]


def split_large_dataframe(df: pd.DataFrame, max_rows: int = 500000) -> list[pd.DataFrame]:
    """Splits a large DataFrame into a list of smaller DataFrames, each with a maximum of `max_rows` rows."""
    num_chunks = int(np.ceil(len(df) / max_rows))
    return [pd.DataFrame(chunk, columns=df.columns) for chunk in np.array_split(df, num_chunks)]
