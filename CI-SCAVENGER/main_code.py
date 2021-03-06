## Import libraries
import sys, getopt
import get_workflow_infos as work
import calculate_stats as calc
import build_json as js
import verify_pipeline as pipeline
from log_requests import requests_dict_count, create_log
import build_csv as csv

def main(argv):
    ## Define inputs
    username = None # Username git hub
    token = None # Validation Token
    owner = None # Repo Owner
    repo = None # Repo name
    n = None # Runs amount to analyze 
    name = None # Output name
    output = None # Output format
    sampling = None # To sample or not
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "u:t:o:r:n:j:e:s:")
    except:
        print("Error")
    for opt, arg in opts:
        if opt in ['-u']:
            username = str(arg)
        elif opt in ['-t']:
            token = str(arg)
        elif opt in ['-o']:
            owner = str(arg)    
        elif opt in ['-r']:
            repo = str(arg)
        elif opt in ['-n']:
            n = int(arg)
        elif opt in ['-j']:
            name = str(arg)
        elif opt in ['-e']:
            output = str(arg)
        elif opt in ['-s']:
            sampling = str(arg)        
    # Execução das funções
    repo_path, full_repo_path, request_path, workflows, n_pipelines = work.define_workflow_path(username, token, owner, repo)
    json_data = {repo_path:[]}
    for i in range(0, n_pipelines): ## Loop for each pipeline
        validate_worflow = pipeline.investigate_workflow_ci_cd(i, n, workflows, request_path, username, token, full_repo_path) # Validate CI/CD workflow
        if (validate_worflow): # If confirm CI/CD, Execute functions and calculate statistics
            store_infos_dict, runs_time_dict = calc.calculate_workflows_stats(i, n, workflows, username, token, request_path, full_repo_path, sampling)
            if (store_infos_dict): # Verify if the workflow is not empty
                store_infos_dict = work.workflow_name_state(i, workflows, store_infos_dict)
                store_infos_dict = work.calculate_development_time(i, workflows, store_infos_dict)
                workflow_json = js.format_file(store_infos_dict, runs_time_dict)
                json_data[repo_path].append(workflow_json)  # Add dictionary with the data and stats
            else: # If empty descart
                continue
                      
    if (output == "json"):
        js.build_json_file(name, json_data) # Build .json
    else:
        csv.build_csv_file(name, json_data, repo_path) # Build .csv
    create_log(requests_dict_count, name) # Create log file
    
if __name__ == "__main__":
    main(sys.argv[1:])
    
