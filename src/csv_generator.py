import pandas as pd


def generate_csv_file(df: pd.DataFrame, path_with_name: str):
    """
    Generates a CSV file from a pandas DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to write to CSV.
    path_with_name (str): The complete path including the file name where the CSV will be saved.
    """
    # Writing the DataFrame to a CSV file at the specified path
    df.to_csv(path_with_name, index=False)
