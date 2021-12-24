import requests
import statistics

def my_print(string_param, verbose):
    if(verbose):
        print(string_param)
    return()

def define_path(username, token, owner, repo, verbose): ## Define os caminhos, cálcula o número de pipelines e salva as informçaões dos workflow em um json
    repo_path = owner + "/" + repo # Caminho até o repositório
    api_url = "https://api.github.com/repos/" 
    full_repo_path = api_url + repo_path
    request_path = full_repo_path + "/actions/workflows" # Caminho que recupera os workflows
    request_workflows = requests.get(request_path, auth= (username, token)) # Comando que recupera as informações
    workflows_json = request_workflows.json()
    n_pipelines = workflows_json["total_count"] # Obtendo a quantidade de workflows no repositório
    workflows = workflows_json["workflows"]
    my_print("----------------------------------------------------------------------", verbose)
    my_print("Número de worflows: {0}".format(n_pipelines), verbose)
    return(repo_path, full_repo_path, request_path, workflows, n_pipelines)

def workflow_name_state(i, workflows, verbose):
    my_print("----------------------------------------------------------------------", verbose)
    workflow_name = workflows[i].get("name") # Recupera o nome do Pipeline
    workflow_state = workflows[i].get("state") # Recupera se o Pipeline está ativo
    my_print("Workflow Name: {0}".format(workflow_name), verbose) 
    my_print("Estado do Workflow: {0}".format(workflow_state), verbose) 
    return(workflow_name, workflow_state)
    
        