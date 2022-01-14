import json
from datetime import datetime, timedelta

json_data = """{'apache/lucene': [{'n_worfklows': 3}, 
{'Workflow_Name': 'Gradle Precommit Checks', 'State': 'active', 'Created_at': '2021-03-10T07:34:27.000-03:00', 'Updated_at': '2021-10-12T10:07:17.000-03:00', 'Dev_time': '216 days 2:32:50', 'Success_rate': '55.0 %', 'Branch_Main_rate': '5.0 %', 'Other_Branchs_rate': '95.0 %', 'Mean(Execution time)': '0:08:46', 'Std_deviation(Execution time)': '0:01:03', 'Jobs_mean': '2', 'Total_runs': 1976}, 
{'Workflow_Name': 'Validate Gradle Wrapper', 'State': 'active', 'Created_at': '2021-03-10T06:51:30.000-03:00', 'Updated_at': '2021-03-10T06:51:30.000-03:00', 'Dev_time': '0:00:00', 'Success_rate': '100.0 %', 'Branch_Main_rate': '0.0 %', 'Other_Branchs_rate': '100.0 %', 'Mean(Execution time)': '0:01:05', 'Std_deviation(Execution time)': '0:00:42', 'Jobs_mean': '1', 'Total_runs': 6}, 
{'Workflow_Name': 'Hunspell regression tests', 'State': 'active', 'Created_at': '2021-03-10T12:01:06.000-03:00', 'Updated_at': '2021-03-10T12:01:06.000-03:00', 'Dev_time': '0:00:00', 'Success_rate': '84.21 %', 'Branch_Main_rate': '0.0 %', 'Other_Branchs_rate': '100.0 %', 'Mean(Execution time)': '0:04:59', 'Std_deviation(Execution time)': '0:00:29', 'Jobs_mean': '1', 'Total_runs': 210}
]
}"""
teste = json_data.replace("'", '"')
#print(teste)
def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True

isValid = validateJSON(teste)
#print("Given JSON string is Valid", isValid)
## Comando de checagem python -m json.tool DataJson.json
run_time_start = "2021-12-22T15:03:35Z"
run_start_date = datetime(year = int(run_time_start[0:4]), month = int(run_time_start[5:7]), day = int(run_time_start[8:10]))
print(run_start_date)
teste1 = {run_time_start[0:7]:1}
#if (run_time_start[0:7] in teste1):
#    teste1[run_time_start[0:7]] += 1
#else:
#    teste1[run_time_start[0:7]] = 1

#for chave, valor in teste1.items():
#   teste1[chave] = valor/n * 100

# for chave, valor in teste1.items():
#    my_print("Porcentagem de execuções em {0}: {1} %".format(chave, valor), verbose)

#regulagem = {'max': 10, 'meio': 5, 'min': 0}
#extra = {'passo': 2}

# Junção de dicionários com **
#juncao_dicio = {**regulagem, **extra}    
#print(juncao_dicio)