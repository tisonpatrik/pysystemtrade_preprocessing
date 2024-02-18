import os

import pandas as pd

from src.csv_generator import generate_csv_file
from src.tradable_insturments.tradable_instruments_generator import (
    get_tradable_instruments,
)

file_name = "instrumentconfig.csv"

new_columns = [
    "symbol",
    "description",
    "pointsize",
    "currency",
    "asset_class",
    "per_block",
    "percentage",
    "per_trade",
    "region",
]


def generate_instrumentconfig_csv(source_path: str, target_path: str):
    source_path = os.path.join(source_path, file_name)
    df = pd.read_csv(source_path)
    df.columns = new_columns
    symbols = get_tradable_instruments()
    filtered_df = df[df["symbol"].isin(symbols)]
    target_path = os.path.join(target_path, file_name)
    generate_csv_file(filtered_df, target_path)
