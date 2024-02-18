import os

import pandas as pd

from csv_generator import generate_csv_file

file_name = "instrumentconfig.csv"


def generate_instrumentconfig_csv(dir_path: str, source_path: str):
    source_path = os.path.join(source_path, file_name)
    df = pd.read_csv(source_path)
    target_path = os.path.join(dir_path, file_name)
    generate_csv_file(df, target_path)
