## Arquivo com funções para formatação Json
import json
import statistics
from datetime import datetime, timedelta

# Função que valida se a formatação está correta
def validateJSON(jsonData):
    try:
        json.loads(jsonData) 
    except ValueError as err:
        return False
    return True

# Função que coloca os resultados da aplicação no formato dicionário para depois transformar em .json
def json_transform(workflow_name, workflow_state, temp_start, temp_close, diff_temp, perc_sucess, perc_branch_main, perc_branch_outros, runs_time_list, n_jobs_list, n_runs, n_runs_analyzed):
    meean_time = str(timedelta(seconds= int(statistics.mean(runs_time_list)))) # Calcula a média do tempo de execução
    dev_time = str(timedelta(seconds= int(statistics.stdev(runs_time_list)))) # Calcula o tempo entre data de criação e atualização
    mean_jobs = str(statistics.mean(n_jobs_list)) # Calcula média do número de jobs
    perc_sucess = "{0} %".format(round(perc_sucess, 2)) # Calcula porcentagem de sucesso
    perc_branch_main = "{0} %".format(round(perc_branch_main, 2)) # Calcula porcentagem de execuções relacionadas a branch main
    perc_branch_outros = "{0} %".format(round(perc_branch_outros, 2)) # Calcula porcentagem de execuções relacionadas a outras branch
    workflow_json = {
            "Workflow_Name":workflow_name, "State":workflow_state, "Created_at": temp_start, "Updated_at" :temp_close,
            "Dev_time":diff_temp, "Success_rate":perc_sucess, "Branch_Main_rate":perc_branch_main, "Other_Branchs_rate":perc_branch_outros,
            "Mean(Execution time)":meean_time, "Std_deviation(Execution time)": dev_time, "Jobs_mean":mean_jobs, "Total_runs": n_runs , "Runs_Analyzed": n_runs_analyzed
        }    
    return(workflow_json)

