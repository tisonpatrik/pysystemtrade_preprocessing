import logging
from pathlib import Path

import requests
from configs import BASE_URL, REQUEST_TIMEOUT
from models.git_reposnse import GitHubContent
from models.raw_data import RawDataFile
from pydantic import parse_obj_as
from utils.utils import check_and_confirm_directory, create_dir, load_existing_content

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_or_raw_data(local_dir: Path) -> list[RawDataFile]:
    target_path = local_dir / "data"
    if not check_and_confirm_directory(target_path):
        logger.info("User chose not to overwrite. Loading existing content.")
        return load_existing_content(target_path)

    return download_repository_content(local_dir, BASE_URL)


def download_repository_content(target_path: Path, url: str) -> list[RawDataFile]:
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    content = parse_obj_as(list[GitHubContent], response.json())
    files = []
    for item in content:
        if item.type == "file":
            file = _download_file(item, item.path)
            files.append(file)
        elif item.type == "dir":
            dir_to_create = item.path
            create_dir(dir_to_create)
            logger.info("Created directory: %s", dir_to_create)
            download_repository_content(target_path / item.path, item.url)
    return files


def _download_file(item: GitHubContent, target_path: Path) -> RawDataFile:
    file_response = requests.get(item.url, timeout=REQUEST_TIMEOUT)
    with target_path.open("wb") as file:
        file.write(file_response.content)
    logger.info("Downloaded file: %s", target_path)
    return RawDataFile(name=item.name, local_path=target_path, directory=target_path.parent.name)
