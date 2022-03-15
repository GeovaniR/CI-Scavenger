import requests
import print_infos as prt
from datetime import datetime

def define_workflow_path(username, token, owner, repo, verbose): ## Define os caminhos, cálcula o número de pipelines e salva as informçaões dos workflow em um json
    repo_path = owner + "/" + repo # Caminho até o repositório
    api_url = "https://api.github.com/repos/" # Caminho da api
    full_repo_path = api_url + repo_path # Forma caminho até o repositório
    request_path = full_repo_path + "/actions/workflows" # Caminho que recupera os workflows
    request_workflows = requests.get(request_path, auth= (username, token)) # Request das informações dos workflows
    workflows_json = request_workflows.json() # Transforma em .json
    n_pipelines = workflows_json["total_count"] # Obtendo a quantidade de workflows no repositório
    workflows = workflows_json["workflows"] # Salvando varíavel com informações do workflow
    prt.my_print("----------------------------------------------------------------------", verbose) # Embelezando saídas
    prt.my_print("Número de worflows: {0}".format(n_pipelines), verbose)
    prt.my_print("----------------------------------------------------------------------", verbose) # Embelezando saídas
    return(repo_path, full_repo_path, request_path, workflows, n_pipelines)

def workflow_name_state(i, workflows, verbose): # Função que recupera o nome e o estado do workflow
    workflow_name = workflows[i].get("name") # Recupera o nome do Pipeline
    workflow_state = workflows[i].get("state") # Recupera se o Pipeline está ativo
    prt.my_print("Workflow Name: {0}".format(workflow_name), verbose) 
    prt.my_print("Estado do Workflow: {0}".format(workflow_state), verbose) 
    return(workflow_name, workflow_state)

## Recupera quando o pipeline foi criado e a ultima vez que foi atualizado, além de calcular a diferença entre essas datas *calculate_development_time*
def calculate_development_time(i, workflows, verbose):
    temp_start = workflows[i].get("created_at") # Recupera quando o workflow foi criado
    temp_close = workflows[i].get("updated_at") # Recupera quando foi a última atualização do workflow
    temp_start_date = datetime.strptime(temp_start, "%Y-%m-%dT%H:%M:%S.%f%z") # Transforma de string para data
    temp_close_date = datetime.strptime(temp_close, "%Y-%m-%dT%H:%M:%S.%f%z") # Transforma de string para data
    prt.my_print("Data de Criação: {0}".format(temp_start), verbose)
    prt.my_print("Última atualização: {0}".format(temp_close), verbose)
    diff_temp = str(temp_close_date - temp_start_date) # Calcula o tempo entre data de criação e atualização
    diff_temp = diff_temp.replace(",", "")
    prt.my_print("Tempo de Desenvolvimento do Workflow: {0}".format(diff_temp), verbose)
    prt.my_print("----------------------------------------------------------------------", verbose) # Embelezando saídas
    return (temp_start, temp_close, diff_temp)    
        