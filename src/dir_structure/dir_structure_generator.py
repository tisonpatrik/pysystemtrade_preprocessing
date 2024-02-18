import os
from time import sleep


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
