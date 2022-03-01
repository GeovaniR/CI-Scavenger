import requests
import print_functions as prt
import jobs_functions as jbs
import runs_functions as runsf
import runs_sucess as run_sucess

# Recupera informações se uma run foi acionada relacionada a branch main
def count_branch_ativation(i, runs, branch_main_ativation): # Função que conta a quantidade de runs que foram ativadas pela branch main
    branch = runs[i].get("head_branch") # recupera qual branch ativou a run
    if (branch == "main"): # Testa se foi a branch main
       branch_main_ativation += 1
    return(branch_main_ativation) 

# Calcula porcentagem de sucesso
def calculate_perc(sucess, n_runs, private, branch_main_ativation, runs_time_dict):
    perc_sucess = sucess/(n_runs-private) *100 # Calcula porcentagem média de sucesso do workflow
    perc_branch_main = branch_main_ativation/n_runs *100 # Calcula a porcentagem de runs relacionadas a branch main
    perc_branch_outros = (n_runs-branch_main_ativation)/n_runs *100 # Calcula a porcentagem de runs relacionadas a outras branchs
    for chave, valor in runs_time_dict.items(): # Loop para deixar os resultados do mês de execução das runs em forma de porcentagem
        perc_data = valor/n_runs *100
        runs_time_dict[chave] = "{0} %".format(round(perc_data, 2)) # Deixa o resultado no formato string como porcentagem
    return (perc_sucess, perc_branch_main, perc_branch_outros, runs_time_dict)

# Função principal que chama as secundárias para calcular as informações
def calculate_workflows_stats(i, n, workflows, username, token, request_path, full_repo_path, verbose): # n define quantos runs serão pegas
    n_runs, runs = runsf.runs_path(i, n, workflows, request_path, username, token) # Recupera o número de runs no workflow e o texto json com as informações 
    n_runs_sucess, runs_sucess = run_sucess.runs_sucess_path(i, n, workflows, request_path, username, token) # Recupera o número de runs que foram sucesso entre as n últimas runs e o texto json com as informações
    runs_time_list = [] # Lista para salvar o tempo das últimas n runs
    n_jobs_list = [] # Lista para salvar o número de jobs nas últimas n runs
    runs_time_dict = {} # Dicionário para salvar o mês em que cada run foi executada
    runs_diff_time = [] # Lista do tempo de execuções entre as runs
    sucess, private, branch_main_ativation = 0, 0, 0
    if (n_runs < n): # Testa se o número de runs solicitado para análise é maior que o número de runs disponíel
        for i in range(0, n_runs): # Faz o loop das funções para o máximo de runs dísponível, mesmo que menor que n
            sucess, private = run_sucess.count_runs_sucess(i, runs, sucess, private)
            branch_main_ativation = count_branch_ativation(i, runs, branch_main_ativation)
            jbs.count_jobs_runs(i, runs, n_jobs_list, username, token, full_repo_path)
            runs_time_dict = runsf.calculate_runs_data_freq(runs, i, runs_time_dict)
            runs_diff_time = runsf.calculate_time_between_runs_execution(runs, i, runs_diff_time, n_runs)
        runs_time_list = runsf.loop_to_calculate_n_runs_execution_time(n_runs, n_runs_sucess, runs_sucess, runs_time_list)
        n_runs_analyses = n_runs  # Armazena que o número de runs análisadas é igual ao número total de runs disponível         
        perc_sucess, perc_branch_main, perc_branch_outros, runs_time_dict = calculate_perc(sucess, n_runs, private, branch_main_ativation, runs_time_dict)         
    else:   
        for i in range(0, n): # Faz o loop das funções para a quantidade de runs solicitadas
            sucess, private = run_sucess.count_runs_sucess(i, runs, sucess, private)
            branch_main_ativation = count_branch_ativation(i, runs, branch_main_ativation)
            jbs.count_jobs_runs(i, runs, n_jobs_list, username, token, full_repo_path)
            runs_time_dict = runsf.calculate_runs_data_freq(runs, i, runs_time_dict)
            runs_diff_time = runsf.calculate_time_between_runs_execution(runs, i, runs_diff_time, n)
        runs_time_list = runsf.loop_to_calculate_n_runs_execution_time(n, n_runs_sucess, runs_sucess, runs_time_list)
        n_runs_analyses = n  # Armazena que o número de runs análisadas é igual ao solicitado pelo usuário
        perc_sucess, perc_branch_main, perc_branch_outros, runs_time_dict = calculate_perc(sucess, n, private, branch_main_ativation, runs_time_dict)
    prt.print_information(perc_sucess, perc_branch_main, perc_branch_outros, runs_time_list, n_jobs_list, n_runs, verbose, n_runs_analyses, runs_time_dict, runs_diff_time)
    return(perc_sucess, perc_branch_main, perc_branch_outros, runs_time_list, n_jobs_list, n_runs, n_runs_analyses, runs_time_dict, runs_diff_time)
