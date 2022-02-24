import requests
import runs_functions as runsf
from unidecode import unidecode
from Keywords_list import keywords_list

def investigate_workflow_keywords(i, n, workflows, request_path, username, token, full_repo_path):
    n_runs, runs = runsf.runs_path(i, n, workflows, request_path, username, token) # Runs é o arquivo json com os dados das runs e n_runs o número de runs no workflow
    word_found_status = verify_workflow_words(i, workflows, keywords_list) # Testa o nome do workflow
    if (word_found_status): # Testa se a palavra foi encontrada (word_found_status igual a True)
        return(True) # Caso tenha encontrado já retorna que o workflow pode ser testado
    else: # Caso contrário testa os jobs e steps
        word_found_status = verify_jobs_and_steps(0, runs, keywords_list, full_repo_path, username, token)
        if (word_found_status): # Testa se encontrou alguma palavra no nome do job e passos
            return(True) # Caso tenha encontrado já retorna que o workflow pode ser testado                  
    return(False) # Caso não tenha encontrado retorna false

def chr_remove(old, to_remove): # Função que remove caracteres especiais
    new_string = old.lower() # Transforma string para inteiramente minúsculo
    for x in to_remove: # Para cada caractere na lista dos que devem ser retirados
        new_string = new_string.replace(x, '') # substitui caractere especial por espaço vázio
    return new_string

def compare_word_with_dict(name, keywords_list): # Função que analisa a existência da palavra dentro do dicionário
    name = chr_remove(name, "!@#$%¨&*()_-=+'?:<>,.\|^~`}{][;") # Remove caracteres especiais
    name = unidecode(name) # Remove acentos
    lista_palavras = name.split() # lista com as palavras da frase
    for palavra in lista_palavras: # testa de palavra em palavra com o dicionário
        if (palavra in keywords_list): # Se uma palavra é encontrada já retorna True
            return(True)
    return(False) 

def verify_workflow_words(i, workflows, keywords_list): # Função que verifica se o nome do workflow da evidências de ser para CI/CD
    workflow_name = workflows[i].get("name") # Recupera o nome do workflow
    word_found_status = compare_word_with_dict(workflow_name, keywords_list) # Testa o nome do workflow
    return(word_found_status) # Retorna se a palavra foi encontrada(True) ou não(False)

def verify_jobs_words(j, jobs, keywords_list): # Função que verifica se o nome do Job da evidências de ser para CI/CD
    job_name = jobs[j].get("name") # Recupera o nome do Job
    word_found_status = compare_word_with_dict(job_name, keywords_list) # Testa o nome
    return(word_found_status) # Retorna se a palavra foi encontrada(True) ou não(False)

def verify_steps_words(j, jobs, keywords_list): # Função que verifica se os passos do Job fornecem evidências de CI/CD
    steps = jobs[j].get("steps") # Entra na lista de steps
    n_steps = len(steps) # recupera quantidade de steps
    for k in range(n_steps): # Laço que vai do primeiro step até o último
        step_name = steps[k].get("name") # Recupera o nome do Job
        word_found_status = compare_word_with_dict(step_name, keywords_list) # Testa o nome
        if (word_found_status): # Testa se a palavra foi encontrada (word_found_status igual a True)
            break 
    return(word_found_status) # Retorna se a palavra foi encontrada(True) ou não(False)

def build_jobs_path(i, runs, full_repo_path, username, token): # A função encontra a última run que tenha acesso aberto e faz o caminho para obter as informações
    condition = runs[i].get("conclusion")  # Obtém status da conclusão da última run para analisar se é fechado
    while (condition == "action_required"): # Loop até achar uma run sem acesso privado
        i += 1 # soma 1 para ir para run seguinte
        condition = runs[i].get("conclusion")   
    id_jobs = runs[i].get("id") # recupera id da run
    path_jobs = full_repo_path + "/actions/runs/{0}/jobs".format(id_jobs) # define caminho para os jobs da run
    res_jobs = requests.get(path_jobs, auth= (username, token)) # Executa chamada para informações dos jobs
    jobs_json = res_jobs.json() # Transformar informações para formato json
    n_jobs = int(jobs_json["total_count"]) # Recupera a quantidade total de jobs
    jobs = jobs_json["jobs"] # Entra nas informações sobre os jobs
    return(n_jobs, jobs)


def verify_jobs_and_steps(i, runs, keywords_list, full_repo_path, username, token): # i percore o número de runs
    n_jobs, jobs = build_jobs_path(i, runs, full_repo_path, username, token) # Obtém o número de jobs e as informações desses jobs
    for j in range(n_jobs): # Percore cada Job existente
        word_found_status = verify_jobs_words(j, jobs, keywords_list) # Testa o nome do job
        if (word_found_status): # Testa se a palavra foi encontrada (word_found_status igual a True)
            return(True) # Retorna que a palavra foi encontrada
    for j in range(n_jobs): # Percore cada Job existente
        word_found_status = verify_steps_words(j, jobs, keywords_list) # Testa os passos do job
        if (word_found_status): # Testa se a palavra foi encontrada (word_found_status igual a True)
             return(True) # Retorna que a palavra foi encontrada                     
    return(False) # Se chegar até aqui retorna que a palavra não foi encontrada

