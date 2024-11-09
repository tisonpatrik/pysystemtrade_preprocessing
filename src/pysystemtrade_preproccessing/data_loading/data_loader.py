import logging
from pathlib import Path

import requests
from configs import BASE_URL, RAW_URL, REQUEST_TIMEOUT
from models.git_reposnse import GitHubContent
from models.raw_data import RawDataFile
from pydantic import parse_obj_as
from utils.utils import check_and_confirm_directory, load_existing_content

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_or_raw_data(local_dir: Path) -> list[RawDataFile]:
    target_path = local_dir / "data"
    if not check_and_confirm_directory(target_path):
        logger.info("User chose not to overwrite. Loading existing content.")
        return load_existing_content(target_path)

    return download_repository_content(BASE_URL, local_dir)


def download_repository_content(api_url: str, path: Path) -> list[RawDataFile]:
    response = requests.get(api_url, timeout=REQUEST_TIMEOUT)
    content = parse_obj_as(list[GitHubContent], response.json())
    files = []

    for item in content:
        if item.type == "file":
            file = _download_file(item, item.path)
            files.append(file)
        elif item.type == "dir":
            dir_to_create = path / item.path
            download_repository_content(item.url, dir_to_create)
    return files


def _download_file(item: GitHubContent, target_path: Path) -> RawDataFile:
    # Ensure the directory within the root exists
    target_path.parent.mkdir(parents=True, exist_ok=True)

    # Construct the raw content URL for direct download
    raw_file_url = f"{RAW_URL}/{item.path}"
    logger.info("Downloading file from raw URL: %s", raw_file_url)
    file_response = requests.get(raw_file_url, timeout=REQUEST_TIMEOUT)
    with target_path.open("wb") as file:
        file.write(file_response.content)

    return RawDataFile(name=item.name, local_path=target_path, directory=target_path.parent.name)
