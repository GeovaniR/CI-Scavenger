### Algoritmo para recuperar informações dos Pipelines dos repos
### Pip install requests - Instala biblioteca

## Importando bibliotecas
import get_workflow_infos as work
import calculate_stats as calc
import build_and_validate_json as js
import print_infos as prt
import verify_pipeline as pipeline

def main():
    username = input("Username:") # Entrada Username git hub
    token = input("Token:") # Entrada do token de validação
    owner = input("Repository Owner:") # Entrada do nome do Dono do repo
    repo = input("Repository Name:") # Entrada do nome do repo
    n = int(input("Número de runs para ánalise:")) # Entrada do número de runs que vamos analisar
    verbose = int(input("Retornar texto além do Json?:")) # Entrada binária
    name_json = str(input("Nome do arquivo de saída:")) # Entrada do nome do arquivo de saída
    name_json = name_json + ".json" # Entrada do nome do arquivo de saída
    repo_path, full_repo_path, request_path, workflows, n_pipelines = work.define_workflow_path(username, token, owner, repo, verbose)
    json_data = {repo_path:[{"n_worfklows" : n_pipelines}]}
    for i in range(0, n_pipelines): ## Loop para que seja rodada as funções em cada pipeline
        validate_worflow = pipeline.investigate_workflow_keywords(i, n, workflows, request_path, username, token, full_repo_path) # Valdia se o workflow tem destino a CI/CD para permitir análise
        if (validate_worflow):
            workflow_name, workflow_state = work.workflow_name_state(i, workflows, verbose)
            temp_start, temp_close, diff_temp = work.calculate_development_time(i, workflows, verbose)
            perc_sucess, perc_branch_main, perc_branch_outros, runs_time_list, n_jobs_list, n_runs, n_runs_analyzed, runs_time_dict, runs_diff_time = calc.calculate_workflows_stats(i, n, workflows, username, token, request_path, full_repo_path, verbose)
            workflow_json = js.json_transform(workflow_name, workflow_state, temp_start, temp_close, diff_temp, perc_sucess, perc_branch_main, perc_branch_outros, runs_time_list, n_jobs_list, n_runs, n_runs_analyzed, runs_time_dict, runs_diff_time)
            json_data[repo_path].append(workflow_json)  # Adicionada dicionário com as análises produzidas      
    isValid = js.validateJSON(json_data) # Valida Texto que será transformado em Json
    js.build_json_file(isValid, name_json, json_data) # Função que cria arquivo .json
    prt.my_print(json_data, verbose) # Printa saídas caso desejado

if (__name__ == "__main__"):
    main()    