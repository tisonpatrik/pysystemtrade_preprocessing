from pathlib import Path

from models.raw_data import LoadedDirectory, RawDataFile


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
        user_input = input(f"The directory {directory} is not empty. Do you want to overwrite its contents? (y/n): ")
        if user_input.lower() != "y":
            return False  # Cancel operation
    return True  # Proceed with operation


def load_existing_content(directory: Path) -> LoadedDirectory:
    """Loads existing files in the directory into DownloadedContent without downloading."""
    downloaded_content = LoadedDirectory(files=[])

    for file_path in directory.rglob("*"):  # Recursively go through all files
        if file_path.is_file():
            downloaded_content.files.append(RawDataFile(name=file_path.name, local_path=file_path))

    return downloaded_content
