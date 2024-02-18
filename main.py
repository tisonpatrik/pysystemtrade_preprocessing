import os

from src.csvconfig.csvconfig_generator import generate_csvconfig_sctructure
from src.raw_data.adjusted_prices_generator import generate_adjusted_prices_sctructure
from src.raw_data.fx_prices_generator import generate_fx_prices_sctructure
from src.tradable_insturments.tradable_instruments_generator import (
    generate_tradable_instruments_csv,
)


def main():
    print(get_source_path())
    dir_structure_generator = DirStructureGenerator()
    print("Generation of directory structure")
    dir_structure_generator.generate_dir_structure()

    generate_tradable_instruments_csv(dir_structure_generator.get_csvconfig_path())

    generate_csvconfig_sctructure(
        get_source_path(), dir_structure_generator.get_csvconfig_path()
    )
    generate_adjusted_prices_sctructure(
        get_source_path(), dir_structure_generator.get_adjusted_prices_csv_path()
    )
    generate_fx_prices_sctructure(
        get_source_path(), dir_structure_generator.get_fx_prices_path()
    )


def get_source_path():
    current_script_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_script_path)
    parent_dir_of_repositories = os.path.join(current_dir, "..")
    source_path = os.path.join(
        parent_dir_of_repositories, "pysystemtrade", "data", "futures"
    )
    return os.path.abspath(source_path)


class DirStructureGenerator:
    def __init__(self):
        pass

    def generate_dir_structure(self):

        os.makedirs(self.get_data_dir_path(), exist_ok=True)
        os.makedirs(self.get_adjusted_prices_csv_path(), exist_ok=True)
        os.makedirs(self.get_csvconfig_path(), exist_ok=True)
        os.makedirs(self.get_fx_prices_path(), exist_ok=True)
        os.makedirs(self.get_multiple_prices_path(), exist_ok=True)
        os.makedirs(self.get_roll_calendars_csv_path(), exist_ok=True)

    def get_data_dir_path(self):
        return "data"

    def get_adjusted_prices_csv_path(self):
        return "data/adjusted_prices"

    def get_csvconfig_path(self):
        return "data/config"

    def get_fx_prices_path(self):
        return "data/fx_prices"

    def get_multiple_prices_path(self):
        return "data/multiple_prices"

    def get_roll_calendars_csv_path(self):
        return "data/roll_calendars"


if __name__ == "__main__":
    main()
