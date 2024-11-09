from data_loading.data_loader import load_or_raw_data
from raw_data.data_processor import process_files
from utils.utils import get_project_root


def main():
    root = get_project_root()
    files = load_or_raw_data(local_dir=root)
    process_files(root, files)


if __name__ == "__main__":
    main()
