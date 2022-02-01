from datetime import datetime

# Recupera informações sobre o tempo que levou para ser executado uma das últimas runs do pipeline e adiciona numa lista
def calculate_runs_time(runs_sucess, i, runs_time_list):
    if(runs_sucess[i].get("run_attempt") == "1"): # Verifica se é a primeira execução daquela run
        run_time_start = runs_sucess[i].get("created_at") # Recupera quando a run começou
    else:
        run_time_start = runs_sucess[i].get("run_started_at") # Recupera quando a última execução da run começou
    rum_time_finish = runs_sucess[i].get("updated_at") # Recupera quando a run terminou
    run_start_date = datetime(year = int(run_time_start[0:4]), month = int(run_time_start[5:7]), day = int(run_time_start[8:10]), hour = int(run_time_start[11:13]), minute = int(run_time_start[14:16]), second = int(run_time_start[17:19]))
    run_finish_date = datetime(year = int(rum_time_finish[0:4]), month = int(rum_time_finish[5:7]), day = int(rum_time_finish[8:10]), hour = int(rum_time_finish[11:13]), minute = int(rum_time_finish[14:16]), second = int(rum_time_finish[17:19]))
    diff_temp = run_finish_date - run_start_date # Calcula o tempo
    runs_time_list.append(diff_temp.total_seconds()) # Adiciona numa lista
    return (runs_time_list)

def calculate_runs_data_freq(runs, i, runs_time_dict):
    run_time = runs[i].get("run_started_at") # Recupera quando a última execução da run começou
    if (run_time[0:7] in runs_time_dict):
        runs_time_dict[run_time[0:7]] += 1
    else:
        runs_time_dict[run_time[0:7]] = 1
    return(runs_time_dict)

def calculate_runs_time_between_executions(runs, i, runs_diff_time):
    run_time_start = runs[i].get("created_at") # Recupera quando a run começou
    rum_time_start_2 = runs[i+1].get("created_at") # Recupera quando a run anterior começou
    run_start = datetime(year = int(run_time_start[0:4]), month = int(run_time_start[5:7]), day = int(run_time_start[8:10]), hour = int(run_time_start[11:13]), minute = int(run_time_start[14:16]), second = int(run_time_start[17:19]))
    run_start_2 = datetime(year = int(rum_time_start_2[0:4]), month = int(rum_time_start_2[5:7]), day = int(rum_time_start_2[8:10]), hour = int(rum_time_start_2[11:13]), minute = int(rum_time_start_2[14:16]), second = int(rum_time_start_2[17:19]))
    diff_temp = run_start - run_start_2 # Calcula o tempo entre as execuções
    runs_diff_time.append(diff_temp.total_seconds()) # Adiciona numa lista
    return(runs_diff_time)    


# Recupera informação se uma run foi sucesso ou não. Obs: Tira da contagem aquelas que não temos permissão
def count_runs_sucess(i, runs, sucess, failed):
    conclusion = runs[i].get("conclusion")
    if (conclusion == "success"):
        sucess += 1  
    elif (conclusion == "action_required"):
        failed += 1    
    return(sucess, failed)