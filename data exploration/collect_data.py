import json
import requests
from requests.auth import HTTPBasicAuth

def dump_repo_data(class_name):

        with open("../data collection/"+class_name+"/"+class_name+"_repos_names.txt", 'r') as file:
            repos = file.readlines()

        for repo in repos:
            r = requests.get("https://api.github.com/repos/"+repo[:-1],auth=('FlatErik90','bvb90EF'))
            print "https://api.github.com/repos/"+repo, r.status_code
            if r.status_code == 200:
                with open("../data collection/"+class_name+"/repos/"+repo[:-1].split('/')[1]+".json",'w') as file:
                    jsonContent = json.dumps(r.json())
                    file.write(jsonContent)
                    file.close()

dump_repo_data("data")