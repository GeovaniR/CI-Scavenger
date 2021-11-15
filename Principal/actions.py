### Algoritmo para recuperar informações dos Pipelines dos repos
### Pip install requests - Instala biblioteca

## Importando bibliotecas
import requests
from datetime import datetime, timedelta
import statistics

## Salva a lista de pipelines do repo e transformar em formato .json para análise, também recupera o número de pipelines do repo
username = input("Username:")
token = input("Token:")
owner = input("Repository Owner:")
repo = input("Repository Name:")
repo_path = owner + "/" + repo
pi_url = "https://api.github.com/repos/"
full_repo_path = pi_url + repo_path
request_path = full_repo_path + "/actions/workflows"
res_workflows = requests.get(request_path, auth= (username, token))
json_w = res_workflows.json()
n_pipelines = json_w["total_count"]
workflows = json_w["workflows"]
print("----------------------------------------------------------------------")
print("Número de worflows:",n_pipelines)

### Funções
## Recupera quando o pipeline foi criado e a ultima vez que foi atualizado, além de calcular a diferença entre essas datas *calculate_development_time*
def calculate_development_time(i):
    t1 = workflows[i].get("created_at")
    t2 = workflows[i].get("updated_at")
    print("Data de Criação:",t1)
    print("Última atualização:",t2)
    t1_date = datetime(year = int(t1[0:4]), month = int(t1[5:7]), day = int(t1[8:10]), hour = int(t1[11:13]), minute = int(t1[14:16]), second = int(t1[17:19]))
    t2_date = datetime(year = int(t2[0:4]), month = int(t2[5:7]), day = int(t2[8:10]), hour = int(t2[11:13]), minute = int(t2[14:16]), second = int(t2[17:19]))
    diff_temp = t2_date - t1_date
    return (print("Tempo de Desenvolvimento do Workflow:", diff_temp))

# Recupera informações sobre o tempo que levou para ser executado uma das últimas runs do pipeline e adiciona numa lista
def calculate_runs_time(t, runs, l_t, r):
    if (runs[t].get("conclusion") == "success"):
        t1 = runs[t].get("created_at")
        t2 = runs[t].get("updated_at")
        t1_date = datetime(year = int(t1[0:4]), month = int(t1[5:7]), day = int(t1[8:10]), hour = int(t1[11:13]), minute = int(t1[14:16]), second = int(t1[17:19]))
        t2_date = datetime(year = int(t2[0:4]), month = int(t2[5:7]), day = int(t2[8:10]), hour = int(t2[11:13]), minute = int(t2[14:16]), second = int(t2[17:19]))
        diff_temp = t2_date - t1_date
        l_t.append(diff_temp.total_seconds())
        t += 1
        r += 1
        return (l_t, t, r)
    else:
        t += 1
        return(l_t, t, r)    

# Recupera informação se uma run foi sucesso ou não. Obs: Tira da contagem aquelas que não temos permissão
def count_runs_sucess(i, runs, j, block):
    conclu = runs[i].get("conclusion")
    if (conclu == "success"):
        j += 1  
    elif (conclu != "action_required"):
        block = +1    
    return(j, block) 

# Recupera informações sobre o número de jobs nas runs do pipeline e adiciona numa lista
def count_jobs_runs(i, runs, l_jobs):
    id_jobs = runs[i].get("id")
    path_2 = full_repo_path + "/actions/runs/{0}/jobs".format(id_jobs)
    res_jobs = requests.get(path_2, auth= (username, token)) 
    jobs = res_jobs.json()
    q_jobs = int(jobs["total_count"])
    l_jobs.append(q_jobs)
    return (l_jobs)

# Recupera informações se uma run foi acionada relacionada branch main
def count_branch_ativation(i, runs, a):
    branch = runs[i].get("head_branch")
    if (branch == "main"):
        a += 1
    return(a)        

def print_information(perc_suc, perc_main, perc_outros, l_t, l_jobs, n_runs):
    print("Porcentagem de sucesso: {:.2f}%".format(perc_suc))       
    print("Porcentagem de Execuções relacionadas a Branch Main {:.2f} %  /  Porcentagem ligada a Ramificações {:.2f} %".format(perc_main, perc_outros))
    print("Média (Tempo de Execução): {0}  /  Desvio Padrão (Tempo de Execução): {1}".format(timedelta(seconds= int(statistics.mean(l_t))), timedelta(seconds= int(statistics.stdev(l_t)))))
    print("Média de jobs no Pipeline:{0}".format(statistics.mean(l_jobs)))
    print("Número de runs:", n_runs)
    return

def calculate_perc(j,n, block, a):
    perc_suc = j/(n-block) *100 # Calcula porcentagem média de sucesso
    perc_main = a/n *100 # Calcula a porcentagem de runs relacionadas a branch main
    perc_outros = (n-a)/n *100 # Calcula a porcentagem de runs relacionadas a outras branchs
    return (perc_suc, perc_main, perc_outros) 

# Função principal que chama as secundárias para calcular as informações
def calculate_runs(i,n): # n define quantos runs serão pegas
    id = workflows[i].get("id") # Recupera ID do pipeline
    path = request_path + "/{0}/runs".format(id)
    res_runs = requests.get(path, auth= (username, token))
    json_runs = res_runs.json()
    n_runs = json_runs["total_count"] # Recupera o número de runs
    runs = json_runs["workflow_runs"] # Informação das runs
    l_t = []
    l_jobs = []
    j, block, a = 0, 0, 0
    if (n_runs < n): # Ignora o caso de Pipelines que não são utilizados, mas estão no actions do repo
        print("Não temos execuções suficientes para calcular estatísticas")
        return(print("Número de runs:", n_runs))
    else:
        t = 0
        r = 0    
        for i in range(0,n):
            j, block = count_runs_sucess(i, runs, j, block)
            a = count_branch_ativation(i, runs, a)
            count_jobs_runs(i, runs, l_jobs)
        while(r < n):
            l_t, t, r = calculate_runs_time(t, runs, l_t, r)
    print(l_t)    
    perc_suc, perc_main, perc_outros = calculate_perc(j,n, block, a)
    return(print_information(perc_suc, perc_main, perc_outros, l_t, l_jobs, n_runs))
    
## Loop para que seja rodada as funções em cada pipeline
for i in range(0,n_pipelines):
    print("---------------------------------------------------------------------")
    print("Workflow Name:",workflows[i].get("name")) # Recupera o nome do Pipeline
    print("Estado do Workflow:", workflows[i].get("state")) # Recupera se o Pipeline está ativo
    calculate_development_time(i)
    calculate_runs(i, 20)
