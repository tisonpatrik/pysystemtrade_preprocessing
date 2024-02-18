from dir_structure.dir_structure_generator import DirStructureGenerator
from tradable_insturments.tradable_instruments_generator import (
    generate_tradable_instruments_csv,
)


def main():
    dir_structure_generator = DirStructureGenerator()
    print("Generation of directory structure")
    dir_structure_generator.generate_dir_structure()
    print("Generation of tradable_instruments.csv")
    generate_tradable_instruments_csv(dir_structure_generator.get_csvconfig_path())


if __name__ == "__main__":
    main()
