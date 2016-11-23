import json


class ConfigReader:
    def __init__(self):
        github_auth_file = "../github-api-credentials.config"
        file = open(github_auth_file, 'r')
        self.credentials = json.load(file)

    def getCredentials(self):
        return self.credentials["username"], self.credentials["password"]