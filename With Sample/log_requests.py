# Dicíonario para contar o número de requests em cada função no Log
import logging
requests_dict_count = {"build_jobs_path":0, "runs_path":0, "count_jobs_runs":0, "runs_sucess_path":0, "define_workflow_path":0} # Dicionário para contar quantidade de requests

def create_log(requests_dict_count, name):
    name = name + "_request"
    logging.basicConfig(filename = "{}.log".format(name), level= logging.INFO, format = "%(levelname)s:%(message)s", filemode = "w") # Configurando logging
    for item, valor in requests_dict_count.items():
        logging.info("Quantidade de requests vindo de {0}:{1}".format(item, valor))
    return()