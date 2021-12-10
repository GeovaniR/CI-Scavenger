import json

teste = """{"apache/lucene": [{"n_worfklows": 3}, 
{"Workflow_Name": "Gradle Precommit Checks", "State": "active", "Created_at": "2021-03-10T07:34:27.000-03:00", "Updated_at": "2021-10-12T10:07:17.000-03:00", "Dev_time": "216 days 2:32:50", "Success_rate": "89.47 %", "Branch_Main_rate": "25.0 %", "Other_Branchs_rate": "75.0 %", "Mean(Execution time)": "0:08:48", "Std_deviation(Execution time)": "0:01:02", "Jobs_mean": "2", "Total_runs": 1858},
{"Workflow_Name": "Validate Gradle Wrapper", "State": "active", "Created_at": "2021-03-10T06:51:30.000-03:00", "Updated_at": "2021-03-10T06:51:30.000-03:00", "Dev_time": "0:00:00", "Success_rate": "100.0 %", "Branch_Main_rate": "0.0 %", "Other_Branchs_rate": "100.0 %", "Mean(Execution time)": "0:01:05", "Std_deviation(Execution time)": "0:00:42", "Jobs_mean": "1", "Total_runs": 6}, 
{"Workflow_Name": "Hunspell regression tests", "State": "active", "Created_at": "2021-03-10T12:01:06.000-03:00", "Updated_at": "2021-03-10T12:01:06.000-03:00", "Dev_time": "0:00:00", "Success_rate": "100.0 %", "Branch_Main_rate": "0.0 %", "Other_Branchs_rate": "100.0 %", "Mean(Execution time)": "0:05:06", "Std_deviation(Execution time)": "0:00:30", "Jobs_mean": "1", "Total_runs": 182}
]
}"""

def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True

isValid = validateJSON(teste)
print("Given JSON string is Valid", isValid)
