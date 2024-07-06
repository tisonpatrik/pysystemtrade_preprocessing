import os

from src.csv_utils.csv_generator import generate_csv_file, load_multiple_csv_files
from src.raw_data.utils import (
    aggregate_to_day_prices,
    concatenate_data_frames,
    convert_date_to_date_time,
    fix_names_of_columns,
    round_values_in_column,
    fill_symbol_name,
    safe_convert_to_int
)
from src.tradable_insturments.tradable_instruments_generator import (
    get_tradable_instruments,
)

source_name = "multiple_prices_csv"
target_name = "multiple_prices.csv"
new_columns = [
    "date_time",
    "carry",
    "carry_contract",
    "price",
    "price_contract",
    "forward",
    "forward_contract",
]


def generate_multiple_prices_sctructure(source_path: str, target_path: str):
    print("Generation of multiple_prices structure")
    source_path = os.path.join(source_path, source_name)
    list_of_symbols = get_tradable_instruments()
    dataframes = load_multiple_csv_files(
        directory=source_path, list_of_symbols=list_of_symbols, ignore_symbols=False
    )
    processed_data_frames = []
    for symbol_name, data_frame in dataframes.items():
        renamed = fix_names_of_columns(data_frame, new_columns)
        date_timed = convert_date_to_date_time(renamed)
        resampled = aggregate_to_day_prices(date_timed, "date_time")
        filled = fill_symbol_name(resampled, symbol_name)
        empty_value_checker(filled)
        filled = round_values_in_column(filled, "price")

        filled["carry_contract"] = safe_convert_to_int(filled["carry_contract"])
        filled["price_contract"] = safe_convert_to_int(filled["price_contract"])
        filled["forward_contract"] = safe_convert_to_int(filled["forward_contract"])

        processed_data_frames.append(filled)

    result = concatenate_data_frames(processed_data_frames)
    target_path = os.path.join(target_path, target_name)

    generate_csv_file(result, target_path)


def empty_value_checker(data_frame):
    column = "carry_contract"
    contains_empty_or_nan = (
        data_frame[column].isna().any() or (data_frame[column] == "").any()
    )
    if contains_empty_or_nan:
        filtered_df = data_frame[
            (data_frame[column].isna()) | (data_frame[column] == "")
        ]
        print(data_frame.iloc[6255:6270])

        print(f"Data contains empty or NaN values for price: {filtered_df['carry']}")
        print("Data contains empty or NaN values")
