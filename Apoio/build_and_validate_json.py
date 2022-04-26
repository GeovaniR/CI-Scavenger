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
    workflow_json = {
            "Workflow_Name":workflow_name, "State":workflow_state, "Created_at": temp_start, "Updated_at" :temp_close,
            "Dev_time":diff_temp, "Success_rate":store_infos_dict["perc_sucess"], "Branch_Main_rate":store_infos_dict["perc_branch_main"], "Other_Branchs_rate":store_infos_dict["perc_branch_outros"],
            "Mean(Execution time)":store_infos_dict["runs_mean_time"], "Std_deviation(Execution time)": store_infos_dict["runs_sd_time"], "Jobs_mean":store_infos_dict["mean_jobs"], "Jobs_deviation": store_infos_dict["sd_jobs"], "Total_runs": store_infos_dict["n_runs"], 
            "Runs_Analyzed": store_infos_dict["n_runs_analyses"], "Mean Time Between runs":store_infos_dict["runs_mean_time_between_executions"], 
            "Std_deviation Time Between runs": store_infos_dict["runs_sd_time_between_executions"]
        }
    workflow_json = {**workflow_json, **runs_time_dict} # Junta com o dicionário que aprenseta a data de frequência da execução da runs
    return(workflow_json)

