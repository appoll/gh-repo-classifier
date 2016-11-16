import json
import requests


class ExampleData:

    def __init__(self):

        self.repo_data = []

        with open("dev_repos.txt", 'r') as file:
            repos = file.readlines()

        for repo in repos:
            r = requests.get("https://api.github.com/repos/"+repo)
            if r.status_code == 200:
                self.objects.append((r.json(), 'DEV'))



        print self.repo_data

ExampleData()