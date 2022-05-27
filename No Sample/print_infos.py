## Função que verifica se deve printar ou não os resultados
def my_print(string_param, verbose):
    if(verbose):
        print(string_param)
    return()

# Função que printa informações
def print_information(verbose, store_infos_dict, runs_time_dict):
    my_print("Porcentagem de sucesso: {0} %".format(store_infos_dict["perc_sucess"]), verbose)       
    my_print("Porcentagem de Execuções relacionadas a Branch Main {0} %  /  Porcentagem ligada a Ramificações {1} %".format(store_infos_dict["perc_branch_main"], store_infos_dict["perc_branch_outros"]), verbose)
    my_print("Média (Tempo de Execução): {0}  /  Desvio Padrão (Tempo de Execução): {1}".format(store_infos_dict["runs_mean_time"], store_infos_dict["runs_sd_time"]), verbose)
    my_print("Média (Tempo entre runs): {0}  /  Desvio Padrão (Tempo entre runs): {1}".format(store_infos_dict["runs_mean_time_between_executions"], store_infos_dict["runs_sd_time_between_executions"]), verbose)
    my_print("Média de jobs no Pipeline: {0}".format(store_infos_dict["mean_jobs"]), verbose)
    my_print("Desvio padrão de jobs no Pipeline: {0}".format(store_infos_dict["sd_jobs"]), verbose)
    my_print("Número de runs: {0}".format(store_infos_dict["n_runs"]), verbose)
    my_print("Número de runs analisadas: {0}".format(store_infos_dict["n_runs_analyses"]), verbose)
    for chave, valor in runs_time_dict.items():
        my_print("Porcentagem de execuções em {0}: {1}".format(chave, valor), verbose)
    return()