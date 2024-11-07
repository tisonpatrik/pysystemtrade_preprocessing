import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
from configs import REQUEST_TIMEOUT
from models.git_reposnse import GitHubContent
from models.raw_data import LoadedDirectory, RawDataFile
from pydantic import parse_obj_as
from utils.utils import check_and_confirm_directory, create_dir, load_existing_content

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
HTTP_OK = 200
MAX_WORKERS = 8


def load_or_raw_data(base_url: str, local_dir: Path) -> LoadedDirectory:
    """Recursively downloads files from the GitHub repository into the specified local directory using parallel processing."""

    if not check_and_confirm_directory(local_dir):
        logger.info("User chose not to overwrite. Loading existing content.")
        return load_existing_content(local_dir)

    response = requests.get(base_url, timeout=REQUEST_TIMEOUT)
    content_list = parse_obj_as(list[GitHubContent], response.json())
    downloaded_content = LoadedDirectory(files=[])

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_item = {executor.submit(_process_item, item, local_dir): item for item in content_list}

        for future in as_completed(future_to_item):
            item = future_to_item[future]
            try:
                result = future.result()
                if result is not None:
                    downloaded_content.files.append(result)
            except Exception:
                logger.exception("Error processing %s", item.name)

    return downloaded_content


def _process_item(item, local_dir) -> RawDataFile | None:
    """Processes an item by downloading the file, if applicable, and returning a DownloadedFile model."""
    item_path = local_dir / item.path
    if item.type == "file" and item.download_url:
        return _download_file(item, item_path)
    if item.type == "dir":
        create_dir(item_path)
        logger.info("Created directory: %s", item_path)
    else:
        logger.warning("No download URL for file: %s", item.name)
    return None


def _download_file(item, item_path) -> RawDataFile | None:
    """
    Downloads a single file and saves it to the specified path if not already loaded,
    returning a RawDataFile model.
    """
    file_response = requests.get(item.download_url, timeout=REQUEST_TIMEOUT)
    if file_response.status_code == HTTP_OK:
        item_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure parent directory exists
        with item_path.open("wb") as file:
            file.write(file_response.content)
        logger.info("Downloaded file: %s", item_path)
        return RawDataFile(name=item.name, local_path=item_path)
    logger.error("Failed to download %s from %s, Status: %s", item.name, item.download_url, file_response.status_code)
    return None
