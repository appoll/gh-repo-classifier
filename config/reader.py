import json


class ConfigReader:
    def __init__(self):
        github_credentials_file = "../github-api-credentials.config"
        github_oauth_token_file = "../github-api-OAuth.config"
        file = open(github_credentials_file, 'r')
        self.credentials = json.load(file)
        file = open(github_oauth_token_file, 'r')
        self.oauth = json.load(file)

    def get_credentials(self):
        return self.credentials["username"], self.credentials["password"]

    def get_oauth_token(self):
        return self.oauth["token"]