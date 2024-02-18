import os

import pandas as pd

from src.csv_utils.csv_generator import generate_csv_file, load_multiple_csv_files
from src.tradable_insturments.tradable_instruments_generator import (
    get_tradable_instruments,
)

source_name = "adjusted_prices_csv"
new_columns = ["unix_date_time", "symbol", "price"]


def generate_adjusted_prices_sctructure(source_path: str, target_path: str):
    print("Generation of adjusted_prices structure")
    source_path = os.path.join(source_path, source_name)
    list_of_symbols = get_tradable_instruments()
    dataframes = load_multiple_csv_files(
        directory=source_path, list_of_symbols=list_of_symbols, ignore_symbols=False
    )
    print(dataframes)
