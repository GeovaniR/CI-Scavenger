import requests
import print_functions as prt
from datetime import datetime

def define_workflow_path(username, token, owner, repo, verbose): ## Define os caminhos, cálcula o número de pipelines e salva as informçaões dos workflow em um json
    repo_path = owner + "/" + repo # Caminho até o repositório
    api_url = "https://api.github.com/repos/" 
    full_repo_path = api_url + repo_path
    request_path = full_repo_path + "/actions/workflows" # Caminho que recupera os workflows
    request_workflows = requests.get(request_path, auth= (username, token)) # Comando que recupera as informações
    workflows_json = request_workflows.json()
    n_pipelines = workflows_json["total_count"] # Obtendo a quantidade de workflows no repositório
    workflows = workflows_json["workflows"]
    prt.my_print("----------------------------------------------------------------------", verbose)
    prt.my_print("Número de worflows: {0}".format(n_pipelines), verbose)
    return(repo_path, full_repo_path, request_path, workflows, n_pipelines)

def workflow_name_state(i, workflows, verbose):
    prt.my_print("----------------------------------------------------------------------", verbose)
    workflow_name = workflows[i].get("name") # Recupera o nome do Pipeline
    workflow_state = workflows[i].get("state") # Recupera se o Pipeline está ativo
    prt.my_print("Workflow Name: {0}".format(workflow_name), verbose) 
    prt.my_print("Estado do Workflow: {0}".format(workflow_state), verbose) 
    return(workflow_name, workflow_state)

## Recupera quando o pipeline foi criado e a ultima vez que foi atualizado, além de calcular a diferença entre essas datas *calculate_development_time*
def calculate_development_time(i, workflows, verbose):
    temp_start = workflows[i].get("created_at") # Recupera quando o workflow foi criado
    temp_close = workflows[i].get("updated_at") # Recupera quando foi a última atualização do workflow
    prt.my_print("Data de Criação: {0}".format(temp_start), verbose)
    prt.my_print("Última atualização: {0}".format(temp_close), verbose)
    temp_start_date = datetime(year = int(temp_start[0:4]), month = int(temp_start[5:7]), day = int(temp_start[8:10]), hour = int(temp_start[11:13]), minute = int(temp_start[14:16]), second = int(temp_start[17:19]))
    temp_close_date = datetime(year = int(temp_close[0:4]), month = int(temp_close[5:7]), day = int(temp_close[8:10]), hour = int(temp_close[11:13]), minute = int(temp_close[14:16]), second = int(temp_close[17:19]))
    diff_temp = str(temp_close_date - temp_start_date) # Calcula o tempo entre data de criação e atualização
    diff_temp = diff_temp.replace(",", "")
    prt.my_print("Tempo de Desenvolvimento do Workflow: {0}".format(diff_temp), verbose)
    return (temp_start, temp_close, diff_temp)    
        