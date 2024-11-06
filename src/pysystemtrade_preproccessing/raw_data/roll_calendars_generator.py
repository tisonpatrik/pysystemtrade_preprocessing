import os

from csv_utils.csv_generator import load_multiple_csv_files
from raw_data.utils import (
    concatenate_data_frames,
)
from tradable_insturments.tradable_instruments_generator import (
    get_tradable_instruments,
)

source_name = "roll_calendars_csv"
target_name = "roll_calendars.csv"
new_columns = [
    "time",
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
    for _,data_frame in dataframes.items():
        processed_data_frames.append(data_frame)

    result = concatenate_data_frames(processed_data_frames)
    print(result)
