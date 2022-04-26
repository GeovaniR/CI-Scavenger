### Algoritmo para recuperar informações dos Pipelines dos repos

## Importando bibliotecas
import get_workflow_infos as work
import calculate_stats as calc
import build_and_validate_json as js
import print_infos as prt
import verify_pipeline as pipeline
from log_requests import requests_dict_count, create_log
import build_csv as csv

def main():
    username = input("Username:") # Entrada Username git hub
    token = input("Token:") # Entrada do token de validação
    owner = input("Repository Owner:") # Entrada do nome do Dono do repo
    repo = input("Repository Name:") # Entrada do nome do repo
    n = int(input("Número de runs para ánalise:")) # Entrada do número de runs que vamos analisar
    verbose = int(input("Retornar texto além do Json?:")) # Entrada binária
    name = str(input("Nome do arquivo de saída:")) # Entrada do nome do arquivo de saída
    output = str(input("Formato de saída(csv ou json):"))
    repo_path, full_repo_path, request_path, workflows, n_pipelines = work.define_workflow_path(username, token, owner, repo, verbose)
    json_data = {repo_path:[{"n_worfklows" : n_pipelines}]}
    df_data = []
    for i in range(0, n_pipelines): ## Loop para que seja rodada as funções em cada pipeline
        validate_worflow = pipeline.investigate_workflow_ci_cd(i, n, workflows, request_path, username, token, full_repo_path) # Valida se o workflow tem destino a CI/CD para permitir análise
        if (validate_worflow): # Se o worklow da indícios de CI/CD, então roda funçõs para obter estatísticas
            store_infos_dict, runs_time_dict = calc.calculate_workflows_stats(i, n, workflows, username, token, request_path, full_repo_path, verbose)
            if (store_infos_dict): # Vai verificar se o dicionário está vazio, se não estiver é porque temos runs de sucesso então roda demais funções
                workflow_name, workflow_state = work.workflow_name_state(i, workflows, verbose)
                temp_start, temp_close, diff_temp = work.calculate_development_time(i, workflows, verbose)
                if (output == "json"):
                    workflow_json = js.json_transform(workflow_name, workflow_state, temp_start, temp_close, diff_temp, store_infos_dict, runs_time_dict)
                    json_data[repo_path].append(workflow_json)  # Adicionada dicionário com as análises produzidas
                elif(output == "csv"):
                    workflow_df = csv.csv_transform(workflow_name, workflow_state, temp_start, temp_close, diff_temp, store_infos_dict, runs_time_dict)
                    df_data.append(workflow_df)   
            else: #se estiver é porque devemos descarta-lo pois não temos runs de sucesso
                continue          
    if (output == "json"):
        js.build_json_file(name, json_data) # Função que cria arquivo .json
    else:
        csv.build_csv_file(name, df_data)
    prt.my_print(json_data, verbose) # Printa saídas caso desejado
    create_log(requests_dict_count, name) # Cria log para analisar quantidade de requests

if (__name__ == "__main__"):
    main()    