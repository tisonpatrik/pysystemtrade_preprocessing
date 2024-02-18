import os

from src.csvconfig.instrument_metadata_generator import generate_instrument_metadata_csv
from src.csvconfig.instrumentconfig_generator import generate_instrumentconfig_csv

source_sub_dir = "csvconfig"


def generate_csvconfig_sctructure(source_path: str, target_path: str):
    print("Generation of csvconfig structure")
    source_path = os.path.join(source_path, source_sub_dir)
    generate_instrumentconfig_csv(source_path, target_path)
    generate_instrument_metadata_csv(source_path, target_path)
