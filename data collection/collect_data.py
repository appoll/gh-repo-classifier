import json
import os

import requests
from requests.auth import HTTPBasicAuth

from config.reader import ConfigReader
from labels import Labels


class ExampleData:
    def __init__(self):
        self.username, self.password = ConfigReader().getCredentials()
        self.repos_names = "../data collection/%s/%s_repos_names.txt"
        self.repos_folder = "../data collection/%s/repos/"

    def get(self, label):
        names = self.repos_names % (label, label)
        folder = self.repos_folder % label

        with open(names, 'r') as file:
            repos = file.readlines()

        for repo in repos:
            r = requests.get("https://api.github.com/repos/" + repo[:-1], auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                filename = folder + repo[:-1].split('/')[1] + ".json"
                if not os.path.exists(os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))
                with open(filename, 'w') as file:
                    print "Writing to %s" % file.name
                    jsonContent = json.dumps((r.json()))
                    file.write(jsonContent)
                    file.close()


data = ExampleData()
data.get(label=Labels.hw)
