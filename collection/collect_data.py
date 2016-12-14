import glob
import json
import os

import requests
from requests.auth import HTTPBasicAuth

from config.reader import ConfigReader
from labels import Labels


class ExampleData:
    def __init__(self):
        self.username, self.password = ConfigReader().getCredentials()
        self.repos_names = "../collection/%s/%s_repos_names.txt"
        self.repos_folder = "../collection/%s/repos/"
        self.readmes_repos_folder = "../collection/%s/readmes/"
        self.commit_activity_repos_folder = "../collection/%s/commit_activity/"
        self.repos_names_search = "../collection/%s/%s_repos_names_%s.txt"
        self.encoding = "base64",

    def get(self, label):
        names = self.repos_names % (label, label)
        folder = self.repos_folder % label

        with open(names, 'r') as file:
            repos = file.readlines()

        for repo in repos:
            r = requests.get("https://api.github.com/repos/" + repo[:-1],
                             auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                filename = folder + repo[:-1].split('/')[1] + ".json"
                if not os.path.exists(os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))
                with open(filename, 'w') as file:
                    print "Writing to %s" % file.name
                    jsonContent = json.dumps((r.json()))
                    file.write(jsonContent)
                    file.close()

    def getReadmes(self, label):
        names = self.repos_names % (label, label)
        folder = self.readmes_repos_folder % label

        with open(names, 'r') as file:
            repos = file.readlines()
        for repo in repos:
            r = requests.get("https://api.github.com/repos/" + repo[:-1] + "/readme",
                             auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                filename = folder + repo[:-1].split('/')[1] + ".md"
                if not os.path.exists(os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))
                with open(filename, 'w') as file:
                    print "Writing to %s" % file.name
                    content = r.json()['content']
                    decoded = content.decode('base64')
                    file.write(decoded)
                    file.close()


    def getCommitActivity(self, label):
        names = self.repos_names % (label, label)
        folder = self.commit_activity_repos_folder % label

        with open(names, 'r') as file:
            repos = file.readlines()
        for repo in repos:
            r = requests.get("https://api.github.com/repos/" + repo[:-1] + "/stats/commit_activity",
                             auth=HTTPBasicAuth(self.username, self.password))
            print "status code: ", r.status_code
            if r.status_code == 200:
                filename = folder + repo[:-1].split('/')[1] + ".json"
                if not os.path.exists(os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))
                with open(filename, 'w') as file:
                    print "Writing to %s" % file.name
                    jsonContent = json.dumps((r.json()))
                    file.write(jsonContent)
                    file.close()


    def get_repos_by_keyword(self, label, keyword):
        query = {'q': keyword, 's': 'match', 'per_page': 100}
        r = requests.get("https://api.github.com/search/repositories", params=query,
                         auth=HTTPBasicAuth(self.username, self.password))
        print "status code: ", r.status_code
        if r.status_code == 200:

            repos = r.json()["items"]
            links = r.links

            while 'next' in links:
                next_page_url = links['next']['url']
                next_page_request = requests.get(next_page_url, auth=HTTPBasicAuth(self.username, self.password))

                if next_page_request.status_code == 200:
                    repos.extend(next_page_request.json()["items"])
                    links = next_page_request.links

            filename = self.repos_names_search % (label, label, keyword)
            with open(filename, 'w') as file:
                print "Writing to %s" % file.name
                for repo in repos:
                    repo_name = repo["full_name"]
                    print repo_name
                    file.writelines(repo_name + "\n")
                file.close()


data = ExampleData()
#data.get(label=Labels.hw.value)

#data.getReadmes(label=Labels.edu.value)
# data.getReadmes(label=Labels.hw.value)
# data.getReadmes(label=Labels.docs.value)
# data.getReadmes(label=Labels.data.value)
# data.getReadmes(label=Labels.dev.value)
# data.getReadmes(label=Labels.web.value)

#data.getCommitActivity(label=Labels.edu.value)
#data.getCommitActivity(label=Labels.hw.value)
#data.getCommitActivity(label=Labels.docs.value)
#data.getCommitActivity(label=Labels.data.value)
#data.getCommitActivity(label=Labels.dev.value)
#data.getCommitActivity(label=Labels.web.value)

data.get_repos_by_keyword(label=Labels.hw.value,keyword="homework")