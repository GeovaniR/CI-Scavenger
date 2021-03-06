import requests
from log_requests import requests_dict_count
from datetime import datetime
import get_sucess_runs_info as run_sucess 

def loop_to_calculate_n_runs_execution_time(n_runs, n_runs_sucess, runs_sucess, runs_time_list): # Calcula o tempo de execução da últimas n_runs que foram sucesso , caso impossível pega todas as runs disponível 
    if(n_runs > n_runs_sucess): # Verifica se temos o número de runs com sucesso suficiente, pois o workflow pode ter 20 runs e só ter 6 runs que foram sucesso
        for i in range(0, n_runs_sucess): # Faz o loop de cálculo do tempo médio, para o total de runs sucesso disponível, levando em conta que é menor que o solicitado
            runs_time_list = run_sucess.calculate_run_sucess_execution_time(runs_sucess, i, runs_time_list)
    else: # Se tiver o número de runs suficiente usa a quantidade máxima de runs do workflow
        for i in range(0, n_runs): 
            runs_time_list = run_sucess.calculate_run_sucess_execution_time(runs_sucess, i, runs_time_list)             
    return(runs_time_list)
    
def calculate_runs_data_freq(runs, i, runs_time_dict):
    run_time = runs[i].get("run_started_at") # Recupera quando a última execução da run começou   
    if (run_time[0:7] in runs_time_dict):
        runs_time_dict[run_time[0:7]] += 1
    else:
        runs_time_dict[run_time[0:7]] = 1        
    return(runs_time_dict)

def calculate_time_between_runs_execution(runs, i, runs_diff_time, n_runs):
    if (i+1 < n_runs): # Seu loop tem que ser até i-1
        run_time_start = runs[i].get("created_at") # Recupera quando a run começou
        rum_time_start_2 = runs[i+1].get("created_at") # Recupera quando a run anterior começou
        run_start = datetime.strptime( run_time_start, "%Y-%m-%dT%H:%M:%SZ") # Transforma de string para data
        run_start_2 = datetime.strptime(rum_time_start_2, "%Y-%m-%dT%H:%M:%SZ") # Transforma de string para data
        diff_temp = run_start - run_start_2 # Calcula o tempo entre as execuções
        runs_diff_time.append(diff_temp.total_seconds()) # Adiciona numa lista
    return(runs_diff_time)    

def runs_path(i, n, workflows, request_path, username, token):
    id = workflows[i].get("id") # Recupera ID do pipeline
    path = request_path + "/{0}/runs?per_page={1}".format(id, n) # Junta caminho para as runs com id do pipeline
    res_runs = requests.get(path, auth= (username, token)) # Fazendo request
    requests_dict_count["runs_path"] += 1 # Adicionando que a função executou mais um request
    json_runs = res_runs.json() # Transformando em json
    n_runs = int(json_runs["total_count"]) # Recupera o número de runs
    runs = json_runs["workflow_runs"] # Informação das runs
    return(n_runs, runs)
   