from configs import BASE_URL
from downloader.downloader import load_or_raw_data
from utils.utils import get_project_root


def main():
    root = get_project_root()
    files = load_or_raw_data(base_url=BASE_URL, local_dir=root)


if __name__ == "__main__":
    main()
