### Algoritmo para recuperar informações dos Pipelines dos repos
### Pip install requests - Instala biblioteca

## Importando bibliotecas
import requests
from datetime import datetime, timedelta
import statistics

def main():
    username = input("Username:") # Entrada Username git hub
    token = input("Token:") # Entrada do token de validação
    owner = input("Repository Owner:") # Entrada do nome do Dono do repo
    repo = input("Repository Name:") # Entrada do nome do repo
    n = int(input("Número de runs para ánalise:"))
    full_repo_path, request_path, workflows, n_pipelines = define_path(username, token, owner, repo) 
    for i in range(0, n_pipelines): ## Loop para que seja rodada as funções em cada pipeline
        workflow_name_state(i, workflows)
        calculate_development_time(i, workflows)
        calculate_runs(i, n, workflows, username, token, request_path, full_repo_path)

def define_path(username, token, owner, repo): ## Define os caminhos, cálcula o número de pipelines e salva as informçaões dos workflow em um json
    repo_path = owner + "/" + repo
    api_url = "https://api.github.com/repos/"
    full_repo_path = api_url + repo_path
    request_path = full_repo_path + "/actions/workflows"
    request_workflows = requests.get(request_path, auth= (username, token))
    workflows_json = request_workflows.json()
    n_pipelines = workflows_json["total_count"]
    workflows = workflows_json["workflows"]
    print("----------------------------------------------------------------------")
    print("Número de worflows:", n_pipelines)
    return(full_repo_path, request_path, workflows, n_pipelines)

def workflow_name_state(i, workflows):
    print("---------------------------------------------------------------------")
    print("Workflow Name:",workflows[i].get("name")) # Recupera o nome do Pipeline
    print("Estado do Workflow:", workflows[i].get("state")) # Recupera se o Pipeline está ativo

## Recupera quando o pipeline foi criado e a ultima vez que foi atualizado, além de calcular a diferença entre essas datas *calculate_development_time*
def calculate_development_time(i, workflows):
    temp_start = workflows[i].get("created_at")
    temp_close = workflows[i].get("updated_at")
    print("Data de Criação:",temp_start)
    print("Última atualização:",temp_close)
    temp_start_date = datetime(year = int(temp_start[0:4]), month = int(temp_start[5:7]), day = int(temp_start[8:10]), hour = int(temp_start[11:13]), minute = int(temp_start[14:16]), second = int(temp_start[17:19]))
    temp_close_date = datetime(year = int(temp_close[0:4]), month = int(temp_close[5:7]), day = int(temp_close[8:10]), hour = int(temp_close[11:13]), minute = int(temp_close[14:16]), second = int(temp_close[17:19]))
    diff_temp = temp_close_date - temp_start_date
    return (print("Tempo de Desenvolvimento do Workflow:", diff_temp))

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
    elif (conclusion != "action_required"):
        failed = +1    
    return(sucess, failed) 

# Recupera informações sobre o número de jobs nas runs do pipeline e adiciona numa lista
def count_jobs_runs(i, runs, n_jobs_list, username, token, full_repo_path):
    id_jobs = runs[i].get("id")
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

def print_information(perc_sucess, perc_branch_main, perc_branch_outros, runs_time_list, n_jobs_list, n_runs):
    print("Porcentagem de sucesso: {:.2f}%".format(perc_sucess))       
    print("Porcentagem de Execuções relacionadas a Branch Main {:.2f} %  /  Porcentagem ligada a Ramificações {:.2f} %".format(perc_branch_main, perc_branch_outros))
    print("Média (Tempo de Execução): {0}  /  Desvio Padrão (Tempo de Execução): {1}".format(timedelta(seconds= int(statistics.mean(runs_time_list))), timedelta(seconds= int(statistics.stdev(runs_time_list)))))
    print("Média de jobs no Pipeline:{0}".format(statistics.mean(n_jobs_list)))
    print("Número de runs:", n_runs)
    return

def calculate_perc(sucess, n, failed, branch_main_ativation):
    perc_sucess = sucess/(n-failed) *100 # Calcula porcentagem média de sucesso
    perc_branch_main = branch_main_ativation/n *100 # Calcula a porcentagem de runs relacionadas a branch main
    perc_branch_outros = (n-branch_main_ativation)/n *100 # Calcula a porcentagem de runs relacionadas a outras branchs
    return (perc_sucess, perc_branch_main, perc_branch_outros) 

# Função principal que chama as secundárias para calcular as informações
def calculate_runs(i, n, workflows, username, token, request_path, full_repo_path): # n define quantos runs serão pegas
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
        print("Só é possível calcular as estastísticas para {0} runs".format(n_runs))          
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
            runs_time_list = calculate_runs_time(runs_sucess, i, runs_time_list)
        perc_sucess, perc_branch_main, perc_branch_outros = calculate_perc(sucess, n, failed, branch_main_ativation)    
    return(print_information(perc_sucess, perc_branch_main, perc_branch_outros, runs_time_list, n_jobs_list, n_runs))
    
if __name__ == "__main__":
    main()
    