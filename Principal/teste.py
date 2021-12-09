### Algoritmo para recuperar informações dos Pipelines dos repos
### Pip install requests - Instala biblioteca

## Importando bibliotecas
import requests
from datetime import datetime, timedelta
import statistics
import json

def main():
    username = input("Username:") # Entrada Username git hub
    token = input("Token:") # Entrada do token de validação
    owner = input("Repository Owner:") # Entrada do nome do Dono do repo
    repo = input("Repository Name:") # Entrada do nome do repo
    n = int(input("Número de runs para ánalise:")) # Entrada do número de runs que vamos analisar
    verbose = int(input("Retornar texto além do Json?:")) # Entrada binária
    repo_path, full_repo_path, request_path, workflows, n_pipelines = define_path(username, token, owner, repo, verbose)
    json_data = {repo_path:[{"n_worfklows" : n_pipelines}]}
    for i in range(0, n_pipelines): ## Loop para que seja rodada as funções em cada pipeline
        workflow_name, workflow_state = workflow_name_state(i, workflows, verbose)
        temp_start, temp_close, diff_temp = calculate_development_time(i, workflows, verbose)
        perc_sucess, perc_branch_main, perc_branch_outros, runs_time_list, n_jobs_list, n_runs = calculate_runs(i, n, workflows, username, token, request_path, full_repo_path, verbose)
        workflow_json = json_transform(workflow_name, workflow_state, temp_start, temp_close, diff_temp, perc_sucess, perc_branch_main, perc_branch_outros, runs_time_list, n_jobs_list, n_runs)
        json_data[repo_path].append(workflow_json)
    json_data = json.dumps(json_data)
    print(json_data)   

def my_print(string_param, verbose):
    if(verbose):
        print(string_param)
    return()

def json_transform(workflow_name, workflow_state, temp_start, temp_close, diff_temp, perc_sucess, perc_branch_main, perc_branch_outros, runs_time_list, n_jobs_list, n_runs):
    meean_time = str(timedelta(seconds= int(statistics.mean(runs_time_list))))
    dev_time = str(timedelta(seconds= int(statistics.stdev(runs_time_list))))
    mean_jobs = str(statistics.mean(n_jobs_list))
    perc_sucess = "{0} %".format(round(perc_sucess, 2))
    perc_branch_main = "{0} %".format(round(perc_branch_main, 2))
    perc_branch_outros = "{0} %".format(round(perc_branch_outros, 2))
    workflow_json = {
            "Workflow_Name":workflow_name, "State":workflow_state, "Created_at": temp_start, "Updated_at" :temp_close,
            "Dev_time":diff_temp, "success_rate":perc_sucess, "Branch_Main_rate":perc_branch_main, "Other_Branchs_rate":perc_branch_outros,
            "Mean(Execution time)":meean_time, "Std_deviation(Execution time)": dev_time, "Jobs_mean":mean_jobs, "total_runs": n_runs
        }
    return(workflow_json)

def define_path(username, token, owner, repo, verbose): ## Define os caminhos, cálcula o número de pipelines e salva as informçaões dos workflow em um json
    repo_path = owner + "/" + repo
    api_url = "https://api.github.com/repos/"
    full_repo_path = api_url + repo_path
    request_path = full_repo_path + "/actions/workflows"
    request_workflows = requests.get(request_path, auth= (username, token))
    workflows_json = request_workflows.json()
    n_pipelines = workflows_json["total_count"]
    workflows = workflows_json["workflows"]
    my_print("----------------------------------------------------------------------", verbose)
    my_print("Número de worflows:{0}".format(n_pipelines), verbose)
    return(repo_path, full_repo_path, request_path, workflows, n_pipelines)

def workflow_name_state(i, workflows, verbose):
    my_print("----------------------------------------------------------------------", verbose)
    workflow_name = workflows[i].get("name")
    workflow_state = workflows[i].get("state")
    my_print("Workflow Name:{0}".format(workflow_name), verbose) # Recupera o nome do Pipeline
    my_print("Estado do Workflow:{0}".format(workflow_state), verbose) # Recupera se o Pipeline está ativo
    return(workflow_name, workflow_state)

## Recupera quando o pipeline foi criado e a ultima vez que foi atualizado, além de calcular a diferença entre essas datas *calculate_development_time*
def calculate_development_time(i, workflows, verbose):
    temp_start = workflows[i].get("created_at")
    temp_close = workflows[i].get("updated_at")
    my_print("Data de Criação:{0}".format(temp_start), verbose)
    my_print("Última atualização:{0}".format(temp_close), verbose)
    temp_start_date = datetime(year = int(temp_start[0:4]), month = int(temp_start[5:7]), day = int(temp_start[8:10]), hour = int(temp_start[11:13]), minute = int(temp_start[14:16]), second = int(temp_start[17:19]))
    temp_close_date = datetime(year = int(temp_close[0:4]), month = int(temp_close[5:7]), day = int(temp_close[8:10]), hour = int(temp_close[11:13]), minute = int(temp_close[14:16]), second = int(temp_close[17:19]))
    diff_temp = str(temp_close_date - temp_start_date)
    diff_temp = diff_temp.replace(",", "")
    my_print("Tempo de Desenvolvimento do Workflow:{0}".format(diff_temp), verbose)
    return (temp_start, temp_close, diff_temp)

# Recupera informações sobre o tempo que levou para ser executado uma das últimas runs do pipeline e adiciona numa lista
def calculate_runs_time(runs_sucess, i, runs_time_list):
    if(runs_sucess[i].get("run_attempt") == "1"):
        run_time_start = runs_sucess[i].get("created_at")
    else:
        run_time_start = runs_sucess[i].get("run_started_at")
    rum_time_finish = runs_sucess[i].get("updated_at")    
    run_start_date = datetime(year = int(run_time_start[0:4]), month = int(run_time_start[5:7]), day = int(run_time_start[8:10]), hour = int(run_time_start[11:13]), minute = int(run_time_start[14:16]), second = int(run_time_start[17:19]))
    run_finish_date = datetime(year = int(rum_time_finish[0:4]), month = int(rum_time_finish[5:7]), day = int(rum_time_finish[8:10]), hour = int(rum_time_finish[11:13]), minute = int(rum_time_finish[14:16]), second = int(rum_time_finish[17:19]))
    diff_temp = run_finish_date - run_start_date
    runs_time_list.append(diff_temp.total_seconds())
    return (runs_time_list)    

# Recupera informação se uma run foi sucesso ou não. Obs: Tira da contagem aquelas que não temos permissão
def count_runs_sucess(i, runs, sucess, failed):
    conclusion = runs[i].get("conclusion")
    if (conclusion == "success"):
        sucess += 1  
    elif (conclusion == "action_required"):
        failed += 1    
    return(sucess, failed) 

# Recupera informações sobre o número de jobs nas runs do pipeline e adiciona numa lista
def count_jobs_runs(i, runs, n_jobs_list, username, token, full_repo_path):
    id_jobs = runs[i].get("id")
    condition = runs[i].get("conclusion")
    if (condition != "action_required"):
        path_2 = full_repo_path + "/actions/runs/{0}/jobs".format(id_jobs)
        res_jobs = requests.get(path_2, auth= (username, token)) 
        jobs = res_jobs.json()
        n_jobs = int(jobs["total_count"])
        n_jobs_list.append(n_jobs)    
    return (n_jobs_list)

# Recupera informações se uma run foi acionada relacionada branch main
def count_branch_ativation(i, runs, branch_main_ativation):
    branch = runs[i].get("head_branch")
    if (branch == "main"):
       branch_main_ativation += 1
    return(branch_main_ativation)        

def print_information(perc_sucess, perc_branch_main, perc_branch_outros, runs_time_list, n_jobs_list, n_runs, verbose):
    my_print("Porcentagem de sucesso: {:.2f}%".format(perc_sucess), verbose)       
    my_print("Porcentagem de Execuções relacionadas a Branch Main {:.2f} %  /  Porcentagem ligada a Ramificações {:.2f} %".format(perc_branch_main, perc_branch_outros), verbose)
    my_print("Média (Tempo de Execução): {0}  /  Desvio Padrão (Tempo de Execução): {1}".format(timedelta(seconds= int(statistics.mean(runs_time_list))), timedelta(seconds= int(statistics.stdev(runs_time_list)))), verbose)
    my_print("Média de jobs no Pipeline:{0}".format(statistics.mean(n_jobs_list)), verbose)
    my_print("Número de runs:{0}".format(n_runs), verbose)
    return()

def calculate_perc(sucess, n, failed, branch_main_ativation):
    perc_sucess = sucess/(n-failed) *100 # Calcula porcentagem média de sucesso
    perc_branch_main = branch_main_ativation/n *100 # Calcula a porcentagem de runs relacionadas a branch main
    perc_branch_outros = (n-branch_main_ativation)/n *100 # Calcula a porcentagem de runs relacionadas a outras branchs
    return (perc_sucess, perc_branch_main, perc_branch_outros) 

# Função principal que chama as secundárias para calcular as informações
def calculate_runs(i, n, workflows, username, token, request_path, full_repo_path, verbose): # n define quantos runs serão pegas
    id = workflows[i].get("id") # Recupera ID do pipeline
    path = request_path + "/{0}/runs?per_page={1}".format(id, n) # Junta caminho para as runs com id do pipeline
    res_runs = requests.get(path, auth= (username, token)) # Fazendo request
    json_runs = res_runs.json() # Transformando em json
    n_runs = json_runs["total_count"] # Recupera o número de runs
    runs = json_runs["workflow_runs"] # Informação das runs
    path_sucess = request_path + "/{0}/runs?status=success&per_page={1}".format(id, n) # caminho para últimas runs com sucesso
    res_runs_sucess = requests.get(path_sucess, auth= (username, token)) # request das últimas runs com sucesso
    json_runs_sucess = res_runs_sucess.json() # Transformando em json
    runs_sucess = json_runs_sucess["workflow_runs"] # Informação das runs de sucesso
    n_runs_sucess = json_runs_sucess["total_count"] # Informação da quantidade de runs de sucesso
    runs_time_list = [] # Lista para salvar o tempo das últimas n runs
    n_jobs_list = [] # Lista para salvar o número de jobs nas últimas n runs
    sucess, failed, branch_main_ativation = 0, 0, 0
    if (n_runs < n): # Ignora o caso de Pipelines que não são utilizados, mas estão no actions do repo   
        for i in range(0, n_runs): # Faz o loop das funções para o máximo de runs dísponível, mesmo que menor que n
            sucess, failed = count_runs_sucess(i, runs, sucess, failed)
            branch_main_ativation = count_branch_ativation(i, runs, branch_main_ativation)
            count_jobs_runs(i, runs, n_jobs_list, username, token, full_repo_path)
        if(n_runs > n_runs_sucess): # Verifica se temos o número de runs com sucesso suficiente
            for i in range(0, n_runs_sucess): # Faz o loop de cálculo do tempo médio, para o total de runs sucesso disponível
                runs_time_list = calculate_runs_time(runs_sucess, i, runs_time_list)
        else:
            for i in range(0, n_runs): 
                runs_time_list = calculate_runs_time(runs_sucess, i, runs_time_list)     
        perc_sucess, perc_branch_main, perc_branch_outros = calculate_perc(sucess, n_runs, failed, branch_main_ativation)
        my_print("Só é possível calcular as estastísticas para {0} runs".format(n_runs), verbose)          
    else:   
        for i in range(0, n):
            sucess, failed = count_runs_sucess(i, runs, sucess, failed)
            branch_main_ativation = count_branch_ativation(i, runs, branch_main_ativation)
            count_jobs_runs(i, runs, n_jobs_list, username, token, full_repo_path)
        if (n > n_runs_sucess): # Verifica se temos o número de runs com sucesso suficiente
            for i in range(0, n_runs_sucess): # Faz o loop de cálculo do tempo médio, para o total de runs sucesso disponível
                runs_time_list = calculate_runs_time(runs_sucess, i, runs_time_list)
        else:
            for i in range(0, n):
                runs_time_list = calculate_runs_time(runs_sucess, i, runs_time_list)
        perc_sucess, perc_branch_main, perc_branch_outros = calculate_perc(sucess, n, failed, branch_main_ativation)
    print_information(perc_sucess, perc_branch_main, perc_branch_outros, runs_time_list, n_jobs_list, n_runs, verbose)
    return(perc_sucess, perc_branch_main, perc_branch_outros, runs_time_list, n_jobs_list, n_runs)
    
if __name__ == "__main__":
    main()
    