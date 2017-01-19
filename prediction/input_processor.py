import glob
import json
import os
import sys
sys.path.append('..')
import requests
from requests.auth import HTTPBasicAuth

from config.helper import Helper
from config.reader import ConfigReader

JSON_REPO_FILE_NAME = "%s_%s.json"
JSON_COMMITS_FILE_NAME = "%s_%s.json"
JSON_CONTENTS_FILE_NAME = "%s_%s.json"
JSON_COMMITS_INTERVAL_FILE_NAME = "%s_%s.json"
MD_README_FILE_NAME = "%s_%s.md"


class InputProcessor:
    def __init__(self):
        reader = ConfigReader()
        self.username, self.password = reader.get_credentials()

        self.repos_folder = 'json_repos/'
        self.readmes_folder = 'json_readmes/'
        self.contents_folder = 'json_contents/'
        self.commits_folder = 'json_commits/'
        self.commits_interval_folder = 'json_commits_interval/'

        self.updated_repos_folder = 'json_repos_updated/'

        self.RESULTS_PER_PAGE = 30

    def urls_to_repo_names(self, filename):
        repo_names_filename = filename.replace('urls', 'names')
        file_repos_names = open(repo_names_filename, 'w')
        try:
            with open(filename, 'r') as file:
                input_urls = file.readlines()
        except IOError:
            print 'File %s should exist in the current folder.' % filename
            return

        for url in input_urls:
            split = url.split("/")
            file_repos_names.write(split[3] + "/" + split[4])

    def names_to_json_repos(self, filename):
        folder = self.repos_folder
        try:
            with open(filename, 'r') as file:
                input_names = file.readlines()
        except IOError:
            print 'File %s should exist in the current folder.' % filename
            return

        for repo_name in input_names:
            repo_name = repo_name.replace('\n', '')
            repo_name = repo_name.replace('\r', '')
            print 'Fetching json repo object for %s ' % repo_name
            request_url = "https://api.github.com/repos/" + repo_name
            r = requests.get(request_url,
                             auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                filename = Helper().build_path_from_folder_and_repo_name(repo_name, folder, JSON_REPO_FILE_NAME)
                if not os.path.exists(os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))
                with open(filename, 'w') as file:
                    print "Writing to %s \n" % file.name
                    jsonContent = json.dumps((r.json()))
                    file.write(jsonContent)
                    file.close()
            else:
                print r.headers

    def names_to_readmes(self, filename):
        folder = self.readmes_folder
        try:
            with open(filename, 'r') as file:
                input_names = file.readlines()
        except IOError:
            print 'File %s should exist in the current folder.' % filename
            return

        for repo_name in input_names:
            repo_name = repo_name.replace('\n', '')
            repo_name = repo_name.replace('\r', '')
            print 'Fetching readme file contents for %s ' % repo_name
            request_url = "https://api.github.com/repos/" + repo_name + '/readme'
            r = requests.get(request_url,
                             auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                filename = Helper().build_path_from_folder_and_repo_name(repo_name, folder, MD_README_FILE_NAME)
                if not os.path.exists(os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))
                with open(filename, 'w') as file:
                    print "Writing to %s\n" % file.name
                    content = r.json()['content']
                    decoded = content.decode('base64')
                    file.write(decoded)
                    file.close()
            else:
                print r.headers

    def names_to_contents(self, filename):
        folder = self.contents_folder
        try:
            with open(filename, 'r') as file:
                input_names = file.readlines()
        except IOError:
            print 'File %s should exist in the current folder.' % filename
            return

        for repo_name in input_names:
            repo_name = repo_name.replace('\n', '')
            repo_name = repo_name.replace('\r', '')
            print 'Fetching readme file contents for %s ' % repo_name
            request_url = "https://api.github.com/repos/" + repo_name + '/contents'
            r = requests.get(request_url,
                             auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                filename = Helper().build_path_from_folder_and_repo_name(repo_name, folder, JSON_CONTENTS_FILE_NAME)
                if not os.path.exists(os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))
                with open(filename, 'w') as file:
                    print "Writing to %s \n" % file.name
                    contents = json.dumps((r.json()))
                    file.write(contents)
                    file.close()
            else:
                print r.headers

    def names_to_commits(self, filename):
        folder = self.commits_folder
        query = {'per_page': 100}

        try:
            with open(filename, 'r') as file:
                input_names = file.readlines()
        except IOError:
            print 'File %s should exist in the current folder.' % filename
            return

        for repo_name in input_names:
            repo_name = repo_name.replace('\n', '')
            repo_name = repo_name.replace('\r', '')
            print 'Fetching all commits for %s ' % repo_name
            request_url = "https://api.github.com/repos/" + repo_name + '/commits'

            filename = Helper().build_path_from_folder_and_repo_name(repo_name, folder, JSON_COMMITS_FILE_NAME)

            if os.path.exists(filename):
                print filename, " exists"
                continue

            r = requests.get(request_url, params=query,
                             auth=HTTPBasicAuth(self.username, self.password))

            if r.status_code == 200:
                print "status code: ", r.status_code

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
                    print "Writing %d commits to %s\n" % (jsonCommitsList.__len__(), file.name)
                    jsonContent = json.dumps(jsonCommitsList)
                    file.write(jsonContent)
                    file.close()
            else:
                print r.headers

    def names_to_commits_interval(self, filename):
        folder = self.commits_interval_folder

        try:
            with open(filename, 'r') as file:
                input_names = file.readlines()
        except IOError:
            print 'File %s should exist in the current folder.' % filename
            return

        for repo_name in input_names:
            repo_name = repo_name.replace('\n', '')
            repo_name = repo_name.replace('\r', '')

            print 'Fetching commits interval information for %s ' % repo_name
            request_url = "https://api.github.com/repos/" + repo_name + '/commits'

            filename = Helper().build_path_from_folder_and_repo_name(repo_name, folder, JSON_COMMITS_FILE_NAME)

            if os.path.exists(filename):
                print filename, " exists"
                continue

            r = requests.get(request_url,
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
                last_page_json_object = None
                if last_page != -1:
                    req = requests.get(last_page_url, auth=HTTPBasicAuth(self.username, self.password))
                    if req.status_code == 200:
                        last_page_json_object = req.json()
                        last_commit = last_page_json_object[len(last_page_json_object) - 1]
                    else:
                        print 'Page request failed'

                if last_page_json_object is not None:
                    count = len(last_page_json_object)
                else:
                    count = 0

                if last_page != -1:
                    # multiply by results per page
                    count += (last_page - 1) * 30

                if not os.path.exists(os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))

                json_interval_object = {"commits_count": count}
                json_interval_object['first_commit'] = first_commit
                json_interval_object['last_commit'] = last_commit

                with open(filename, 'w') as file:
                    print "Writing commits interval and count %d to %s\n" % (count, file.name)
                    jsonContent = json.dumps(json_interval_object)
                    file.write(jsonContent)
                    file.close()
            else:
                print r.headers

    def contents_to_file_trees(self):
        source_folder = self.contents_folder
        for filename in glob.glob(source_folder + '*'):
            print filename
            f = open(filename, 'r')
            contents = json.load(f)
            f.close()

            new_filename = filename.replace("json_contents", "json_trees")
            if os.path.exists(new_filename):
                print '%s new_filename tree already exists' % new_filename
                continue
            entries_trees = []

            for entry in contents:
                entry_type = entry['type']
                entry_size = entry['size']
                entry_name = entry['name']

                if entry_type == 'dir':
                    print 'Fetching tree for %s folder' % entry_name
                    entry_url = entry['git_url']
                    r = requests.get(entry_url + "?recursive=1", auth=HTTPBasicAuth(self.username, self.password))
                    if r.status_code == 200:
                        entry_tree = r.json()

                        entry_tree['root_folder_name'] = entry_name

                        entries_trees.append(entry_tree)

                    else:
                        print r.status_code

            if not os.path.exists(os.path.dirname(new_filename)):
                os.makedirs(os.path.dirname(new_filename))
            with open(new_filename, 'w') as file:
                print "Writing to %s" % file.name
                file.write(json.dumps(entries_trees))
                file.close()

    def update_repos(self, url_key, count_key):
        source_folder = self.repos_folder

        for filename in glob.glob(source_folder + '*'):
            print filename
            f = open(filename, 'r')
            repoObject = json.load(f)
            f.close()

            new_filename = filename.replace("json_repos", "json_repos_updated")

            if os.path.exists(new_filename):
                updated_repo_file = open(new_filename, 'r')
            else:
                updated_repo_file = open(filename, 'r')

            updated_repo_object = json.load(updated_repo_file)
            url = repoObject[url_key]
            if '{' in url:
                url = url.split('{')[0]
            print url
            r = requests.get(url, auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                if 'last' not in r.links:
                    jsonObject = r.json()
                    last_page = -1
                else:
                    print r.links
                    last_page_url = r.links['last']['url']
                    last_page = (int)(last_page_url.split('=')[1])
                    print last_page

                if last_page != -1:
                    req = requests.get(last_page_url, auth=HTTPBasicAuth(self.username, self.password))
                    if req.status_code == 200:
                        jsonObject = req.json()
                    else:
                        print 'Page request failed'

                count = len(jsonObject)
                if last_page != -1:
                    count += (last_page - 1) * self.RESULTS_PER_PAGE

                updated_repo_object[count_key] = count
                try:
                    del updated_repo_object[url_key]
                except KeyError:
                    print 'nothing to delete. move along'

                if not os.path.exists(os.path.dirname(new_filename)):
                    os.makedirs(os.path.dirname(new_filename))

                with open(new_filename, 'w') as file:
                    print "Writing to %s" % file.name
                    file.write(json.dumps(updated_repo_object))
                    file.close()
            else:
                print r.status_code

    def update_repos_with_languages(self):
        source_folder = self.repos_folder

        for filename in glob.glob(source_folder + '*'):
            print "Fetching languages for %s" % filename

            f = open(filename, 'r')
            updated_folder_filename = filename.replace("json_repos", "json_repos_updated")
            updated_folder_file = open(updated_folder_filename, 'r')

            # unarchived repo object, with all repo information
            repoObject = json.load(f)

            # already updated repo object, with missing urls
            updatedRepoObject = json.load(updated_folder_file)

            f.close()
            updated_folder_file.close()

            if 'languages' in updatedRepoObject:
                print 'exists'
                continue

            languages_url = repoObject["languages_url"]
            print languages_url
            r = requests.get(languages_url, auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                languages_object = r.json()

                if len(languages_object) == updatedRepoObject["languages_count"]:
                    print "yay!"
                # new_filename = filename.replace("repos", "updated_repos")
                updatedRepoObject["languages"] = languages_object
                new_filename = updated_folder_filename
                if not os.path.exists(os.path.dirname(new_filename)):
                    os.makedirs(os.path.dirname(new_filename))
                with open(new_filename, 'w') as file:
                    print "Writing to %s" % file.name
                    file.write(json.dumps(updatedRepoObject))
                    file.close()
            else:
                print r


if __name__ == '__main__':

    input_processor = InputProcessor()

    # inputProcessor.urls_to_repo_names(filename='input_urls.txt')
    # inputProcessor.names_to_json_repos(filename='input_names.txt')
    # inputProcessor.names_to_readmes(filename='input_names.txt')
    # inputProcessor.names_to_commits(filename='input_names.txt')
    # inputProcessor.names_to_commits_interval(filename='input_names.txt')
    # inputProcessor.names_to_contents(filename='input_names.txt')

    # input_processor.contents_to_file_trees()

    input_processor.update_repos('commits_url', 'commits_count')
    input_processor.update_repos('comments_url', 'comments_count')
    input_processor.update_repos('languages_url', 'languages_count')
    input_processor.update_repos('labels_url', 'labels_count')
    input_processor.update_repos('tags_url', 'tags_count')
    input_processor.update_repos('issues_url', 'issues_count')
    input_processor.update_repos('branches_url', 'branches_count')

    input_processor.update_repos_with_languages()
