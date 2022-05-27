from socket import if_indextoname
import requests
from log_requests import requests_dict_count

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