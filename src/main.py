from pathlib import Path

from tradable_insturments.tradable_instruments_generator import (
    generate_tradable_instruments_csv,
)


def main():
    data_directory = Path(__file__).parent / "data"
    data_directory.mkdir(exist_ok=True)

    print("Generování tradable instruments CSV...")
    generate_tradable_instruments_csv()


if __name__ == "__main__":
    main()
