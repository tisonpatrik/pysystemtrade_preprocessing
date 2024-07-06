import os

from src.csv_utils.csv_generator import generate_csv_file, load_multiple_csv_files
from src.raw_data.utils import (
    concatenate_data_frames,
    convert_date_to_date_time,
    fix_names_of_columns,
    fill_symbol_name
)
from src.tradable_insturments.tradable_instruments_generator import (
    get_tradable_instruments,
)

source_name = "roll_calendars_csv"
target_name = "roll_calendars.csv"
new_columns = [
    "date_time",
    "current_contract",
    "next_contract",
    "carry_contract",

]


def generate_roll_calendars_sctructure(source_path: str, target_path: str):
    print("Generation of roll_calendars structure")
    source_path = os.path.join(source_path, source_name)
    list_of_symbols = get_tradable_instruments()
    dataframes = load_multiple_csv_files(
        directory=source_path, list_of_symbols=list_of_symbols, ignore_symbols=False
    )
    processed_data_frames = []
    for symbol_name, data_frame in dataframes.items():
        if "Unnamed: 4" in data_frame.columns:  # Adjust the column name as needed
            data_frame = data_frame.drop(columns=["Unnamed: 4"])
        renamed = fix_names_of_columns(data_frame, new_columns)
        date_timed = convert_date_to_date_time(renamed)
        filled = fill_symbol_name(date_timed, symbol_name)
        processed_data_frames.append(filled)

    result = concatenate_data_frames(processed_data_frames)
    target_path = os.path.join(target_path, target_name)

    generate_csv_file(result, target_path)
