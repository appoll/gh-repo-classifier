import json
import os
import sys

import time

sys.path.append('..')

import requests
from requests.auth import HTTPBasicAuth

from config.helper import Helper
from config.reader import ConfigReader

JSON_REPO_FILE_NAME = "%s_%s.json"
JSON_COMMIT_ACTIVITY_FILE_NAME = "%s_%s.json"
MD_README_FILE_NAME = "%s_%s.md"


class ExampleData:
    def __init__(self):
        self.username, self.password = ConfigReader().getCredentials()
        self.repos_folder = "../collection/%s/json_repos/"
        self.readmes_repos_folder = "../collection/%s/json_readmes/"
        self.commit_activity_repos_folder = "../collection/%s/json_commit_activity/"
        self.repos_names_search = "../collection/%s/%s_repos_names_%s.txt"
        self.encoding = "base64",

    def get_repos_by_keyword(self, label, keyword):
        names = self.repos_names_search % (label, label, keyword)
        folder = self.repos_folder % label

        with open(names, 'r') as file:
            repos = file.readlines()

        for repo in repos:
            r = requests.get("https://api.github.com/repos/" + repo[:-1],
                             auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                filename = Helper().build_path_from_folder_and_repo_name(repo, folder, JSON_REPO_FILE_NAME)
                if not os.path.exists(os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))
                with open(filename, 'w') as file:
                    print "Writing to %s" % file.name
                    jsonContent = json.dumps((r.json()))
                    file.write(jsonContent)
                    file.close()
            else:
                print r.headers

    def getReadmes(self, label, keyword):
        names = self.repos_names_search % (label, label, keyword)
        folder = self.readmes_repos_folder % label

        with open(names, 'r') as file:
            repos = file.readlines()
        for repo in repos:
            r = requests.get("https://api.github.com/repos/" + repo[:-1] + "/readme",
                             auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                filename = Helper().build_path_from_folder_and_repo_name(repo, folder, MD_README_FILE_NAME)
                if not os.path.exists(os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))
                with open(filename, 'w') as file:
                    print "Writing to %s" % file.name
                    content = r.json()['content']
                    decoded = content.decode('base64')
                    file.write(decoded)
                    file.close()
            else:
                print r.headers

    def getCommitActivity(self, label, keyword):
        names = self.repos_names_search % (label, label, keyword)
        folder = self.commit_activity_repos_folder % label

        with open(names, 'r') as file:
            repos = file.readlines()
        for repo in repos:
            r = requests.get("https://api.github.com/repos/" + repo[:-1] + "/stats/commit_activity",
                             auth=HTTPBasicAuth(self.username, self.password))

            if r.status_code == 202:
                while r.status_code == 202:
                    print "status code: ", r.status_code
                    r = requests.get("https://api.github.com/repos/" + repo[:-1] + "/stats/commit_activity",
                                     auth=HTTPBasicAuth(self.username, self.password))
                    time.sleep(3)

            if r.status_code == 200:
                print "status code: ", r.status_code
                filename = Helper().build_path_from_folder_and_repo_name(repo, folder, JSON_COMMIT_ACTIVITY_FILE_NAME)

                if not os.path.exists(os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))
                with open(filename, 'w') as file:
                    print "Writing to %s" % file.name
                    jsonContent = json.dumps((r.json()))
                    file.write(jsonContent)
                    file.close()
            else:
                print r.headers

    def get_repo_names_by_keyword(self, label, keyword):
        query = {'q': keyword, 's': 'match', 'per_page': 100}
        r = requests.get("https://api.github.com/search/repositories", params=query,
                         auth=HTTPBasicAuth(self.username, self.password))
        print "status code: ", r.status_code
        if r.status_code == 200:

            repos = r.json()["items"]
            links = r.links

            print "repos loaded:", len(repos)
            while 'next' in links:
                next_page_url = links['next']['url']
                next_page_request = requests.get(next_page_url, auth=HTTPBasicAuth(self.username, self.password))

                if next_page_request.status_code == 200:
                    repos.extend(next_page_request.json()["items"])
                    links = next_page_request.links
                print "repos loaded:", len(repos)

            filename = self.repos_names_search % (label, label, keyword)
            with open(filename, 'a') as file:
                print "Writing to %s" % file.name
                for repo in repos:
                    repo_name = repo["full_name"]
                    # print repo_name
                    file.writelines(repo_name + "\n")
                file.close()


data = ExampleData()

# data.getReadmes(label=Labels.edu.value)
# data.getReadmes(label=Labels.hw.value)
# data.getReadmes(label=Labels.docs.value)
# data.getReadmes(label=Labels.data.value)
# data.getReadmes(label=Labels.dev.value)
# data.getReadmes(label=Labels.web.value)

# data.getCommitActivity(label=Labels.edu.value)
# data.getCommitActivity(label=Labels.hw.value)
# data.getCommitActivity(label=Labels.docs.value)
# data.getCommitActivity(label=Labels.data.value)
# data.getCommitActivity(label=Labels.dev.value)
# data.getCommitActivity(label=Labels.web.value)

# calls below will append to existing files so uncomment carefully

# data.get_repo_names_by_keyword(label=Labels.hw.value,keyword="homework")

# data.get_repo_names_by_keyword(label=Labels.docs.value, keyword="docs")
# data.get_repo_names_by_keyword(label=Labels.docs.value, keyword="documentation")

# data.get_repo_names_by_keyword(label=Labels.data.value, keyword="data")

# data.get_repo_names_by_keyword('edu', keyword="course")

# data.get_repo_names_by_keyword(label=Labels.dev.value, keyword="framework")

# data.get_repo_names_by_keyword(label=Labels.web.value, keyword="github.io")

# keywords must be the same as the previously called get_repo_names_by_keyword methods

# data.get_repos_by_keyword(label='hw', keyword="homework")
# data.getReadmes(label='hw', keyword="homework")
# data.getCommitActivity(label='hw', keyword="homework")

# data.get_repos_by_keyword(label='data',keyword='data')
# data.getReadmes(label='data', keyword='data')
# data.getCommitActivity(label='data', keyword="data")

# data.get_repos_by_keyword(label='dev',keyword='framework')
# data.getReadmes(label='dev',keyword='framework')
