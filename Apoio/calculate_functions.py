import requests
import print_functions as prt
import jobs_functions as jbs
import runs_functions as runsf

# Recupera informações se uma run foi acionada relacionada branch main
def count_branch_ativation(i, runs, branch_main_ativation):
    branch = runs[i].get("head_branch")
    if (branch == "main"):
       branch_main_ativation += 1
    return(branch_main_ativation) 

# Calcula porcentagem de sucesso
def calculate_perc(sucess, n, failed, branch_main_ativation, runs_time_dict):
    perc_sucess = sucess/(n-failed) *100 # Calcula porcentagem média de sucesso
    perc_branch_main = branch_main_ativation/n *100 # Calcula a porcentagem de runs relacionadas a branch main
    perc_branch_outros = (n-branch_main_ativation)/n *100 # Calcula a porcentagem de runs relacionadas a outras branchs
    for chave, valor in runs_time_dict.items(): # Loop para deixar os resultados em forma de porcentagem
        perc_data = valor/n *100
        runs_time_dict[chave] = "{0} %".format(round(perc_data, 2))
    return (perc_sucess, perc_branch_main, perc_branch_outros, runs_time_dict)

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
    runs_time_dict = {} # Dicionário para salvar o mês em que cada run foi executada
    runs_diff_time = [] # Lista do tempo de execuções entre as runs
    sucess, failed, branch_main_ativation = 0, 0, 0
    if (n_runs < n): # Ignora o caso de Pipelines que não são utilizados, mas estão no actions do repo   
        for i in range(0, n_runs): # Faz o loop das funções para o máximo de runs dísponível, mesmo que menor que n
            sucess, failed = runsf.count_runs_sucess(i, runs, sucess, failed)
            branch_main_ativation = count_branch_ativation(i, runs, branch_main_ativation)
            jbs.count_jobs_runs(i, runs, n_jobs_list, username, token, full_repo_path)
            runs_time_dict = runsf.calculate_runs_data_freq(runs, i, runs_time_dict)
            if (i+1 < n_runs): # Seu loop tem que ser até i-1
                runs_diff_time = runsf.calculate_runs_time_between_executions(runs, i, runs_diff_time)
        if(n_runs > n_runs_sucess): # Verifica se temos o número de runs com sucesso suficiente
            for i in range(0, n_runs_sucess): # Faz o loop de cálculo do tempo médio, para o total de runs sucesso disponível
                runs_time_list = runsf.calculate_runs_time(runs_sucess, i, runs_time_list)
        else:
            for i in range(0, n_runs): 
                runs_time_list = runsf.calculate_runs_time(runs_sucess, i, runs_time_list)
        n_runs_analyses = n_runs             
        perc_sucess, perc_branch_main, perc_branch_outros, runs_time_dict = calculate_perc(sucess, n_runs, failed, branch_main_ativation, runs_time_dict)
        prt.my_print("Só é possível calcular as estastísticas para {0} runs".format(n_runs), verbose)          
    else:   
        for i in range(0, n):
            sucess, failed = runsf.count_runs_sucess(i, runs, sucess, failed)
            branch_main_ativation = count_branch_ativation(i, runs, branch_main_ativation)
            jbs.count_jobs_runs(i, runs, n_jobs_list, username, token, full_repo_path)
            runs_time_dict = runsf.calculate_runs_data_freq(runs, i, runs_time_dict)
            if (i+1 < n): # Seu loop tem que ser até i-1
                runs_diff_time = runsf.calculate_runs_time_between_executions(runs, i, runs_diff_time)
        if (n > n_runs_sucess): # Verifica se temos o número de runs com sucesso suficiente
            for i in range(0, n_runs_sucess): # Faz o loop de cálculo do tempo médio, para o total de runs sucesso disponível
                runs_time_list = runsf.calculate_runs_time(runs_sucess, i, runs_time_list)
        else:
            for i in range(0, n):
                runs_time_list = runsf.calculate_runs_time(runs_sucess, i, runs_time_list)
        n_runs_analyses = n        
        perc_sucess, perc_branch_main, perc_branch_outros, runs_time_dict = calculate_perc(sucess, n, failed, branch_main_ativation, runs_time_dict)
    prt.print_information(perc_sucess, perc_branch_main, perc_branch_outros, runs_time_list, n_jobs_list, n_runs, verbose, n_runs_analyses, runs_time_dict, runs_diff_time)
    return(perc_sucess, perc_branch_main, perc_branch_outros, runs_time_list, n_jobs_list, n_runs, n_runs_analyses, runs_time_dict, runs_diff_time)
    