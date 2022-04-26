from os import sep
import pandas as pd
import csv

def csv_transform(workflow_name, workflow_state, temp_start, temp_close, diff_temp, store_infos_dict, runs_time_dict):
    runs_freq = ""
    for chave, valor in runs_time_dict.items():
        aux = ("{0}: {1} / ".format(chave, valor))
        runs_freq = runs_freq + aux
    data = [workflow_name, workflow_state, temp_start, temp_close, diff_temp, store_infos_dict["runs_mean_time"], store_infos_dict["runs_sd_time"], 
    store_infos_dict["runs_mean_time_between_executions"], store_infos_dict["runs_sd_time_between_executions"], store_infos_dict["mean_jobs"], store_infos_dict["sd_jobs"], 
    store_infos_dict["perc_sucess"], store_infos_dict["perc_branch_main"], store_infos_dict["perc_branch_outros"], store_infos_dict["n_runs"], store_infos_dict["n_runs_analyses"], runs_freq]
    return(data)


def build_csv_file(name_csv, df_data):
    name_csv = name_csv + ".csv" # Entrada do nome do arquivo de saída
    df = pd.DataFrame(df_data, columns=['workflow_name', "workflow_state", "temp_start", "temp_close", "diff_temp", "runs_mean_time", "runs_sd_time", 
    "runs_mean_time_between_executions", "runs_sd_time_between_executions", "mean_jobs", "sd_jobs", "perc_sucess", "perc_branch_main", "perc_branch_outros", 
    "n_runs", "n_runs_analyzed", "runs_freq"])
    df.to_csv(name_csv, sep = ";")
    