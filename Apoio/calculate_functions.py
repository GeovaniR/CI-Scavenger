import statistics
import requests
from datetime import datetime, timedelta

## Função que verifica se deve printar ou não os resultados
def my_print(string_param, verbose):
    if(verbose):
        print(string_param)
    return()

def print_information(perc_sucess, perc_branch_main, perc_branch_outros, runs_time_list, n_jobs_list, n_runs, verbose):
    my_print("Porcentagem de sucesso: {:.2f}%".format(perc_sucess), verbose)       
    my_print("Porcentagem de Execuções relacionadas a Branch Main {:.2f} %  /  Porcentagem ligada a Ramificações {:.2f} %".format(perc_branch_main, perc_branch_outros), verbose)
    my_print("Média (Tempo de Execução): {0}  /  Desvio Padrão (Tempo de Execução): {1}".format(timedelta(seconds= int(statistics.mean(runs_time_list))), timedelta(seconds= int(statistics.stdev(runs_time_list)))), verbose)
    my_print("Média de jobs no Pipeline:{0}".format(statistics.mean(n_jobs_list)), verbose)
    my_print("Número de runs:{0}".format(n_runs), verbose)
    return()

## Recupera quando o pipeline foi criado e a ultima vez que foi atualizado, além de calcular a diferença entre essas datas *calculate_development_time*
def calculate_development_time(i, workflows, verbose):
    temp_start = workflows[i].get("created_at") # Recupera quando o workflow foi criado
    temp_close = workflows[i].get("updated_at") # Recupera quando foi a última atualização do workflow
    my_print("Data de Criação:{0}".format(temp_start), verbose)
    my_print("Última atualização:{0}".format(temp_close), verbose)
    temp_start_date = datetime(year = int(temp_start[0:4]), month = int(temp_start[5:7]), day = int(temp_start[8:10]), hour = int(temp_start[11:13]), minute = int(temp_start[14:16]), second = int(temp_start[17:19]))
    temp_close_date = datetime(year = int(temp_close[0:4]), month = int(temp_close[5:7]), day = int(temp_close[8:10]), hour = int(temp_close[11:13]), minute = int(temp_close[14:16]), second = int(temp_close[17:19]))
    diff_temp = str(temp_close_date - temp_start_date) # Calcula o tempo entre data de criação e atualização
    diff_temp = diff_temp.replace(",", "")
    my_print("Tempo de Desenvolvimento do Workflow:{0}".format(diff_temp), verbose)
    return (temp_start, temp_close, diff_temp)

# Recupera informações sobre o tempo que levou para ser executado uma das últimas runs do pipeline e adiciona numa lista
def calculate_runs_time(runs_sucess, i, runs_time_list):
    if(runs_sucess[i].get("run_attempt") == "1"): # Verifica se é a primeira execução daquela run
        run_time_start = runs_sucess[i].get("created_at") # Recupera quando a run começou
    else:
        run_time_start = runs_sucess[i].get("run_started_at") # Recupera quando a última execução da run começou
    rum_time_finish = runs_sucess[i].get("updated_at") # Recupera quando a run terminou
    run_start_date = datetime(year = int(run_time_start[0:4]), month = int(run_time_start[5:7]), day = int(run_time_start[8:10]), hour = int(run_time_start[11:13]), minute = int(run_time_start[14:16]), second = int(run_time_start[17:19]))
    run_finish_date = datetime(year = int(rum_time_finish[0:4]), month = int(rum_time_finish[5:7]), day = int(rum_time_finish[8:10]), hour = int(rum_time_finish[11:13]), minute = int(rum_time_finish[14:16]), second = int(rum_time_finish[17:19]))
    diff_temp = run_finish_date - run_start_date # Calcula o tempo
    runs_time_list.append(diff_temp.total_seconds()) # Adiciona numa lista
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

# Calcula porcentagem de sucesso
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
        n_runs_analyses = n_runs             
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
        n_runs_analyses = n        
        perc_sucess, perc_branch_main, perc_branch_outros = calculate_perc(sucess, n, failed, branch_main_ativation)
    print_information(perc_sucess, perc_branch_main, perc_branch_outros, runs_time_list, n_jobs_list, n_runs, verbose)
    return(perc_sucess, perc_branch_main, perc_branch_outros, runs_time_list, n_jobs_list, n_runs, n_runs_analyses)