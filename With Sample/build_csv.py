from os import sep
import pandas as pd


def build_csv_file(name_csv, json_data, repo_path):
    name_csv = name_csv + ".csv" # Entrada do nome do arquivo de saída
    df = pd.DataFrame.from_dict(json_data[repo_path])
    df.to_csv(name_csv, sep = ";")
    