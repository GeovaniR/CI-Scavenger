### Algoritmo para recuperar informações dos Pipelines dos repos
### Pip install requests - Instala biblioteca
### 1XX - Informação ; 2XX - Sucesso ; 3XX - Redirecionar ; 4XX - Erro do cliente ; 5XX - Erro do servidos
import requests
from datetime import datetime
import statistics

res_workflows = requests.get("https://api.github.com/repos/apache/lucene/actions/workflows")
json_w = res_workflows.json()
workflows = json_w["workflows"]
id = workflows[0].get("id")
path = 'https://api.github.com/repos/apache/lucene/actions/workflows/{0}/runs'.format(id)
res_runs = requests.get(path)
json_runs = res_runs.json()
n_runs = json_runs["total_count"]
runs = json_runs["workflow_runs"]
l_t = []
j = 0
block = 0
n = 20
id_jobs = runs[0].get("id")
print(id_jobs)
path_2 = 'https://api.github.com/repos/apache/lucene/actions/runs/{0}/jobs'.format(id_jobs)
res_jobs = requests.get(path_2) 
jobs = res_jobs.json()
print(int(jobs["total_count"]))