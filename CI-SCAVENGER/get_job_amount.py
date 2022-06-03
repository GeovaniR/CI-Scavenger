from socket import if_indextoname
import requests
from log_requests import requests_dict_count
import random

# Recupera informações sobre o número de jobs através de uma amostra das runs do pipeline e adiciona numa lista
def sample_jobs_runs(n, runs, n_jobs_list, username, token, full_repo_path): # Função que conta o número de jobs em cada run
    tamanho_amostra = n//2 # Tamanho da amostra
    if (tamanho_amostra%2 != 0):
        tamanho_amostra += 1
    bloco_1 = random.sample(range(tamanho_amostra), k= tamanho_amostra//2) # O primeiro bloco é uma amostra das runs mais recentes
    bloco_2 = random.sample(range(tamanho_amostra, n), k= tamanho_amostra//2) # O segundo bloco é uma amostra das runs mais antigas
    amostra = [*bloco_1, *bloco_2] # Junto os blocos pra formar a amostra
    for i in amostra: 
        count_jobs_runs(i, runs, n_jobs_list, username, token, full_repo_path)
    return (n_jobs_list)

# Recupera informações sobre o número de jobs percorendo todas as runs
def count_jobs_runs(i, runs, n_jobs_list, username, token, full_repo_path): # Função que conta o número de jobs em cada run
    job_id = runs[i].get("id") # Recupera id da run
    conclusion = runs[i].get("conclusion") # Recupera estado de conclusão da run
    if (conclusion != "action_required" or conclusion != "Skipped"): # Testa se o acesso as informações da run não é fechado
        job_path = full_repo_path + "/actions/runs/{0}/jobs".format(job_id) # estrutra caminho para os jobs
        job_request = requests.get(job_path, auth= (username, token)) # Faz o request dos jobs
        requests_dict_count["count_jobs_runs"] += 1 # Adicionando que a função executou mais um request
        job_json = job_request.json() # Transforma as informações em json
        n_jobs = int(job_json["total_count"]) # Recupera a quantidade total de jobs
        n_jobs_list.append(n_jobs) # Adiciona na lista que está armazenando a quantidade de jobs para cada run
    return (n_jobs_list)

def sample_or_not(sampling, runs, n_jobs_list, username, token, full_repo_path, n):
    if (sampling == "n"):
        for i in range(0, n):
            count_jobs_runs(i, runs, n_jobs_list, username, token, full_repo_path)
    elif (sampling == "y"):
        sample_jobs_runs(n, runs, n_jobs_list, username, token, full_repo_path)        