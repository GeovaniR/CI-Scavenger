from os import sep
import pandas as pd
import csv

def csv_transform(workflow_name, workflow_state, temp_start, temp_close, diff_temp, store_infos_dict, runs_time_dict):
    runs_mean_time = str(store_infos_dict["runs_mean_time"]) # Transforma em string a média do tempo de execução
    runs_sd_time = str(store_infos_dict["runs_sd_time"]) # Transforma em string o desvio padrão do tempo de execução
    runs_mean_time_between_executions = str(store_infos_dict["runs_mean_time_between_executions"]) # Transforma em string o tempo médio entre as execuções das runs
    runs_sd_time_between_executions = str(store_infos_dict["runs_sd_time_between_executions"]) # Transforma em string o desvio padrão do tempo entre as execuções das runs
    mean_jobs = str(store_infos_dict["mean_jobs"]) # Transforma em string a média do número de jobs das runs
    sd_jobs = str(store_infos_dict["sd_jobs"]) # Transforma em string o desvio padrão do número de jobs das runs
    perc_sucess = "{0} %".format(store_infos_dict["perc_sucess"]) # formata a saída para formato string como porcentagem
    perc_branch_main = "{0} %".format(store_infos_dict["perc_branch_main"]) # formata a saída para formato string como porcentagem
    perc_branch_outros = "{0} %".format(store_infos_dict["perc_branch_outros"]) # formata a saída para formato string como porcentagem
    n_runs = store_infos_dict["n_runs"]
    n_runs_analyzed = store_infos_dict["n_runs_analyses"]
    runs_freq = ""
    for chave, valor in runs_time_dict.items():
        aux = ("{0}: {1} / ".format(chave, valor))
        runs_freq = runs_freq + aux
    data = [workflow_name, workflow_state, temp_start, temp_close, diff_temp, runs_mean_time, runs_sd_time, runs_mean_time_between_executions, runs_sd_time_between_executions,
    mean_jobs, sd_jobs, perc_sucess, perc_branch_main, perc_branch_outros, n_runs, n_runs_analyzed, runs_freq]
    return(data)


def build_csv_file(name_csv, df_data):
    name_csv = name_csv + ".csv" # Entrada do nome do arquivo de saída
    df = pd.DataFrame(df_data, columns=['workflow_name', "workflow_state", "temp_start", "temp_close", "diff_temp", "runs_mean_time", "runs_sd_time", 
    "runs_mean_time_between_executions", "runs_sd_time_between_executions", "mean_jobs", "sd_jobs", "perc_sucess", "perc_branch_main", "perc_branch_outros", 
    "n_runs", "n_runs_analyzed", "runs_freq"])
    df.to_csv(name_csv, sep = ";")
    