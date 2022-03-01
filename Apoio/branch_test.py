import json
from datetime import datetime, timedelta
import requests
import get_runs_info as runsf
from unidecode import unidecode
#json_data = """{'apache/lucene': [{'n_worfklows': 3}, 
#{'Workflow_Name': 'Gradle Precommit Checks', 'State': 'active', 'Created_at': '2021-03-10T07:34:27.000-03:00', 'Updated_at': '2021-10-12T10:07:17.000-03:00', 'Dev_time': '216 days 2:32:50', 'Success_rate': '55.0 %', 'Branch_Main_rate': '5.0 %', 'Other_Branchs_rate': '95.0 %', 'Mean(Execution time)': '0:08:46', 'Std_deviation(Execution time)': '0:01:03', 'Jobs_mean': '2', 'Total_runs': 1976}, 
#{'Workflow_Name': 'Validate Gradle Wrapper', 'State': 'active', 'Created_at': '2021-03-10T06:51:30.000-03:00', 'Updated_at': '2021-03-10T06:51:30.000-03:00', 'Dev_time': '0:00:00', 'Success_rate': '100.0 %', 'Branch_Main_rate': '0.0 %', 'Other_Branchs_rate': '100.0 %', 'Mean(Execution time)': '0:01:05', 'Std_deviation(Execution time)': '0:00:42', 'Jobs_mean': '1', 'Total_runs': 6}, 
#{'Workflow_Name': 'Hunspell regression tests', 'State': 'active', 'Created_at': '2021-03-10T12:01:06.000-03:00', 'Updated_at': '2021-03-10T12:01:06.000-03:00', 'Dev_time': '0:00:00', 'Success_rate': '84.21 %', 'Branch_Main_rate': '0.0 %', 'Other_Branchs_rate': '100.0 %', 'Mean(Execution time)': '0:04:59', 'Std_deviation(Execution time)': '0:00:29', 'Jobs_mean': '1', 'Total_runs': 210}
#]
#}"""
#teste = json_data.replace("'", '"')
#print(teste)
#def validateJSON(jsonData):
#    try:
#        json.loads(jsonData)
#    except ValueError as err:
#        return False
#    return True

#isValid = validateJSON(teste)
#print("Given JSON string is Valid", isValid)
## Comando de checagem python -m json.tool DataJson.json
#run_time_start = "2021-12-22T15:03:35Z"
#run_start_date = datetime(year = int(run_time_start[0:4]), month = int(run_time_start[5:7]), day = int(run_time_start[8:10]))
#print(run_start_date)
#teste1 = {run_time_start[0:7]:1}
#if (run_time_start[0:7] in teste1):
#    teste1[run_time_start[0:7]] += 1
#else:
#    teste1[run_time_start[0:7]] = 1
# keywords_dict = {"test":0}

# def chr_remove(old, to_remove):
#     new_string = old
#     for x in to_remove:
#         new_string = new_string.replace(x, '')
#     return new_string

# path = "https://api.github.com/repos/apache/lucene/actions/workflows/6563726/runs"
# res_runs = requests.get(path, auth= (username, token)) # Fazendo request
# json_runs = res_runs.json() # Transformando em json
# n_runs = json_runs["total_count"] # Recupera o número de runs
# runs = json_runs["workflow_runs"] # Informação das runs
# id_jobs = runs[0].get("id")
# condition = runs[0].get("conclusion")
# if (condition != "action_required"):
#     path_jobs = "https://api.github.com/repos/apache/lucene" + "/actions/runs/{0}/jobs".format(id_jobs)
#     res_jobs = requests.get(path_jobs, auth= (username, token)) 
#     jobs_json = res_jobs.json()
#     n_jobs = int(jobs_json["total_count"])
#     jobs = jobs_json["jobs"]
#     steps = jobs[0].get("steps")
#     print(steps[0].get("name"))
#     for j in range(n_jobs):
#         job_name = jobs[j].get("name")
#         job_name = chr_remove(job_name, "!@#$%¨&*()_-=+'?:<>,.\|^~`}{][;")
#         job_name = unidecode(job_name)
#         lista_palavras = job_name.split()
#         for palavra in lista_palavras:
#             if (palavra in keywords_dict):
#                 keywords_dict[palavra] += 1
# print(keywords_dict)