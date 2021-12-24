### Algoritmo para recuperar informações dos Pipelines dos repos
### Pip install requests - Instala biblioteca

## Importando bibliotecas
import requests
from datetime import datetime, timedelta
import statistics
import json
import sys, getopt
import functions_aux as aux
import calculate_functions as calc
import json_aux as js
def main(argv):
    ## Definindo entradas
    username = None # Entrada Username git hub
    token = None # Entrada do token de validação
    owner = None # Entrada do nome do Dono do repo
    repo = None # Entrada do nome do repo
    n = None # Entrada do número de runs que vamos analisar
    verbose = None # Entrada binária
    name_json = None # Entrada do nome do arquivo de saída
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "u:t:o:r:n:v:j:")
    except:
        print("Error")
    for opt, arg in opts:
        if opt in ['-u']:
            username = arg
        elif opt in ['-t']:
            token = arg
        elif opt in ['-o']:
            owner = arg    
        elif opt in ['-r']:
            repo = arg
        elif opt in ['-n']:
            n = int(arg)
        elif opt in ['-v']:
            verbose = int(arg)
        elif opt in ['-j']:
            name_json = arg
    # Execução das funções
    repo_path, full_repo_path, request_path, workflows, n_pipelines = aux.define_path(username, token, owner, repo, verbose)
    json_data = {repo_path:[{"n_worfklows" : n_pipelines}]}
    for i in range(0, n_pipelines): ## Loop para que seja rodada as funções em cada pipeline
        workflow_name, workflow_state = aux.workflow_name_state(i, workflows, verbose)
        temp_start, temp_close, diff_temp = calc.calculate_development_time(i, workflows, verbose)
        perc_sucess, perc_branch_main, perc_branch_outros, runs_time_list, n_jobs_list, n_runs, n_runs_analyzed, runs_time_dict = calc.calculate_runs(i, n, workflows, username, token, request_path, full_repo_path, verbose)
        workflow_json = js.json_transform(workflow_name, workflow_state, temp_start, temp_close, diff_temp, perc_sucess, perc_branch_main, perc_branch_outros, runs_time_list, n_jobs_list, n_runs, n_runs_analyzed, runs_time_dict)
        json_data[repo_path].append(workflow_json)
    name_json = name_json + ".json" # Entrada do nome do arquivo de saída
    json_test = str(json_data) # Salva texto dicionario em string para função de testagem
    json_test = json_test.replace("'", '"') # Corrige aspas incorretas
    isValid = js.validateJSON(json_test) # Valida Texto que será transformado em Json
    if (isValid):
        with open(name_json, 'w', encoding='utf-8') as outfile:
            json.dump(json_data, outfile, ensure_ascii=False, indent=2)
    else:
        return(print("Arquivo json não está formatado corretamente"))    
    aux.my_print(json_data, verbose)   
    
if __name__ == "__main__":
    main(sys.argv[1:])
    