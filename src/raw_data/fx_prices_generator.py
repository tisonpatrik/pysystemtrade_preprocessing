import glob
import os

from src.csv_utils.csv_generator import generate_csv_file, load_multiple_csv_files
from src.raw_data.utils import (
    aggregate_to_day_prices,
    concatenate_data_frames,
    convert_date_to_date_time,
    fix_names_of_columns,
    round_values_in_column,
    fill_symbol_name
)

source_name = "fx_prices_csv"
target_name = "fx_prices.csv"
new_columns = ["date_time", "price"]


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
    for symbol_name, data_frame in dataframes.items():
        renamed = fix_names_of_columns(data_frame, new_columns)
        date_timed = convert_date_to_date_time(renamed)
        resampled = aggregate_to_day_prices(date_timed, "date_time")
        rounded = round_values_in_column(resampled, "price")
        filled = fill_symbol_name(date_timed, symbol_name)
        empty_value_checker(filled)

        processed_data_frames.append(filled)

    result = concatenate_data_frames(processed_data_frames)
    target_path = os.path.join(target_path, target_name)

    generate_csv_file(result, target_path)


def empty_value_checker(data_frame):
    contains_empty_or_nan = (
        data_frame["price"].isna().any() or (data_frame["price"] == "").any()
    )
    if contains_empty_or_nan:
        filtered_df = data_frame[
            (data_frame["price"].isna()) | (data_frame["price"] == "")
        ]
        print(data_frame.iloc[5020:5030])

        print(f"Data contains empty or NaN values for price: {filtered_df['price']}")
        print("Data contains empty or NaN values")
