import requests
from datetime import datetime, timedelta
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
def eventos(i, runs, j, block):
    conclu = runs[i].get("conclusion")
    print(conclu)
    if (conclu == "success"):
        j += 1  
    elif (conclu != "action_required"):
        block = +1    
    return(j, block)    

def tempo_run(i, runs, l_t):
    t1 = runs[i].get("created_at")
    t2 = runs[i].get("updated_at")
    t1_date = datetime(year = int(t1[0:4]), month = int(t1[5:7]), day = int(t1[8:10]), hour = int(t1[11:13]), minute = int(t1[14:16]), second = int(t1[17:19]))
    t2_date = datetime(year = int(t2[0:4]), month = int(t2[5:7]), day = int(t2[8:10]), hour = int(t2[11:13]), minute = int(t2[14:16]), second = int(t2[17:19]))
    diff_temp = t2_date - t1_date
    l_t.append(diff_temp.total_seconds())
    return (l_t)

def n_jobs(i, runs):
    id_jobs = runs[i].get("id")
    path_2 = 'https://api.github.com/repos/apache/lucene/actions/runs/{0}/jobs'.format(id_jobs)
    res_jobs = requests.get(path_2) 
    jobs = res_jobs.json()
    print(jobs["total_count"])

for i in range(0,20):
    tempo_run(i, runs, l_t)
    j, block = eventos(i, runs, j, block)

print("Execuções com Sucesso:", j) 
print("Execuções bloqueadas:", block)
perc_suc = j/(n-block) *100
print("Porcentagem de sucesso: {:.2f}%".format(perc_suc))
print("Média (Tempo de Execução):", timedelta(seconds= int(statistics.mean(l_t))))
print("Desvio Padrão (Tempo de Execução):", timedelta(seconds= int(statistics.stdev(l_t))))
print("Número de runs:", n_runs)