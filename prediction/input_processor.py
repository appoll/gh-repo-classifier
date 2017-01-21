import glob
import json
import os
import sys

sys.path.append('..')
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, time
import dateutil.parser
import math
import numpy as np
import collections
from config.helper import Helper
from config.reader import ConfigReader
from collection.labels import Labels

JSON_REPO_FILE_NAME = "%s_%s.json"
JSON_COMMITS_FILE_NAME = "%s_%s.json"
JSON_CONTENTS_FILE_NAME = "%s_%s.json"
JSON_COMMITS_INTERVAL_FILE_NAME = "%s_%s.json"
JSON_PUNCH_CARD_FILE_NAME = "%s_%s.json"
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
        self.punch_card_folder = "json_punch_card/"

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

    def names_to_punchcard(self, filename):
        folder = self.punch_card_folder
        try:
            with open(filename, 'r') as file:
                input_names = file.readlines()
        except IOError:
            print 'File %s should exist in the current folder.' % filename
            return

        for repo_name in input_names:
            repo_name = repo_name.replace('\n', '')
            repo_name = repo_name.replace('\r', '')

            filename = Helper().build_path_from_folder_and_repo_name(repo_name, folder, JSON_PUNCH_CARD_FILE_NAME)
            if os.path.exists(filename):
                print filename, " exists"
                continue
            print 'Fetching punch card information for %s ' % repo_name

            request_url = "https://api.github.com/repos/" + repo_name + '/stats/punch_card'

            r = requests.get(request_url,
                             auth=HTTPBasicAuth(self.username, self.password))

            if r.status_code == 202:
                while r.status_code == 202:
                    print "status code: ", r.status_code
                    r = requests.get(request_url,
                                     auth=HTTPBasicAuth(self.username, self.password))
                    time.sleep(3)

            if r.status_code == 200:
                print "status code: ", r.status_code
                filename = Helper().build_path_from_folder_and_repo_name(repo_name, folder,
                                                                         JSON_PUNCH_CARD_FILE_NAME)

                if not os.path.exists(os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))
                with open(filename, 'w') as file:
                    print "Writing to %s" % file.name
                    jsonContent = json.dumps((r.json()))
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


class FeatureExtractor:
    def __init__(self):
        self.readmes_folder = 'json_readmes/'
        self.contents_folder = 'json_contents/'
        self.commits_folder = 'json_commits/'
        self.commits_interval_folder = 'json_commits_interval/'
        self.trees_folder = "json_trees/"
        self.punch_card_folder = "json_punch_card/"

        self.updated_repos_folder = 'json_repos_updated/'

        self.features_folder = "features/"

        self.all_languages = {}

    def get_commits_interval_features(self):
        folder = self.commits_interval_folder
        name = self.features_folder + "commits_interval_data.txt"

        if not os.path.exists(os.path.dirname(name)):
            os.makedirs(os.path.dirname(name))
        f = open(name, 'w')
        header = "commits_count commits_interval_days commits_per_day repo_name\n"
        f.write(header)
        for filename in glob.glob(folder + '*'):
            print filename
            json_file = open(filename, 'r')
            name = os.path.basename(filename)
            commits_interval = json.load(json_file)
            json_file.close()

            all_commits_count = commits_interval['commits_count']
            first_commit = commits_interval['first_commit']
            last_commit = commits_interval['last_commit']
            commits_interval_days = self.get_commits_interval(last_commit, first_commit)
            commits_per_day = self.get_commits_per_day(last_commit, first_commit, all_commits_count)

            line = "%.2f" % all_commits_count
            line = line + " " + "%.2f" % commits_interval_days
            line = line + " " + "%.2f" % commits_per_day

            line = line + " " + name.split('.')[0]

            f.write(line)
            f.write('\n')
        print "Wrote commits interval features to %s" % f.name
        f.close()

    def get_punchcard_features(self):
        folder = self.punch_card_folder
        name = self.features_folder + "punch_card_data.txt"
        if not os.path.exists(os.path.dirname(name)):
            os.makedirs(os.path.dirname(name))
        f = open(name, 'w')
        header = ""
        weekdays = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
        for day in weekdays:
            for i in range(24):
                header += day + str(i) + " "
        header += "repo_name\n"
        f.write(header)
        for filename in glob.glob(folder + '*'):
            print filename
            json_file = open(filename, 'r')
            name = os.path.basename(filename)
            punch_card_info = json.load(json_file)
            json_file.close()

            punch_card_info = np.array(punch_card_info)
            punch_card_info = punch_card_info[:, 2]
            commit_sum = float(np.sum(punch_card_info))
            punch_card_info = map(lambda x: x / commit_sum, punch_card_info)

            line = ' '.join(map(str, punch_card_info)) + " " + name.split('.')[0]

            f.write(line)
            f.write('\n')
        print "Wrote punch card features to %s" % f.name
        f.close()

    def get_commits_features(self):
        folder = self.commits_folder
        name = self.features_folder + "commit_data.txt"

        if not os.path.exists(os.path.dirname(name)):
            os.makedirs(os.path.dirname(name))
        f = open(name, 'w')
        header = "all_commits weekend_commits weekday_commits work_hrs_commits non_work_hrs_commits inter_commit_distance_average commits_per_day_average authors_count author_vs_committer active_days repo_name\n"
        f.write(header)

        for filename in glob.glob(folder + '*'):
            print filename
            json_file = open(filename, 'r')
            name = os.path.basename(filename)
            commits_list = json.load(json_file)
            json_file.close()

            all_commits_count = len(commits_list)
            weekend_commits_count = 0
            weekday_commits_count = 0
            work_hrs_commits_count = 0
            non_work_hrs_commits_count = 0

            inter_commit_distance = 0
            prev_date = 0

            print 'Processing %s commits...' % len(commits_list)
            for commit in commits_list:
                author_date = dateutil.parser.parse(commit['author_date'])

                if datetime.isoweekday(author_date) in range(6, 8):
                    weekend_commits_count += 1
                else:
                    weekday_commits_count += 1

                if author_date.hour in range(9, 19):
                    work_hrs_commits_count += 1
                else:
                    non_work_hrs_commits_count += 1

                if prev_date != 0:
                    distance = prev_date - author_date
                    hours = distance.total_seconds() / 3600
                    inter_commit_distance += hours
                prev_date = author_date

            if all_commits_count > 1:
                first_commit = commits_list[all_commits_count - 1]
                last_commit = commits_list[0]
                commits_per_day = self.get_commits_per_day(first_commit, last_commit, all_commits_count)
            else:
                commits_per_day = 1

            line = "%.2f" % all_commits_count
            line = line + " " + "%.2f" % (float(weekend_commits_count) / all_commits_count)
            line = line + " " + "%.2f" % (float(weekday_commits_count) / all_commits_count)
            line = line + " " + "%.2f" % (float(work_hrs_commits_count) / all_commits_count)
            line = line + " " + "%.2f" % (float(non_work_hrs_commits_count) / all_commits_count)

            line = line + " " + "%.2f" % (
                self.get_inter_commit_distance_average(inter_commit_distance, all_commits_count))
            line = line + " " + "%.2f" % commits_per_day
            line = line + " " + "%.2f" % (self.get_unique_authors(commits_list))
            line = line + " " + "%.2f" % (self.get_authors_vs_committers(commits_list))
            line = line + " " + "%.2f" % (self.get_active_days(commits_list))

            line = line + " " + name.split('.')[0]

            f.write(line)
            f.write('\n')
        print "Wrote commits features to %s" % f.name
        f.close()

    def get_language_features(self, binary):

        folder = self.updated_repos_folder
        name = self.features_folder + "languages_data.txt"

        if len(self.all_languages.keys()) == 0:
            print 'Initialize all languages dict'
            self.all_languages = self.get_all_languages()

        if not os.path.exists(os.path.dirname(name)):
            os.makedirs(os.path.dirname(name))
        f = open(name, 'w')
        header = "languages_count languages_total_lines "
        for language in self.all_languages:
            language = language.replace(" ", "_")
            header += language + " "

        header += "repo_name\n"
        f.write(header)

        for filename in glob.glob(folder + '*'):
            print filename
            # print len(self.all_languages)
            current_languages = self.all_languages.fromkeys(self.all_languages, 0)
            json_file = open(filename, 'r')
            name = os.path.basename(filename)
            repo = json.load(json_file)

            try:
                languages = repo["languages"]
                repo_size = repo['size']
            except KeyError:
                print "Key Error in %s" % filename
                continue

            all_languages_count = len(languages)
            total_lines = sum(languages.itervalues())

            #            if repo_size == 0:
            #                continue

            for language, code_lines in languages.iteritems():
                # print language
                if language not in current_languages:
                    raise ValueError("Should not be!")
                try:
                    if binary == True:
                        current_languages[language] = 1
                    else:
                        current_languages[language] = "%.2f" % (float(code_lines) / total_lines)
                except ZeroDivisionError:
                    current_languages[language] = 0
                    # raise ZeroDivisionError("Somewhere you missed a check on total_bytes!")

            # print len(current_languages)

            line = "%.2f" % all_languages_count
            line = line + " " + "%.2f" % total_lines
            for code_lines in current_languages.values():
                line = line + " " + str(code_lines)

            line = line + " " + name.split('.')[0]

            f.write(line)
            f.write('\n')
        print "Wrote languages features to %s" % f.name
        f.close()

    def get_repo_features(self):
        folder = self.updated_repos_folder
        name = self.features_folder + "repo_data.txt"

        if not os.path.exists(folder):
            raise Exception("Folder should exist!")

        if not os.path.exists(os.path.dirname(name)):
            os.makedirs(os.path.dirname(name))
        f = open(name, 'w')
        header = "size labels tags issues branches languages forks commits comments repo_name\n"
        f.write(header)

        for filename in glob.glob(folder + '*'):
            print filename
            json_file = open(filename, 'r')
            name = os.path.basename(filename)
            repo = json.load(json_file)
            json_file.close()

            try:
                # size in KB
                size = repo['size']
                labels = repo['labels_count']
                # contributors = repo['contributors_count']
                tags = repo['tags_count']
                issues = repo['issues_count']
                branches = repo['branches_count']
                languages = repo['languages_count']
                forks = repo['forks']
                commits = repo['commits_count']
                comments = repo['comments_count']
            except KeyError:
                print 'KeyError, not considering repo'
                continue

            if size == 0:
                print 'Not considering empty repos'
                continue

            line = "%d" % size
            line = line + " " + "%d" % labels
            # line = line + " " + "%d" % contributors
            line = line + " " + "%d" % tags
            line = line + " " + "%d" % issues
            line = line + " " + "%d" % branches
            line = line + " " + "%d" % languages
            line = line + " " + "%d" % forks
            line = line + " " + "%d" % commits
            line = line + " " + "%d" % comments

            line = line + " " + name.split('.')[0]

            f.write(line)
            f.write('\n')
        print "Wrote repo features to %s" % f.name
        f.close()

    def get_contents_features(self):
        folder = self.contents_folder
        name = self.features_folder + "contents_data.txt"

        if not os.path.exists(os.path.dirname(name)):
            os.makedirs(os.path.dirname(name))
        f = open(name, 'w')
        header = "total dirs files folder_names file_names fo_and_fi_names repo_name\n"
        f.write(header)

        for filename in glob.glob(folder + '*'):
            print filename
            json_file = open(filename, 'r')
            name = os.path.basename(filename)
            contents = json.load(json_file)
            json_file.close()

            total = len(contents)
            dir_count = self.get_dir_count(contents)
            file_count = self.get_file_count(contents)
            folder_names = self.get_folder_names_as_str(contents)
            file_names = self.get_file_names_as_str(contents)
            fo_and_fi_names = self.get_folder_and_file_names_as_str(contents)

            line = "%d" % total
            if total > 0:
                line = line + " " + "%.2f" % (float(dir_count) / total)
                line = line + " " + "%.2f" % (float(file_count) / total)
            else:
                line = line + " " + "%.2f" % 0
                line = line + " " + "%.2f" % 0

            line = line + " " + folder_names
            line = line + " " + file_names
            line = line + " " + fo_and_fi_names

            line = line + " " + name.split('.')[0]
            print line
            # line = line.replace(u"\u2019", "'")
            line = line.encode('utf-8')
            f.write(line)
            f.write('\n')
        print "Wrote contents features to %s" % f.name
        f.close()

    def get_readmes_features(self):
        folder = self.readmes_folder
        name = self.features_folder + "readme_data.txt"

        if not os.path.exists(os.path.dirname(name)):
            os.makedirs(os.path.dirname(name))
        f = open(name, 'w')
        header = "readme_filename repo_name\n"
        f.write(header)

        for filename in glob.glob(folder + '*'):
            print filename
            name = os.path.basename(filename)
            line = "%s" % filename
            line = line + " " + name.split('.')[0]
            f.write(line)
            f.write('\n')

        print "Wrote readmes features to %s" % f.name
        f.close()
        f.close()

    def get_trees_features(self):
        folder = self.trees_folder
        name = self.features_folder + "trees_data.txt"

        if not os.path.exists(os.path.dirname(name)):
            os.makedirs(os.path.dirname(name))
        f = open(name, 'w')
        header = "blob_paths repo_name\n"
        f.write(header)

        for filename in glob.glob(folder + '*'):
            print filename
            json_file = open(filename, 'r')
            name = os.path.basename(filename)

            contents_filename = filename.replace("json_trees", "json_contents")
            contents_json_file = open(contents_filename, 'r')

            root_folder_trees = json.load(json_file)
            contents = json.load(contents_json_file)

            contents_json_file.close()
            json_file.close()

            total_root_folders = len(root_folder_trees)
            print '%d root folders here' % total_root_folders

            if len(contents) > 0:
                blob_paths = "\""
                blob_paths += self.get_file_paths_as_str(contents=contents).replace('\"', '')
                blob_paths += " "
            else:
                blob_paths = "\""

            for root_folder_entry in root_folder_trees:
                folder_name = root_folder_entry['root_folder_name']
                folder_tree = root_folder_entry['tree']
                for tree_entry in folder_tree:
                    # print tree_entry
                    if tree_entry['type'] == 'blob':
                        blob_paths += tree_entry['path'].replace('\"', '')
                        blob_paths += " "
            blob_paths += "\""

            line = "%s" % blob_paths
            line = line + " " + name.split('.')[0]
            line = line.encode('utf-8')
            f.write(line)
            f.write('\n')

        print "Wrote trees features to %s" % f.name
        f.close()

    def get_inter_commit_distance_average(self, inter_commit_distance, total_commits):
        if total_commits > 1:
            return inter_commit_distance / (total_commits - 1)
        return 0

    def get_commits_per_day(self, first_commit, last_commit, all_commits_count):
        day_in_seconds = 86400

        try:
            first_commit_author_date = dateutil.parser.parse(first_commit['commit']['author']['date'])
            last_commit_author_date = dateutil.parser.parse(last_commit['commit']['author']['date'])
        except KeyError:
            first_commit_author_date = dateutil.parser.parse(first_commit['author_date'])
            last_commit_author_date = dateutil.parser.parse(last_commit['author_date'])

        commits_interval = last_commit_author_date - first_commit_author_date
        days = commits_interval.total_seconds() / day_in_seconds
        if days > 1:
            return all_commits_count / days
        return all_commits_count

    def get_commits_interval(self, first_commit, last_commit):
        day_in_seconds = 86400

        first_commit_author_date = dateutil.parser.parse(first_commit['commit']['author']['date'])
        last_commit_author_date = dateutil.parser.parse(last_commit['commit']['author']['date'])
        commits_interval = last_commit_author_date - first_commit_author_date
        days = commits_interval.total_seconds() / day_in_seconds

        return days

    def get_unique_authors(self, commits_list):
        authors = []
        for commit in commits_list:
            author = commit['author_email']
            if author not in authors:
                authors.append(author)
        return len(authors)

    def get_authors_vs_committers(self, commits_list):
        count = 0
        for commit in commits_list:
            author = commit['author_email']
            committer = commit['committer_email']
            if author != committer:
                count += 1
        return count

    def get_active_days(self, commits_list):
        day_in_seconds = 86400
        all_commits_count = len(commits_list)

        first_commit = commits_list[all_commits_count - 1]
        last_commit = commits_list[0]

        first_commit_author_date = dateutil.parser.parse(first_commit['author_date'])
        last_commit_author_date = dateutil.parser.parse(last_commit['author_date'])

        commits_interval = last_commit_author_date - first_commit_author_date
        days = commits_interval.total_seconds() / day_in_seconds

        active_days = []

        if days > 0:
            for commit in commits_list:
                commit_author_date = dateutil.parser.parse(commit['author_date'])
                active_day = datetime(year=commit_author_date.year, month=commit_author_date.month,
                                      day=commit_author_date.day)
                if active_day not in active_days:
                    active_days.append(active_day)
            if len(active_days) / math.ceil(days) > 1:
                return 1
            return len(active_days) / math.ceil(days)
        print 'only one commit here!'
        return 1
        #
        # if days > 1:
        #     prev_date = last_commit_author_date
        #
        #     active_days = 0
        #
        #     for commit in commits_list:
        #         commit_author_date = dateutil.parser.parse(commit['author_date'])
        #         print prev_date
        #
        #         print commit_author_date
        #
        #         print prev_date - timedelta(days=1)
        #
        #         print "ha"
        #         if commit_author_date > prev_date:
        #             print 'continue'
        #             continue
        #
        #         if prev_date >= commit_author_date > prev_date - timedelta(days=1):
        #             print 'active ++'
        #             active_days += 1
        #             dist = prev_date - commit_author_date
        #             shift = dist.total_seconds() / day_in_seconds
        #             print shift
        #             print int(shift)
        #             if shift < 1:
        #                 prev_date = prev_date - timedelta(days=1)
        #             else:
        #                 prev_date = prev_date - timedelta(days=int(shift))
        #
        #     print active_days
        #     print days
        #     return active_days / math.ceil(days)
        # return 1

    def get_all_languages(self):
        used_languages = {}
        for label in Labels.toArray():
            print label
            folder = self.updated_repos_folder
            for filename in glob.glob(folder + '*'):
                print filename
                json_file = open(filename, 'r')
                repo = json.load(json_file)

                try:
                    languages = repo["languages"]
                except KeyError:
                    print 'keyy'

                for language in languages:
                    if language not in used_languages:
                        used_languages[language] = 0
                        print 'Added %s to the list of used languages' % language
        print len(used_languages.keys())
        return collections.OrderedDict(used_languages)

    def get_dir_count(self, contents):
        count = 0
        for entry in contents:
            if entry['type'] == 'dir':
                count += 1
        return count

    def get_file_count(self, contents):
        count = 0
        for entry in contents:
            if entry['type'] == 'file':
                count += 1
        return count

    def get_folder_names_as_str(self, contents):
        result = "\""
        for entry in contents:
            if entry['type'] == 'dir':
                result += entry['name'] + " "
        result += "\""
        return result

    def get_file_names_as_str(self, contents):
        result = "\""
        for entry in contents:
            if entry['type'] == 'file':
                result += entry['name'] + " "
        result += "\""
        return result

    def get_languages_names_as_str(self, languages):
        result = "\""
        for language in languages:
            print language
            result += language + " "
        result = result[:-1]
        result += "\""
        return result

    def get_file_paths_as_str(self, contents):
        result = ""
        for entry in contents:
            if entry['type'] == 'file':
                result += entry['name'] + " "
        return result

    def get_folder_and_file_names_as_str(self, contents):
        result = "\""
        for entry in contents:
            entry_type = entry['type']
            if entry_type == 'file' or entry_type == 'dir':
                result += entry['name'] + " "
        result += "\""
        return result


if __name__ == '__main__':
    input_processor = InputProcessor()
    input_processor.urls_to_repo_names(filename='input_urls.txt')
    input_processor.names_to_json_repos(filename='input_names.txt')
    input_processor.names_to_readmes(filename='input_names.txt')
    input_processor.names_to_commits(filename='input_names.txt')
    input_processor.names_to_commits_interval(filename='input_names.txt')
    input_processor.names_to_contents(filename='input_names.txt')
    input_processor.names_to_punchcard(filename='input_names.txt')
    input_processor.contents_to_file_trees()

    input_processor.update_repos('commits_url', 'commits_count')
    input_processor.update_repos('comments_url', 'comments_count')
    input_processor.update_repos('languages_url', 'languages_count')
    input_processor.update_repos('labels_url', 'labels_count')
    input_processor.update_repos('tags_url', 'tags_count')
    input_processor.update_repos('issues_url', 'issues_count')
    input_processor.update_repos('branches_url', 'branches_count')

    input_processor.update_repos_with_languages()

    feature_extractor = FeatureExtractor()
    feature_extractor.get_contents_features()
    feature_extractor.get_repo_features()
    feature_extractor.get_commits_features()
    feature_extractor.get_commits_interval_features()

    feature_extractor.get_punchcard_features()
    feature_extractor.get_language_features(binary=False)
    feature_extractor.get_readmes_features()
    feature_extractor.get_trees_features()