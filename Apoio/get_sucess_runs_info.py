import requests
from datetime import datetime

# Recupera o tempo de execução das últimas runs de sucesso estipuladas
def calculate_run_sucess_execution_time(runs_sucess, i, runs_time_list):
    if(runs_sucess[i].get("run_attempt") == "1"): # Verifica se é a primeira execução daquela run, pois uma run pode ter inúmeras tentativas e só queremos o tempo de sua última execução
        run_time_start = runs_sucess[i].get("created_at") # Se só tiver uma execução da run recuperamos o tempo que foi criada
    else:
        run_time_start = runs_sucess[i].get("run_started_at") # Se tiver mais de uma execução recupera quando a última execução da run começou
    run_time_finish = runs_sucess[i].get("updated_at") # Recupera quando a run terminou
    run_start_date = datetime.strptime(run_time_start, "%Y-%m-%dT%H:%M:%SZ") # Transforma de string para data
    run_finish_date = datetime.strptime(run_time_finish, "%Y-%m-%dT%H:%M:%SZ") # Transforma de string para data
    diff_temp = run_finish_date - run_start_date # Calcula a diferença entre o tempo de começo e fim
    runs_time_list.append(diff_temp.total_seconds()) # Adiciona numa lista que armazena o tempo de execução para cada run
    return (runs_time_list) # retorna lista atualizada

def runs_sucess_path(i, n, workflows, request_path, username, token): # Função que define o caminho para as runs
    id = workflows[i].get("id") # Recupera ID do pipeline
    path_sucess = request_path + "/{0}/runs?status=success&per_page={1}".format(id, n) # caminho para últimas n runs com sucesso
    res_runs_sucess = requests.get(path_sucess, auth= (username, token)) # request das últimas runs com sucesso
    json_runs_sucess = res_runs_sucess.json() # Transformando em json
    runs_sucess = json_runs_sucess["workflow_runs"] # Informação das runs de sucesso
    n_runs_sucess = int(json_runs_sucess["total_count"]) # Quantidade de runs de sucesso
    return(n_runs_sucess, runs_sucess)

# Recupera informação se uma run foi sucesso ou não. Obs: Tira da contagem aquelas que não temos permissão
def count_runs_sucess(i, runs, sucess, private):
    conclusion = runs[i].get("conclusion") # Salva o estado de conclusão da run
    if (conclusion == "success"): # Verifica se foi sucesso
        sucess += 1  # Caso sucesso soma 1
    elif (conclusion == "action_required" or conclusion == "Skipped"): # Verifica se a run tem acesso fechado
        private += 1    # Caso tenha acesso fechado soma 1
    return(sucess, private)

