import glob
import os

from csv_utils.csv_generator import load_multiple_csv_files
from raw_data.utils import (
    concatenate_data_frames,
)

source_name = "fx_prices_csv"
target_name = "fx_prices.csv"
new_columns = ["time", "price"]


def generate_fx_prices_sctructure(source_path: str, target_path: str):
    print("Generation of fx_prices structure")
    source_path = os.path.join(source_path, source_name)
    csv_files = glob.glob(os.path.join(source_path, "*.csv"))
    list_of_symbols = [
        os.path.splitext(os.path.basename(file))[0] for file in csv_files
    ]

    dataframes = load_multiple_csv_files(
        directory=source_path, list_of_symbols=list_of_symbols, ignore_symbols=False
    )
    processed_data_frames = []
    for _,data_frame in dataframes.items():
        processed_data_frames.append(data_frame)

    result = concatenate_data_frames(processed_data_frames)
    print(result)
