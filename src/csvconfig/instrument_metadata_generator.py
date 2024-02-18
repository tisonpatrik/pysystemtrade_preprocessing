import os

import pandas as pd

from src.csv_generator import generate_csv_file
from src.tradable_insturments.tradable_instruments_generator import (
    get_tradable_instruments,
)

file_name = "instrument_metadata.csv"

new_columns = [
    "symbol",
    "asset_class",
    "sub_class",
    "sub_sub_class",
    "style",
    "country",
    "duration",
    "description",
]
source_name = "moreinstrumentinfo.csv"


def generate_instrument_metadata_csv(source_path: str, target_path: str):
    source_path = os.path.join(source_path, source_name)
    df = pd.read_csv(source_path)
    df.columns = new_columns
    symbols = get_tradable_instruments()
    filtered_df = df[df["symbol"].isin(symbols)]
    target_path = os.path.join(target_path, file_name)
    generate_csv_file(filtered_df, target_path)


def finish_data(df):
    def determine_sub_class(symbol):
        if symbol == "V2X":
            return "EU-Vol"
        elif symbol in ["VIX", "VIX_mini"]:
            return "US-Vol"
        elif symbol == "VNKI":
            return "JPY-Vol"
        else:
            return None  # Or some default value, as appropriate

    # Apply the function to the 'symbol' column to update the 'sub_class' column
    df["sub_class"] = df["symbol"].apply(determine_sub_class)
    return df
