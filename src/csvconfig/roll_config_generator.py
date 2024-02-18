import os

import pandas as pd

from src.csv_utils.csv_generator import generate_csv_file
from src.tradable_insturments.tradable_instruments_generator import (
    get_tradable_instruments,
)

source_name = "rollconfig.csv"
target_name = "roll_config.csv"

new_columns = [
    "symbol",
    "hold_roll_cycle",
    "roll_offset_days",
    "carry_offset",
    "priced_roll_cycle",
    "expiry_offset",
]


def generate_instrument_config_csv(source_path: str, target_path: str):
    source_path = os.path.join(source_path, source_name)
    df = pd.read_csv(source_path)
    df.columns = new_columns
    symbols = get_tradable_instruments()
    filtered_df = df[df["symbol"].isin(symbols)]
    target_path = os.path.join(target_path, target_name)
    generate_csv_file(filtered_df, target_path)
