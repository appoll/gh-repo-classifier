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
JSON_PUNCH_CARD_ACTIVITY_FILE_NAME = "%s_%s.json"
JSON_COMMITS_FILE_NAME = "%s_%s.json"
MD_README_FILE_NAME = "%s_%s.md"
JSON_LANGUAGES_FILE_NAME = "%s_%s.json"
JSON_CONTENTS_FILE_NAME = "%s_%s.json"
JSON_COMMITS_INTERVAL = "%s_%s.json"


class ExampleData:
    def __init__(self):
        reader = ConfigReader()
        self.username, self.password = reader.get_credentials()
        self.token = reader.get_oauth_token()
        self.repos_folder = "../collection/%s/json_repos/"
        self.readmes_repos_folder = "../collection/%s/json_readmes/"
        self.contents_repos_folder = "../collection/%s/json_contents/"
        self.commit_activity_repos_folder = "../collection/%s/json_commit_activity/"
        self.punch_card_repos_folder = "../collection/%s/json_punch_card/"
        self.commits_repos_folder = "../collection/%s/json_commits/"
        self.commits_interval_folder = "../collection/%s/json_commits_interval/"
        self.repos_names_search = "../collection/%s/%s_repos_names_%s.txt"

        self.additional_repos_names = "../exploration/additional/%s.txt"
        self.additional_commits_repos_folder = "../exploration/additional/json_commits_%s/"
        self.additional_repos_folder = "../exploration/additional/json_repos_%s/"

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
            filename = Helper().build_path_from_folder_and_repo_name(repo, folder, MD_README_FILE_NAME)
            if os.path.exists(filename):
                print 'exists'
                continue

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
            print repos.__len__()
        for repo in repos:
            filename = Helper().build_path_from_folder_and_repo_name(repo, folder, JSON_COMMIT_ACTIVITY_FILE_NAME)

            if os.path.exists(filename):
                print filename, " exists"
                continue

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

    def getPunchCard(self, label, keyword):
        names = self.repos_names_search % (label, label, keyword)
        folder = self.punch_card_repos_folder % label
        with open(names, 'r') as file:
            repos = file.readlines()
            print repos.__len__()
        for repo in repos:
            filename = Helper().build_path_from_folder_and_repo_name(repo, folder, JSON_PUNCH_CARD_ACTIVITY_FILE_NAME)

            if os.path.exists(filename):
                print filename, " exists"
                continue

            r = requests.get("https://api.github.com/repos/" + repo[:-1] + "/stats/punch_card",
                             auth=HTTPBasicAuth(self.username, self.password))

            if r.status_code == 202:
                while r.status_code == 202:
                    print "status code: ", r.status_code
                    r = requests.get("https://api.github.com/repos/" + repo[:-1] + "/stats/punch_card",
                                     auth=HTTPBasicAuth(self.username, self.password))
                    time.sleep(3)

            if r.status_code == 200:
                print "status code: ", r.status_code
                filename = Helper().build_path_from_folder_and_repo_name(repo, folder, JSON_PUNCH_CARD_ACTIVITY_FILE_NAME)

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

    def get_all_commits(self, label, keyword):
        names = self.repos_names_search % (label, label, keyword)
        folder = self.commits_repos_folder % label
        query = {'per_page': 100}

        with open(names, 'r') as file:
            repos = file.readlines()
            print repos.__len__()
        for repo in repos:
            filename = Helper().build_path_from_folder_and_repo_name(repo, folder, JSON_COMMITS_FILE_NAME)

            if os.path.exists(filename):
                print filename, " exists"
                continue
            r = requests.get("https://api.github.com/repos/" + repo[:-1] + "/commits", params=query,
                             auth=HTTPBasicAuth(self.username, self.password))

            if r.status_code == 200:
                print "status code: ", r.status_code
                filename = Helper().build_path_from_folder_and_repo_name(repo, folder, JSON_COMMITS_FILE_NAME)

                if not os.path.exists(os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))

                jsonCommits = r.json()
                links = r.links
                print "commits loaded:", len(jsonCommits)
                while 'next' in links:
                    next_page_url = links['next']['url']
                    next_page_request = requests.get(next_page_url, auth=HTTPBasicAuth(self.username, self.password))

                    if next_page_request.status_code == 200:
                        jsonCommits.extend(next_page_request.json())
                        links = next_page_request.links
                    print "commits loaded:", len(jsonCommits)

                jsonCommitsList = []
                for commit in jsonCommits:
                    author = commit['commit']['author']
                    committer = commit['commit']['author']
                    comment_count = commit['commit']['comment_count']

                    author_date = author['date']
                    committer_date = committer['date']
                    author_email = author['email']
                    committer_email = committer['email']

                    commit_date = {'author_date': author_date, 'committer_date': committer_date,
                                   'comment_count': comment_count, 'author_email': author_email,
                                   'committer_email': committer_email}
                    jsonCommitsList.append(commit_date)

                with open(filename, 'w') as file:
                    print "Writing %d commits to %s" % (jsonCommitsList.__len__(), file.name)
                    jsonContent = json.dumps(jsonCommitsList)
                    file.write(jsonContent)
                    file.close()



            else:
                print r.headers

        print 'Successfully loaded commits for %d repos' % len(repos)

    def get_commits_interval(self, label, keyword):
        names = self.repos_names_search % (label, label, keyword)
        folder = self.commits_interval_folder % label

        with open(names, 'r') as file:
            repos = file.readlines()
            print repos.__len__()
        for repo in repos:
            filename = Helper().build_path_from_folder_and_repo_name(repo, folder, JSON_COMMITS_INTERVAL)

            if os.path.exists(filename):
                print filename, " exists"
                continue
            r = requests.get("https://api.github.com/repos/" + repo[:-1] + "/commits",
                             auth=HTTPBasicAuth(self.username, self.password))

            if r.status_code == 200:
                if 'last' not in r.links:
                    only_page_json_object = r.json()
                    first_commit = only_page_json_object[0]
                    last_commit = only_page_json_object[len(only_page_json_object) - 1]
                    last_page = -1
                else:
                    print r.links
                    first_page_json_object = r.json()
                    first_commit = first_page_json_object[0]
                    last_page_url = r.links['last']['url']
                    last_page = (int)(last_page_url.split('=')[1])
                    print last_page

                if last_page != -1:
                    req = requests.get(last_page_url, auth=HTTPBasicAuth(self.username, self.password))
                    if req.status_code == 200:
                        last_page_json_object = req.json()
                        last_commit = last_page_json_object[len(last_page_json_object) - 1]
                    else:
                        print 'Page request failed'

                count = len(last_page_json_object)
                if last_page != -1:
                    # multiply by results per page
                    count += (last_page - 1) * 30

                if not os.path.exists(os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))

                json_interval_object = {"commits_count": count}
                json_interval_object['first_commit'] = first_commit
                json_interval_object['last_commit'] = last_commit

                with open(filename, 'w') as file:
                    print "Writing commits interval and count %d to %s" % (count, file.name)
                    jsonContent = json.dumps(json_interval_object)
                    file.write(jsonContent)
                    file.close()
            else:
                print r.headers

        print 'Successfully loaded commits for %d repos' % len(repos)

    def get_contents(self, label, keyword):
        names = self.repos_names_search % (label, label, keyword)
        folder = self.contents_repos_folder % label

        with open(names, 'r') as file:
            repos = file.readlines()
        for repo in repos:
            filename = Helper().build_path_from_folder_and_repo_name(repo, folder, JSON_CONTENTS_FILE_NAME)
            if os.path.exists(filename):
                print filename, " exists"
                continue

            r = requests.get("https://api.github.com/repos/" + repo[:-1] + "/contents",
                             auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:

                if not os.path.exists(os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))
                with open(filename, 'w') as file:
                    print "Writing to %s" % file.name
                    contents = json.dumps((r.json()))
                    file.write(contents)
                    file.close()
            else:
                print r.headers

    def get_all_commits_additional_data(self, label):
        names = self.additional_repos_names % label
        folder = self.additional_commits_repos_folder % label
        query = {'per_page': 100}

        with open(names, 'r') as file:
            repos = file.readlines()
            print repos.__len__()
        for repo in repos:

            filename = Helper().build_path_from_folder_and_repo_link(repo, folder, JSON_COMMITS_FILE_NAME)

            if os.path.exists(filename):
                print filename, " exists"
                continue

            repo_name = Helper().build_repo_name_from_repo_link(repo)
            print repo_name
            r = requests.get("https://api.github.com/repos/" + repo_name + "/commits", params=query,
                             auth=HTTPBasicAuth(self.username, self.password))

            if r.status_code == 200:
                print "status code: ", r.status_code
                filename = Helper().build_path_from_folder_and_repo_link(repo, folder, JSON_COMMITS_FILE_NAME)

                if not os.path.exists(os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))

                jsonCommits = r.json()
                links = r.links
                print "commits loaded:", len(jsonCommits)
                while 'next' in links:
                    next_page_url = links['next']['url']
                    next_page_request = requests.get(next_page_url, auth=HTTPBasicAuth(self.username, self.password))

                    if next_page_request.status_code == 200:
                        jsonCommits.extend(next_page_request.json())
                        links = next_page_request.links
                    print "commits loaded:", len(jsonCommits)

                jsonCommitsList = []
                for commit in jsonCommits:
                    author = commit['commit']['author']
                    committer = commit['commit']['author']
                    comment_count = commit['commit']['comment_count']

                    author_date = author['date']
                    committer_date = committer['date']
                    author_email = author['email']
                    committer_email = committer['email']

                    commit_date = {'author_date': author_date, 'committer_date': committer_date,
                                   'comment_count': comment_count, 'author_email': author_email,
                                   'committer_email': committer_email}
                    jsonCommitsList.append(commit_date)

                with open(filename, 'w') as file:
                    print "Writing %d commits to %s" % (jsonCommitsList.__len__(), file.name)
                    jsonContent = json.dumps(jsonCommitsList)
                    file.write(jsonContent)
                    file.close()



            else:
                print r.headers

        print 'Successfully loaded commits for %d repos' % len(repos)

    def get_repos_additional_data(self, label):
        names = self.additional_repos_names % label
        folder = self.additional_repos_folder % label

        with open(names, 'r') as file:
            repos = file.readlines()

        for repo in repos:
            repo_name = Helper().build_repo_name_from_repo_link(repo)
            r = requests.get("https://api.github.com/repos/" + repo_name,
                             auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                filename = Helper().build_path_from_folder_and_repo_link(repo, folder, JSON_REPO_FILE_NAME)
                if not os.path.exists(os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))
                with open(filename, 'w') as file:
                    print "Writing to %s" % file.name
                    jsonContent = json.dumps((r.json()))
                    file.write(jsonContent)
                    file.close()
            else:
                print r.headers


data = ExampleData()

# data.getReadmes(label=Labels.edu)
# data.getReadmes(label=Labels.hw)
# data.getReadmes(label=Labels.docs)
# data.getReadmes(label=Labels.data)
# data.getReadmes(label=Labels.dev)
# data.getReadmes(label=Labels.web)

# data.getCommitActivity(label=Labels.edu)
# data.getCommitActivity(label=Labels.hw)
# data.getCommitActivity(label=Labels.docs)
# data.getCommitActivity(label=Labels.data)
# data.getCommitActivity(label=Labels.dev)
# data.getCommitActivity(label=Labels.web)

# calls below will append to existing files so uncomment carefully

# data.get_repo_names_by_keyword(label=Labels.hw,keyword="homework")

# data.get_repo_names_by_keyword(label=Labels.docs, keyword="docs")
# data.get_repo_names_by_keyword(label=Labels.docs, keyword="documentation")

# data.get_repo_names_by_keyword(label=Labels.data, keyword="data")

# data.get_repo_names_by_keyword('edu', keyword="course")

# data.get_repo_names_by_keyword(label=Labels.dev, keyword="framework")

# data.get_repo_names_by_keyword(label=Labels.web, keyword="github.io")

# keywords must be the same as the previously called get_repo_names_by_keyword methods

# data.get_repos_by_keyword(label='hw', keyword="homework")
# data.getReadmes(label='hw', keyword="homework")
# data.getCommitActivity(label='hw', keyword="homework")

# data.get_repos_by_keyword(label='data',keyword='dataset')
# data.getReadmes(label='data', keyword='dataset')
# data.getCommitActivity(label='data', keyword="dataset")

# data.get_repos_by_keyword(label='dev',keyword='framework')
# data.getReadmes(label='dev',keyword='framework')
# data.getCommitActivity(label='dev', keyword="framework")

# data.get_commits_interval(label='web', keyword='github.io')
# data.get_commits_interval(label='hw', keyword='homework')
# data.get_commits_interval(label='edu', keyword='course')
data.get_commits_interval(label='data', keyword='dataset')
# data.get_commits_interval(label='dev', keyword='framework')
# data.get_commits_interval(label='docs', keyword='docs')


# data.getCommitActivity(label='docs', keyword="docs")
# data.getCommitActivity(label='edux', keyword="course")

# data.get_last_100_commits(label='edu', keyword='course')
# data.get_last_100_commits(label='dev', keyword='framework')

# data.get_all_commits(label='docs', keyword='docs')

# completed 1000
# data.get_all_commits(label='hw', keyword='homework')
# data.get_all_commits(label='edu', keyword='course')
data.get_all_commits(label='data', keyword='dataset')
# data.get_all_commits(label='web', keyword='github.io')
# data.get_all_commits(label='dev', keyword='framework')




# data.get_all_commits_additional_data(label='docs')
# data.get_all_commits_additional_data(label='dev')
# data.get_all_commits_additional_data(label='data')
# data.get_all_commits_additional_data(label='edu')
# data.get_all_commits_additional_data(label='hw')
# data.get_all_commits_additional_data(label='other')
# data.get_all_commits_additional_data(label='web')

# data.get_repos_additional_data(label='docs')
# data.get_repos_additional_data(label='dev')
# data.get_repos_additional_data(label='data')
# data.get_repos_additional_data(label='edu')
# data.get_repos_additional_data(label='hw')
# data.get_repos_additional_data(label='other')
# data.get_repos_additional_data(label='web')
# #
#
# # data.get_contents(label='hw', keyword='homework')
# data.get_contents(label='edu', keyword='course')
data.get_contents(label='data', keyword='dataset')
# data.get_contents(label='web', keyword='github.io')
# data.get_contents(label='dev', keyword='framework')
# data.get_contents(label='docs', keyword="docs")


# data.getPunchCard(label='web', keyword='github.io')
# data.getPunchCard(label='hw', keyword='homework')
# data.getPunchCard(label='edu', keyword='course')
# data.getPunchCard(label='data', keyword='data')
# data.getPunchCard(label='dev', keyword='framework')
# data.getPunchCard(label='docs', keyword='docs')