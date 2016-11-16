import json
import requests
from requests.auth import HTTPBasicAuth

class ExampleData:

    def __init__(self):

        self.repo_data = []

        with open("../data collection/dev/dev_repos_names.txt", 'r') as file:
            repos = file.readlines()

        header = {'X-Github-Username': 'FlatErik90', 'X-Github-API-Token': "36dc9f6e45d8019dafe001adf05c433f22e6782e"}

        for repo in repos:
            r = requests.get("https://api.github.com/repos/"+repo[:-1],auth=HTTPBasicAuth('FlatErik90','bvb90EF'))
            print "https://api.github.com/repos/"+repo, r.status_code, r.json()
            if r.status_code == 200:
                self.repo_data.append((r.json(), 'DEV'))
                with open("../data collection/dev/repos/"+repo[:-1].split('/')[1]+".json",'w') as file:
                    jsonContent = str(r.json())
                    file.write(jsonContent)
                    file.close()


        print self.repo_data

ExampleData()