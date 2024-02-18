from instrumentconfig_generator import generate_instrumentconfig_csv


def generate_csvconfig_sctructure(dir_path: str, source_path: str):
    print("Generation of csvconfig structure")
    generate_instrumentconfig_csv(dir_path, source_path)
