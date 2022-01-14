import statistics
from datetime import datetime, timedelta

## Função que verifica se deve printar ou não os resultados
def my_print(string_param, verbose):
    if(verbose):
        print(string_param)
    return()

# Função que printa informações
def print_information(perc_sucess, perc_branch_main, perc_branch_outros, runs_time_list, n_jobs_list, n_runs, verbose, n_runs_analyses, runs_time_dict):
    my_print("Porcentagem de sucesso: {:.2f} %".format(perc_sucess), verbose)       
    my_print("Porcentagem de Execuções relacionadas a Branch Main {:.2f} %  /  Porcentagem ligada a Ramificações {:.2f} %".format(perc_branch_main, perc_branch_outros), verbose)
    my_print("Média (Tempo de Execução): {0}  /  Desvio Padrão (Tempo de Execução): {1}".format(timedelta(seconds= int(statistics.mean(runs_time_list))), timedelta(seconds= int(statistics.stdev(runs_time_list)))), verbose)
    my_print("Média de jobs no Pipeline: {0}".format(statistics.mean(n_jobs_list)), verbose)
    my_print("Número de runs: {0}".format(n_runs), verbose)
    my_print("Número de runs analisadas: {0}".format(n_runs_analyses), verbose)
    for chave, valor in runs_time_dict.items():
        my_print("Porcentagem de execuções em {0}: {1}".format(chave, valor), verbose)
    return()
