import os

import pandas as pd
from csv_utils.csv_generator import generate_csv_file
from tradable_insturments.tradable_instruments_generator import (
    get_tradable_instruments,
)

source_name = "moreinstrumentinfo.csv"
target_name = "instrument_metadata.csv"

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


def generate_instrument_metadata_csv(source_path: str, target_path: str):
    source_path = os.path.join(source_path, source_name)
    df = pd.read_csv(source_path)
    df.columns = new_columns
    symbols = get_tradable_instruments()
    filtered_df = df[df["symbol"].isin(symbols)]
    columns_to_drop = ["sub_sub_class", "style", "country", "duration"]
    droped_columns = filtered_df.drop(columns_to_drop, axis=1)
    fixed_missing_data = finish_data(droped_columns)
    target_path = os.path.join(target_path, target_name)
    generate_csv_file(fixed_missing_data, target_path)


def finish_data(droped_columns):
    def determine_sub_class(row):
        # Check if sub_class is already set or not
        if pd.isna(row["sub_class"]):
            if row["symbol"] == "V2X":
                return "EU-Vol"
            elif row["symbol"] in ["VIX", "VIX_mini"]:
                return "US-Vol"
            elif row["symbol"] == "VNKI":
                return "JPY-Vol"
            else:
                return None  # Or some default value, as appropriate
        else:
            # Return existing value if sub_class is not empty
            return row["sub_class"]

    # Apply the function across rows, updating 'sub_class' based on 'symbol'
    droped_columns["sub_class"] = droped_columns.apply(determine_sub_class, axis=1)
    return droped_columns
