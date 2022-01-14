import requests

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

