import requests
from datetime import datetime
from log_requests import requests_dict_count

def define_workflow_path(username, token, owner, repo): ## Define os caminhos, cálcula o número de pipelines e salva as informçaões dos workflow em um json
    repo_path = owner + "/" + repo # Caminho até o repositório
    api_url = "https://api.github.com/repos/" # Caminho da api
    full_repo_path = api_url + repo_path # Forma caminho até o repositório
    request_path = full_repo_path + "/actions/workflows" # Caminho que recupera os workflows
    request_workflows = requests.get(request_path, auth= (username, token)) # Request das informações dos workflows
    requests_dict_count["define_workflow_path"] += 1 # Adicionando que a função executou mais um request
    workflows_json = request_workflows.json() # Transforma em .json
    n_pipelines = workflows_json["total_count"] # Obtendo a quantidade de workflows no repositório
    workflows = workflows_json["workflows"] # Salvando varíavel com informações do workflow
    return(repo_path, full_repo_path, request_path, workflows, n_pipelines)

def workflow_name_state(i, workflows, store_infos_dict): # Função que recupera o nome e o estado do workflow
    workflow_name = workflows[i].get("name") # Recupera o nome do Pipeline
    workflow_state = workflows[i].get("state") # Recupera se o Pipeline está ativo
    store_infos_dict["Workflow_Name"] = workflow_name
    store_infos_dict["State"] = workflow_state
    return(store_infos_dict)

## Recupera quando o pipeline foi criado e a ultima vez que foi atualizado, além de calcular a diferença entre essas datas *calculate_development_time*
def calculate_development_time(i, workflows, store_infos_dict):
    temp_start = workflows[i].get("created_at") # Recupera quando o workflow foi criado
    temp_close = workflows[i].get("updated_at") # Recupera quando foi a última atualização do workflow
    temp_start_date = datetime.strptime(temp_start, "%Y-%m-%dT%H:%M:%S.%f%z") # Transforma de string para data
    temp_close_date = datetime.strptime(temp_close, "%Y-%m-%dT%H:%M:%S.%f%z") # Transforma de string para data
    temp_start = temp_start[0:10] # Salva só Ano-Mês-Dia
    temp_close = temp_close[0:10] # Salva só Ano-Mês-Dia
    diff_temp = str(temp_close_date - temp_start_date) # Calcula o tempo entre data de criação e atualização
    diff_temp = diff_temp.replace(",", "")
    store_infos_dict["Dev_time"] = diff_temp
    store_infos_dict["Created_at"] = temp_start
    store_infos_dict["Updated_at"] = temp_close
    return (store_infos_dict)    
        