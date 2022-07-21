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
def format_file(store_infos_dict, runs_time_dict):
    runs_freq = ""
    for chave, valor in runs_time_dict.items():
        aux = ("{0}: {1} / ".format(chave, valor))
        runs_freq = runs_freq + aux
    workflow_json = {
            "Workflow_Name":store_infos_dict["Workflow_Name"], "State":store_infos_dict["State"], "Created_at": store_infos_dict["Created_at"], 
            "Updated_at" :store_infos_dict["Updated_at"], "Dev_time":store_infos_dict["Dev_time"], "Success_rate":store_infos_dict["perc_sucess"], 
            "Main_Branch_rate":store_infos_dict["perc_branch_main"], "Other_Branchs_rate":store_infos_dict["perc_branch_outros"], 
            "Mean(Execution time)":store_infos_dict["runs_mean_time"], "Std_deviation(Execution time)": store_infos_dict["runs_sd_time"], 
            "Jobs_mean":store_infos_dict["mean_jobs"], "Jobs_deviation": store_infos_dict["sd_jobs"], "Total_runs": store_infos_dict["n_runs"], 
            "Runs_Analyzed": store_infos_dict["n_runs_analyses"], "Mean Time Between runs":store_infos_dict["runs_mean_time_between_executions"], 
            "Std_deviation Time Between runs": store_infos_dict["runs_sd_time_between_executions"], "runs_freq" : runs_freq, 
            "Pipeline_Structure": store_infos_dict["pipeline_structure"]
        }
    return(workflow_json)

