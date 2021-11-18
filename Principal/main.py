## Importando bibliotecas
import requests
from datetime import datetime, timedelta
import statistics
from actions import define_path
from actions import calculate_development_time
from actions import calculate_runs
from actions import workflow_name_state

def main():
    username = input("Username:") # Entrada Username git hub
    token = input("Token:") # Entrada do token de validação
    owner = input("Repository Owner:") # Entrada do nome do Dono do repo
    repo = input("Repository Name:") # Entrada do nome do repo
    ## Define os caminhos, cálcula o número de pipelines e salva as informçaões dos workflow em um json
    full_repo_path, request_path, workflows, n_pipelines = define_path(username, token, owner, repo)
    ## Loop para que seja rodada as funções em cada pipeline
    for i in range(0,n_pipelines):
        workflow_name_state(i)
        calculate_development_time(i)
        calculate_runs(i, 20)
main()
