## Arquivo com funções para formatação Json
import json
import statistics
from datetime import timedelta

# Função que valida se a formatação está correta
def validateJSON(json_data):
    json_test = str(json_data) # Salva texto dicionario em string para função de testagem
    json_test = json_test.replace("'", '"') # Corrige aspas incorretas
    try: # Faz o teste de tranformar de string para json
        json.loads(json_test) 
    except ValueError as err: # Se der erro retorna false
        return False
    return True

def build_json_file(is_valid, name_json, json_data):
    if (is_valid): # Testa se o arquivo está corretamente formatado em .json
        with open(name_json, 'w', encoding='utf-8') as outfile: # Cria arquivo .json
            json.dump(json_data, outfile, ensure_ascii=False, indent=2)
    else: # Caso o teste de incorreto retorna uma mensagem de aviso
        return(print("Arquivo json não está formatado corretamente")) 

# Função que coloca os resultados da aplicação no formato dicionário para depois transformar em .json
def json_transform(workflow_name, workflow_state, temp_start, temp_close, diff_temp, perc_sucess, perc_branch_main, perc_branch_outros, runs_time_list, n_jobs_list, n_runs, n_runs_analyzed, runs_time_dict, runs_diff_time):
    runs_mean_time = str(timedelta(seconds= int(statistics.mean(runs_time_list)))) # Calcula a média do tempo de execução
    runs_sd_time = str(timedelta(seconds= int(statistics.stdev(runs_time_list)))) # Calcula o desvio padrão do tempo de execução
    runs_mean_time_between_executions = str(timedelta(seconds= int(statistics.mean(runs_diff_time)))) # Calcula o tempo médio entre as execuções das runs
    runs_sd_time_between_executions = str(timedelta(seconds= int(statistics.stdev(runs_diff_time)))) # Calcula o desvio padrão do tempo entre as execuções das runs
    mean_jobs = str(round(statistics.mean(n_jobs_list), 2)) # Calcula a média do número de jobs das runs
    sd_jobs = str(round(statistics.stdev(n_jobs_list), 2)) # Calcula o desvio padrão do número de jobs das runs
    perc_sucess = "{0} %".format(round(perc_sucess, 2)) # formata a saída para formato string como porcentagem
    perc_branch_main = "{0} %".format(round(perc_branch_main, 2)) # formata a saída para formato string como porcentagem
    perc_branch_outros = "{0} %".format(round(perc_branch_outros, 2)) # formata a saída para formato string como porcentagem
    workflow_json = {
            "Workflow_Name":workflow_name, "State":workflow_state, "Created_at": temp_start, "Updated_at" :temp_close,
            "Dev_time":diff_temp, "Success_rate":perc_sucess, "Branch_Main_rate":perc_branch_main, "Other_Branchs_rate":perc_branch_outros,
            "Mean(Execution time)":runs_mean_time, "Std_deviation(Execution time)": runs_sd_time, "Jobs_mean":mean_jobs, "Jobs_deviation": sd_jobs, "Total_runs": n_runs, 
            "Runs_Analyzed": n_runs_analyzed, "Mean Time Between runs":runs_mean_time_between_executions, "Std_deviation Time Between runs": runs_sd_time_between_executions
        }
    workflow_json = {**workflow_json, **runs_time_dict} # Junta com o dicionário que aprenseta a data de frequência da execução da runs
    return(workflow_json)

