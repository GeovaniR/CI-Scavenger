## Arquivo com funções para formatação Json
import json

# Função que valida se a formatação está correta
def validateJSON(json_data):
    json_test = str(json_data) # Salva texto dicionario em string para função de testagem
    json_test = json_test.replace("'", '"') # Corrige aspas incorretas
    try: # Faz o teste de tranformar de string para json
        json.loads(json_test) 
    except ValueError as err: # Se der erro retorna false
        return False
    return True

def build_json_file(name_json, json_data):
    name_json = name_json + ".json" # Entrada do nome do arquivo de saída
    is_valid = validateJSON(json_data) # Valida Texto que será transformado em Json
    if (is_valid): # Testa se o arquivo está corretamente formatado em .json
        with open(name_json, 'w', encoding='utf-8') as outfile: # Cria arquivo .json
            json.dump(json_data, outfile, ensure_ascii=False, indent=2)
    else: # Caso o teste de incorreto retorna uma mensagem de aviso
        return(print("Arquivo json não está formatado corretamente")) 

# Função que coloca os resultados da aplicação no formato dicionário para depois transformar em .json
def json_transform(workflow_name, workflow_state, temp_start, temp_close, diff_temp, store_infos_dict, runs_time_dict):
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
    workflow_json = {
            "Workflow_Name":workflow_name, "State":workflow_state, "Created_at": temp_start, "Updated_at" :temp_close,
            "Dev_time":diff_temp, "Success_rate":perc_sucess, "Branch_Main_rate":perc_branch_main, "Other_Branchs_rate":perc_branch_outros,
            "Mean(Execution time)":runs_mean_time, "Std_deviation(Execution time)": runs_sd_time, "Jobs_mean":mean_jobs, "Jobs_deviation": sd_jobs, "Total_runs": n_runs, 
            "Runs_Analyzed": n_runs_analyzed, "Mean Time Between runs":runs_mean_time_between_executions, "Std_deviation Time Between runs": runs_sd_time_between_executions
        }
    workflow_json = {**workflow_json, **runs_time_dict} # Junta com o dicionário que aprenseta a data de frequência da execução da runs
    return(workflow_json)

