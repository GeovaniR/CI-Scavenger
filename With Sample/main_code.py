### Algoritmo para recuperar informações dos Pipelines dos repos

## Import libraries
import sys, getopt
import get_workflow_infos as work
import calculate_stats as calc
import build_json as js
import print_infos as prt
import verify_pipeline as pipeline
from log_requests import requests_dict_count, create_log
import build_csv as csv

def main(argv):
    ## Define inputs
    username = None # Username git hub
    token = None # Validation Token
    owner = None # Repo Owner
    repo = None # Repo name
    n = None # Runs amount to analyze 
    verbose = None # Print informations (1 or 0)
    name = None # Output name
    output = None # Output format
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "u:t:ow:r:n:v:j:out")
    except:
        print("Error")
    for opt, arg in opts:
        if opt in ['-u']:
            username = arg
        elif opt in ['-t']:
            token = arg
        elif opt in ['-ow']:
            owner = arg    
        elif opt in ['-r']:
            repo = arg
        elif opt in ['-n']:
            n = int(arg)
        elif opt in ['-v']:
            verbose = int(arg)
        elif opt in ['-j']:
            name = arg
        elif opt in ['-out']:
            output = arg    
    # Execução das funções
    repo_path, full_repo_path, request_path, workflows, n_pipelines = work.define_workflow_path(username, token, owner, repo, verbose)
    json_data = {repo_path:[]}
    for i in range(0, n_pipelines): ## Loop para que seja rodada as funções em cada pipeline
        validate_worflow = pipeline.investigate_workflow_ci_cd(i, n, workflows, request_path, username, token, full_repo_path) # Valida se o workflow tem destino a CI/CD para permitir análise
        if (validate_worflow): # Se o worklow da indícios de CI/CD, então roda funçõs para obter estatísticas
            store_infos_dict, runs_time_dict = calc.calculate_workflows_stats(i, n, workflows, username, token, request_path, full_repo_path, verbose)
            if (store_infos_dict): # Vai verificar se o dicionário está vazio, se não estiver é porque temos runs de sucesso então roda demais funções
                store_infos_dict = work.workflow_name_state(i, workflows, verbose, store_infos_dict)
                store_infos_dict = work.calculate_development_time(i, workflows, verbose, store_infos_dict)
                workflow_json = js.format_file(store_infos_dict, runs_time_dict)
                json_data[repo_path].append(workflow_json)  # Adicionada dicionário com as análises produzidas  
            else: #se estiver é porque devemos descarta-lo pois não temos runs de sucesso
                continue
                      
    if (output == "json"):
        js.build_json_file(name, json_data) # Build .json
    else:
        csv.build_csv_file(name, json_data, repo_path) # Build .csv
    prt.my_print(json_data, verbose) # Print output
    create_log(requests_dict_count, name) # Create log file
    
if __name__ == "__main__":
    main(sys.argv[1:])
    