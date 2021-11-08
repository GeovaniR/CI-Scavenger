### Algoritmo para recuperar informações dos Pipelines dos repos
### Pip install requests - Instala biblioteca

## Importando bibliotecas
import requests
from datetime import datetime, timedelta
import statistics

## Salva a lista de pipelines do repo e transformar em formato .json para análise, também recupera o número de pipelines do repo
res_workflows = requests.get("https://api.github.com/repos/apache/lucene/actions/workflows")
json_w = res_workflows.json()
n_pipelines = json_w["total_count"]
workflows = json_w["workflows"]
print("----------------------------------------------------------------------")
print("Número de worflows:",n_pipelines)

### Funções
## Recupera quando o pipeline foi criado e a ultima vez que foi atualizado, além de calcular a diferença entre essas datas
def tempo(i):
    t1 = workflows[i].get("created_at")
    t2 = workflows[i].get("updated_at")
    print("Data de Criação:",t1)
    print("Última atualização:",t2)
    t1_date = datetime(year = int(t1[0:4]), month = int(t1[5:7]), day = int(t1[8:10]), hour = int(t1[11:13]), minute = int(t1[14:16]), second = int(t1[17:19]))
    t2_date = datetime(year = int(t2[0:4]), month = int(t2[5:7]), day = int(t2[8:10]), hour = int(t2[11:13]), minute = int(t2[14:16]), second = int(t2[17:19]))
    diff_temp = t2_date - t1_date
    return (print("Tempo de Desenvolvimento do Workflow:", diff_temp))

# Recupera informações sobre o tempo que levou para ser executado uma das últimas runs do pipeline e adiciona numa lista
def tempo_run(i, runs, l_t):
    t1 = runs[i].get("created_at")
    t2 = runs[i].get("updated_at")
    t1_date = datetime(year = int(t1[0:4]), month = int(t1[5:7]), day = int(t1[8:10]), hour = int(t1[11:13]), minute = int(t1[14:16]), second = int(t1[17:19]))
    t2_date = datetime(year = int(t2[0:4]), month = int(t2[5:7]), day = int(t2[8:10]), hour = int(t2[11:13]), minute = int(t2[14:16]), second = int(t2[17:19]))
    diff_temp = t2_date - t1_date
    l_t.append(diff_temp.total_seconds())
    return (l_t)    

# Recupera informação se uma run foi sucesso ou não. Obs: Tira da contagem aquelas que não temos permissão
def eventos(i, runs, j, block):
    conclu = runs[i].get("conclusion")
    if (conclu == "success"):
        j += 1  
    elif (conclu != "action_required"):
        block = +1    
    return(j, block) 

# Recupera informações sobre o número de jobs nas runs do pipeline e adiciona numa lista
def n_jobs(i, runs, l_jobs):
    id_jobs = runs[i].get("id")
    path_2 = 'https://api.github.com/repos/apache/lucene/actions/runs/{0}/jobs'.format(id_jobs)
    res_jobs = requests.get(path_2) 
    jobs = res_jobs.json()
    q_jobs = int(jobs["total_count"])
    l_jobs.append(q_jobs)
    return (l_jobs)

# Recupera informações se uma reun foi acionada relacionada branch main
def head_branch(i, runs, a):
    branch = runs[i].get("head_branch")
    if (branch == "main"):
        a += 1
    return(a)        

# Função principal que chama as secundárias para calcular as informações
def workflow_runs(i,n): # n define quantos runs serão pegas
    id = workflows[i].get("id")
    path = 'https://api.github.com/repos/apache/lucene/actions/workflows/{0}/runs'.format(id)
    res_runs = requests.get(path)
    json_runs = res_runs.json()
    n_runs = json_runs["total_count"] # Recupera o número de runs
    runs = json_runs["workflow_runs"]
    l_t = []
    l_jobs = []
    j, block, a = 0, 0, 0
    if (n_runs < n): # Ignora o caso de Pipelines que não são utilizados, mas estão no actions do repo
        print("Não temos execuções suficientes para calcular estatísticas")
        return(print("Número de runs:", n_runs))
    else:    
        for i in range(0,n):
            tempo_run(i, runs, l_t)
            j, block = eventos(i, runs, j, block)
            a = head_branch(i, runs, a)
            n_jobs(i, runs, l_jobs)
    perc_suc = j/(n-block) *100 # Calcula porcentagem média de sucesso
    perc_main = a/n *100 # Calcula a porcentagem de runs relacionadas a branch main
    perc_outros = (n-a)/n *100 # Calcula a porcentagem de runs relacionadas a outras branchs
    print("Porcentagem de sucesso: {:.2f}%".format(perc_suc))       
    print("Porcentagem de Execuções relacionadas a Branch Main {:.2f} %  /  Porcentagem ligada a Ramificações {:.2f} %".format(perc_main, perc_outros))
    print("Média (Tempo de Execução): {0}  /  Desvio Padrão (Tempo de Execução): {1}".format(timedelta(seconds= int(statistics.mean(l_t))), timedelta(seconds= int(statistics.stdev(l_t)))))
    print("Média de jobs no Pipeline:{0}".format(statistics.mean(l_jobs)))
    return(print("Número de runs:", n_runs))
    
    
## Loop para que seja rodada as funções em cada pipeline
for i in range(0,n_pipelines):
    print("---------------------------------------------------------------------")
    print("Workflow Name:",workflows[i].get("name")) # Recupera o nome do Pipeline
    print("Estado do Workflow:", workflows[i].get("state")) # Recupera se o Pipeline está ativo
    tempo(i)
    workflow_runs(i, 20)
