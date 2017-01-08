import glob
import json
import os

import requests
from requests.auth import HTTPBasicAuth

from config.reader import ConfigReader


class Transformer:
    def __init__(self):
        self.username, self.password = ConfigReader().get_credentials()
        # self.repos_folder = "../collection/%s/repos/"

        # unarchived repos folder
        self.repos_folder = "../collection/%s/json_repos_unarchived/"

        self.updated_repos_folder = "../collection/%s/json_repos_updated/"

        self.commit_activity_folder = "../collection/%s/commit_activity/"
        # self.updated_repos_folder = "../collection/%s/updated_repos/"
        self.RESULTS_PER_PAGE = 30

    def branchCount(self, label):
        folder = self.repos_folder % label

        for filename in glob.glob(folder + '*'):
            f = open(filename, 'r')
            repoObject = json.load(f)
            f.close()
            branches_url = repoObject["branches_url"]
            branches_url = branches_url.split('{')[0]
            print branches_url

            new_filename = filename.replace("repos_unarchived", "repos_updated")

            if os.path.exists(new_filename):
                print new_filename, " exists"
                continue

            r = requests.get(branches_url, auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                if 'last' not in r.links:
                    branchesObject = r.json()
                    last_page = -1
                else:
                    print r.links
                    last_page_url = r.links['last']['url']
                    last_page = (int)(last_page_url.split('=')[1])
                    print last_page

                if last_page != -1:
                    req = requests.get(last_page_url, auth=HTTPBasicAuth(self.username, self.password))
                    if req.status_code == 200:
                        branchesObject = req.json()
                    else:
                        print 'Page request failed'

                branches_count = len(branchesObject)
                if last_page != -1:
                    branches_count += (last_page - 1) * self.RESULTS_PER_PAGE

                print branches_count
                repoObject["branches_count"] = branches_count
                del repoObject["branches_url"]
                if not os.path.exists(os.path.dirname(new_filename)):
                    os.makedirs(os.path.dirname(new_filename))
                with open(new_filename, 'w') as file:
                    print "Writing to %s" % file.name
                    file.write(json.dumps(repoObject))
                    file.close()
            else:
                print r

    def issuesCount(self, label):
        folder = self.updated_repos_folder % label

        for filename in glob.glob(folder + '*'):
            print filename
            f = open(filename, 'r')
            repoObject = json.load(f)
            f.close()

            if 'issues_count' in repoObject:
                print 'exists'
                continue

            issues_url = repoObject["issues_url"]
            # del repoObject[branches_url]
            issues_url = issues_url.split('{')[0]
            print issues_url

            r = requests.get(issues_url, auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                if 'last' not in r.links:
                    issuesObject = r.json()
                    last_page = -1
                else:
                    print r.links
                    last_page_url = r.links['last']['url']
                    last_page = (int)(last_page_url.split('=')[1])
                    print last_page

                if last_page != -1:
                    req = requests.get(last_page_url, auth=HTTPBasicAuth(self.username, self.password))
                    if req.status_code == 200:
                        issuesObject = req.json()
                    else:
                        print 'Page request failed'

                issues_count = len(issuesObject)
                if last_page != -1:
                    issues_count += (last_page - 1) * self.RESULTS_PER_PAGE

                print issues_count
                repoObject["issues_count"] = issues_count
                del repoObject["issues_url"]
                # new_filename = filename.replace("repos", "updated_repos")
                new_filename = filename
                if not os.path.exists(os.path.dirname(new_filename)):
                    os.makedirs(os.path.dirname(new_filename))
                with open(new_filename, 'w') as file:
                    print "Writing to %s" % file.name
                    file.write(json.dumps(repoObject))
                    file.close()
            else:
                print r

    def count(self, label, url_key, count_key):
        """

        :param label: label of repositories' class
        :param url: property to be replaced in the current json file
        :param count: new property's name in the current json file
        """
        folder = self.updated_repos_folder % label

        for filename in glob.glob(folder + '*'):
            print filename
            f = open(filename, 'r')
            repoObject = json.load(f)
            f.close()
            if count_key in repoObject:
                print 'exists'
                continue
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

                repoObject[count_key] = count
                try:
                    del repoObject[url_key]
                except KeyError:
                    print 'nothing to delete. move along'

                new_filename = filename
                if not os.path.exists(os.path.dirname(new_filename)):
                    os.makedirs(os.path.dirname(new_filename))
                with open(new_filename, 'w') as file:
                    print "Writing to %s" % file.name
                    file.write(json.dumps(repoObject))
                    file.close()
            elif r.status_code == 204:
                print r.status_code
                repoObject[count_key] = 0
                # above is really dumb, never writes back to file
            else:
                print r.status_code

    def commit_activity(self, label):
        """
        Maps the commit activity present in json files to the repo object, by adding new numerical values:

        Commit activity is a JSON array of 52 week objects, which is decoded to a Python list of dictionaries

         "commits_total" - sum over all weeks in the previous year
         "commits_mean" - mean over all weeks in the previous year
         "commits_range" - max - min
        :param label:
        """
        folder = self.commit_activity_folder % label

        for filename in glob.glob(folder + '*'):
            f = open(filename, 'r')
            year = json.load(f)
            print filename
            f.close()

            commits_total = sum(week['total'] for week in year)
            commits_mean = commits_total / 52
            commits_max = max(week['total'] for week in year)
            commits_min = min(week['total'] for week in year)
            commits_range = commits_max - commits_min

            new_filename = filename.replace("commit_activity", "updated_repos")

            f = open(new_filename, 'r+')
            repo = json.load(f)
            repo['commits_total'] = commits_total
            repo['commits_mean'] = commits_mean
            repo['commits_range'] = commits_range
            print "Writing to %s" % f.name
            f.seek(0)
            f.write(json.dumps(repo))
            f.close()

    def languages(self, label):
        folder = self.repos_folder % label

        for filename in glob.glob(folder + '*'):
            print "Checking %s" % filename

            f = open(filename, 'r')
            updated_folder_filename = filename.replace("unarchived", "updated")
            try:
                updated_folder_file = open(updated_folder_filename, 'r')
            except IOError:
                print 'Deleting %s' % filename
                os.remove(filename)
                continue

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


feature_converter = Transformer()
# feature_converter.branchCount('dev')
# feature_converter.branchCount('data')
# feature_converter.branchCount('docs')
# feature_converter.branchCount('edu')
# feature_converter.branchCount('hw')
# feature_converter.branchCount('web')

# feature_converter.issuesCount('dev')
# feature_converter.issuesCount('data')
# feature_converter.issuesCount('docs')
# feature_converter.issuesCount('edu')
# feature_converter.issuesCount('hw')
# feature_converter.issuesCount('web')


# feature_converter.count('edu', "tags_url", "tags_count")
# feature_converter.count('dev', "tags_url", "tags_count")
# feature_converter.count('web', "tags_url", "tags_count")
# feature_converter.count('data', "tags_url", "tags_count")
# feature_converter.count('docs', "tags_url", "tags_count")
# feature_converter.count('hw', "tags_url", "tags_count")

# feature_converter.count('edu', "contributors_url", "contributors_count")
# feature_converter.count('dev', "contributors_url", "contributors_count")
# feature_converter.count('web', "contributors_url", "contributors_count")
# feature_converter.count('data', "contributors_url", "contributors_count")
# feature_converter.count('docs', "contributors_url", "contributors_count")
# feature_converter.count('hw', "contributors_url", "contributors_count")
#
# feature_converter.count('edu', "labels_url", "labels_count")
# feature_converter.count('dev', "labels_url", "labels_count")
# feature_converter.count('web', "labels_url", "labels_count")
# feature_converter.count('data', "labels_url", "labels_count")
# feature_converter.count('docs', "labels_url", "labels_count")
# feature_converter.count('hw', "labels_url", "labels_count")

# feature_converter.count('edu', "languages_url", "languages_count")
# feature_converter.count('dev', "languages_url", "languages_count")
# feature_converter.count('web', "languages_url", "languages_count")
# feature_converter.count('data', "languages_url", "languages_count")
# feature_converter.count('docs', "languages_url", "languages_count")
# feature_converter.count('hw', "languages_url", "languages_count")
#
# feature_converter.count('edu', "branches_url", "branches_count")
# feature_converter.count('dev', "branches_url", "branches_count")
# feature_converter.count('web', "branches_url", "branches_count")
# feature_converter.count('data', "branches_url", "branches_count")
# feature_converter.count('docs', "branches_url", "branches_count")
# feature_converter.count('hw', "branches_url", "branches_count")

# feature_converter.commit_activity(label=Labels.edu.value)

# unsuccessful
# feature_converter.languages('data')

# feature_converter.languages('docs')
# feature_converter.languages('web')
# feature_converter.languages('dev')
# feature_converter.languages('hw')
# feature_converter.languages('edu')
# feature_converter.languages('data')

feature_converter.count('data', 'commits_url', 'commits_count')
feature_converter.count('dev', 'commits_url', 'commits_count')
feature_converter.count('docs', 'commits_url', 'commits_count')
feature_converter.count('edu', 'commits_url', 'commits_count')
feature_converter.count('hw', 'commits_url', 'commits_count')
feature_converter.count('web', 'commits_url', 'commits_count')

# feature_converter.issuesCountMatplotlib('dev')
