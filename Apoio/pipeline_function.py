import requests
import runs_functions as runsf
from unidecode import unidecode

def investigate_workflow_keywords(i, n, workflows, request_path, username, token, full_repo_path):
    n_runs, runs = runsf.runs_path(i, n, workflows, request_path, username, token) # Runs é o arquivo json com os dados das runs e n_runs o número de runs no workflow
    keywords_dict = {"clone":0, "compile":0, "build":0, "ci": 0, "maven":0, "tests":0, "test":0, "regression": 0} # Dicionário de palavras chaves relacionadas a automação de CI/CD
    keywords_dict, words_found = verify_workflow_words(i, workflows, keywords_dict)
    if (words_found > 0 ): # Testa se encontrou alguma palavra no nome do worflow
        return(keywords_dict, True) # Caso tenha encontrado já retorna que o workflow pode ser testado
    else:    # Caso contrário testa os jobs
        keywords_dict, words_found = verify_jobs_and_steps(0, runs, keywords_dict, full_repo_path, username, token)
        if (words_found > 0 ): # Testa se encontrou alguma palavra no nome do job e passos
            return(keywords_dict, True) # Caso tenha encontrado já retorna que o workflow pode ser testado                  
    return(keywords_dict, False)

def chr_remove(old, to_remove): # Função que remove caracteres especiais
    new_string = old.lower()
    for x in to_remove:
        new_string = new_string.replace(x, '')
    return new_string

def compare_word_with_dict(name, keywords_dict): # Função que analisa a existência da palavra dentro do dicionário
    words_found = 0 # Variável que armazena o número de palavras encontradas
    name = chr_remove(name, "!@#$%¨&*()_-=+'?:<>,.\|^~`}{][;") # Remove caracteres especiais
    name = unidecode(name) # Remove acentos
    lista_palavras = name.split() # lista com as palavras da frase
    for palavra in lista_palavras: # testa de palavra em palavra com o dicionário
        if (palavra in keywords_dict):
            keywords_dict[palavra] += 1 # Caso encontre soma 1 ocorrência
            words_found += 1 # Soma uma palavra encontrada          
    return(keywords_dict, words_found) # Retorna o dicionário

def verify_workflow_words(i, workflows, keywords_dict): # Função que verifica se o nome do workflow da evidências de ser para CI/CD
    workflow_name = workflows[i].get("name") # Recupera o nome do workflow
    keywords_dict, words_found = compare_word_with_dict(workflow_name, keywords_dict) # Testa o nome do workflow
    return(keywords_dict, words_found) # Retorna o dicionário e o número de palavras encontradas

def verify_jobs_words(j, jobs, keywords_dict): # Função que verifica se o nome do Job da evidências de ser para CI/CD
    job_name = jobs[j].get("name") # Recupera o nome do Job
    keywords_dict, words_found = compare_word_with_dict(job_name, keywords_dict) # Testa o nome
    return(keywords_dict, words_found) # Retorna o dicionário e o número de palavras encontradas

def verify_steps_words(j, jobs, keywords_dict): # Função que verifica se os passos do Job fornecem evidências de CI/CD
    steps = jobs[j].get("steps") # Entra na lista de steps
    n_steps = len(steps) # recupera quantidade de steps
    for k in range(n_steps):
        step_name = steps[k].get("name") # Recupera o nome do Job
        keywords_dict, words_found = compare_word_with_dict(step_name, keywords_dict) # Testa o nome
    return(keywords_dict, words_found) # Retorna o dicionário e o número de palavras encontradas

def verify_jobs_and_steps(i, runs, keywords_dict, full_repo_path, username, token): # i percore o número de runs
    condition = runs[i].get("conclusion") 
    while (condition == "action_required"): # Loop até achar uma run sem acesso privado
        i += 1
        condition = runs[i].get("conclusion")   
    id_jobs = runs[i].get("id") # recupera id da run
    path_jobs = full_repo_path + "/actions/runs/{0}/jobs".format(id_jobs) # define caminho para os jobs da run
    res_jobs = requests.get(path_jobs, auth= (username, token)) # Executa chamada para informações dos jobs
    jobs_json = res_jobs.json() # Transformar informações para formato json
    n_jobs = int(jobs_json["total_count"]) # Recupera a quantidade total de jobs
    jobs = jobs_json["jobs"] # Entra nas informações sobre os jobs
    for j in range(n_jobs): # Percore cada Job existente
        keywords_dict, words_found = verify_jobs_words(j, jobs, keywords_dict) # Testa o nome do job
        if (words_found > 0):
             return(keywords_dict, words_found) # Retorna o dicionário e o número de palavras encontradas 
    for j in range(n_jobs): # Percore cada Job existente
        keywords_dict, words_found = verify_steps_words(j, jobs, keywords_dict) # Testa os passos do job
        if (words_found > 0):
             return(keywords_dict, words_found) # Retorna o dicionário e o número de palavras encontradas                       
    return(keywords_dict, words_found)

