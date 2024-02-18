import os

from src.csv_utils.csv_generator import generate_csv_file, load_multiple_csv_files
from src.raw_data.utils import (
    aggregate_to_day_based_prices,
    concatenate_data_frames,
    convert_date_to_date_time,
    covert_date_to_unix_time,
    fix_names_of_columns,
    round_values_in_column,
)
from src.tradable_insturments.tradable_instruments_generator import (
    get_tradable_instruments,
)

source_name = "adjusted_prices_csv"
target_name = "adjusted_prices.csv"
new_columns = ["unix_date_time", "price", "symbol"]


def generate_adjusted_prices_sctructure(source_path: str, target_path: str):
    print("Generation of adjusted_prices structure")
    source_path = os.path.join(source_path, source_name)
    list_of_symbols = get_tradable_instruments()
    dataframes = load_multiple_csv_files(
        directory=source_path, list_of_symbols=list_of_symbols, ignore_symbols=False
    )
    processed_data_frames = []
    for symbol_name, data_frame in dataframes.items():
        renamed = fix_names_of_columns(data_frame, symbol_name, new_columns)
        date_timed = convert_date_to_date_time(renamed)
        resampled = aggregate_to_day_based_prices(date_timed, "unix_date_time")
        rounded = round_values_in_column(resampled, "price")
        unixed = covert_date_to_unix_time(rounded)
        processed_data_frames.append(unixed)

    result = concatenate_data_frames(processed_data_frames)
    target_path = os.path.join(target_path, target_name)

    generate_csv_file(result, target_path)
