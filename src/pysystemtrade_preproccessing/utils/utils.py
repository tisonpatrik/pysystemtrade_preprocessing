import json
from pathlib import Path

from models.configs import Config, ConfigItem
from models.raw_data import RawDataFile


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


def load_existing_content(directory: Path) -> list[RawDataFile]:
    """Loads existing files in the directory into DownloadedContent without downloading."""
    return [
        RawDataFile(name=file_path.name, local_path=file_path, directory=file_path.parent.name)
        for file_path in directory.rglob("*")
        if file_path.is_file()
    ]


def load_config(root: Path) -> Config:
    config_path = root / "config.json"

    if not config_path.is_file():
        raise FileNotFoundError(f"Config file not found at {config_path}")

    with config_path.open("r") as file:
        config_data = json.load(file)

    return Config(items=[ConfigItem(**item) for item in config_data])
