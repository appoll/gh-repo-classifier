import collections
import glob
import json
import math
import os
import sys

sys.path.append('..')
from datetime import datetime

import numpy as np
from sklearn.externals import joblib
import dateutil.parser

from collection.labels import Labels
from settings import LANGUAGE_FEATURES_NAME_PATH
from config.constants import LANGUAGE_FEATURES_NAME_FILE


class FeatureExtraction:
    def __init__(self):
        self.additional_commits_folder = "../exploration/additional/json_commits_%s/"
        self.additional_repos_folder = "../exploration/additional/json_repos_%s/"
        self.additional_contents_folder = "../exploration/additional/json_contents_%s"

        self.features_folder = "../exploration/features/"
        self.additional_features_folder = "../exploration/additional/features/"
        self.labelled_features_folder = "../exploration/labelled/features/"

        self.commits_folder = "../collection/%s/json_commits/"
        self.commits_interval_folder = "../collection/%s/json_commits_interval/"
        self.repos_folder = "../collection/%s/json_repos_updated/"
        self.contents_folder = "../collection/%s/json_contents/"
        self.trees_folder = "../collection/%s/json_trees/"
        self.punch_card_folder = "../collection/%s/json_punch_card/"

        self.labelled_repos_folder = "../collection/%s/json_repos_updated_labelled/"
        self.labelled_contents_folder = "../collection/%s/json_contents_labelled/"
        self.labelled_trees_folder = "../collection/%s/json_trees_labelled/"
        self.labelled_commits_folder = "../collection/%s/json_commits_labelled/"
        self.labelled_commits_interval_folder = "../collection/%s/json_commits_interval_labelled/"
        self.labelled_punch_card_folder = "../collection/%s/json_punch_card_labelled/"
        self.labelled_readmes_folder = "../collection/%s/json_readmes_unarchived_labelled/"

        self.all_languages = {}
        self.language_features = []

    def get_commits_interval_features(self, label, labelled):
        if labelled:
            folder = self.labelled_commits_interval_folder % label
            name = self.labelled_features_folder + "commits_interval_data_%s.txt" % label
        else:
            folder = self.commits_interval_folder % label
            name = self.features_folder + "commits_interval_data_%s.txt" % label

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

    def get_punchcard_features(self, label, labelled):
        if labelled:
            folder = self.labelled_punch_card_folder % label
            name = self.labelled_features_folder + "punch_card_data_%s.txt" % label
        else:
            folder = self.punch_card_folder % label
            name = self.features_folder + "punch_card_data_%s.txt" % label
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
    def get_commits_features(self, label, labelled):
        if labelled:
            folder = self.labelled_commits_folder % label
            name = self.labelled_features_folder + "commit_data_%s.txt" % label
        else:
            folder = self.commits_folder % label
            name = self.features_folder + "commit_data_%s.txt" % label

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

    def get_language_features(self, label, labelled, binary):
        if labelled:
            folder = self.labelled_repos_folder % label
            name = self.labelled_features_folder + "languages_data_%s.txt" % label
        else:
            folder = self.repos_folder % label
            name = self.features_folder + "languages_data_%s.txt" % label

        if len(self.all_languages.keys()) == 0:
            print 'Initialize all languages dict'
            self.all_languages = self.get_all_languages()

        if not os.path.exists(os.path.dirname(name)):
            os.makedirs(os.path.dirname(name))
        f = open(name, 'w')
        header = "languages_count languages_total_lines "
        self.language_features = []
        for language in self.all_languages:
            language = language.replace(" ", "_")
            header += language + " "

            # extend constant list of language features
            stringyfied_language = '\"' + language + '\"'
            self.language_features.extend([language])
        joblib.dump(self.language_features, LANGUAGE_FEATURES_NAME_PATH + LANGUAGE_FEATURES_NAME_FILE, compress=3)


        header += "repo_name\n"
        f.write(header)

        for filename in glob.glob(folder + '*'):
            print filename
            #print len(self.all_languages)
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
                #print language
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

            #print len(current_languages)

            line = "%.2f" % all_languages_count
            line = line + " " + "%.2f" % total_lines
            for code_lines in current_languages.values():
                line = line + " " + str(code_lines)

            line = line + " " + name.split('.')[0]

            f.write(line)
            f.write('\n')
        print "Wrote languages features to %s" % f.name
        f.close()

    def get_language_features_str(self, label, labelled):
        if labelled:
            folder = self.labelled_repos_folder % label
            name = self.labelled_features_folder + "languages_str_data_%s.txt" % label
        else:
            folder = self.repos_folder % label
            name = self.features_folder + "languages_str_data_%s.txt" % label

        if not os.path.exists(os.path.dirname(name)):
            os.makedirs(os.path.dirname(name))
        f = open(name, 'w')
        header = "languages_count languages_str "
        # for language in self.all_languages:
        #     language = language.replace(" ", "_")
        #     header += language + " "
        #
        header += "repo_name\n"
        f.write(header)

        for filename in glob.glob(folder + '*'):
            print filename
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

            all_languages_str = self.get_languages_names_as_str(languages)

            if repo_size == 0 or all_languages_count == 0:
                continue

            line = "%.2f" % all_languages_count
            line = line + " " + "%s" % all_languages_str
            line = line + " " + name.split('.')[0]

            f.write(line)
            f.write('\n')
        print "Wrote languages str features to %s" % f.name
        f.close()

    def get_all_languages(self):
        used_languages = {}
        for label in Labels.toArray():
            print label
            folder = self.labelled_repos_folder % label
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
        print 'uradura'
        print len(used_languages.keys())
        return collections.OrderedDict(used_languages)

    def get_repo_features(self, label, labelled):
        if labelled:
            folder = self.labelled_repos_folder % label
            name = self.labelled_features_folder + "repo_data_%s.txt" % label
        else:
            folder = self.repos_folder % label
            name = self.features_folder + "repo_data_%s.txt" % label

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

    def get_contents_features(self, label, labelled):
        if labelled:
            folder = self.labelled_contents_folder % label
            name = self.labelled_features_folder + "contents_data_%s.txt" % label
        else:
            folder = self.contents_folder % label
            name = self.features_folder + "contents_data_%s.txt" % label

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

    def get_trees_features(self, label, labelled):
        if labelled:
            folder = self.labelled_trees_folder % label
            name = self.labelled_features_folder + "trees_data_%s.txt" % label
        else:
            folder = self.trees_folder % label
            name = self.features_folder + "trees_data_%s.txt" % label

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
                blob_paths += self.get_file_paths_as_str(contents=contents).replace('\"','')
                blob_paths += " "
            else:
                blob_paths = "\""

            for root_folder_entry in root_folder_trees:
                folder_name = root_folder_entry['root_folder_name']
                folder_tree = root_folder_entry['tree']
                for tree_entry in folder_tree:
                    # print tree_entry
                    if tree_entry['type'] == 'blob':
                        blob_paths += tree_entry['path'].replace('\"','')
                        blob_paths += " "
            blob_paths += "\""

            line = "%s" % blob_paths
            line = line + " " + name.split('.')[0]
            line = line.encode('utf-8')
            f.write(line)
            f.write('\n')

        print "Wrote trees features to %s" % f.name
        f.close()

    def get_readmes_features(self, label):
        folder = self.labelled_readmes_folder % label
        name = self.labelled_features_folder + "readme_data_%s.txt" % label

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


featureExtraction = FeatureExtraction()
# featureExtraction.get_commits_features('docs', additional=True)
# featureExtraction.get_commits_features('dev', additional=True)
# featureExtraction.get_commits_features('data', additional=True)
# featureExtraction.get_commits_features('hw', additional=True)
# featureExtraction.get_commits_features('edu', additional=True)
# featureExtraction.get_commits_features('web', additional=True)
# featureExtraction.get_commits_features('other', additional=True)

# collect docs commits again

# featureExtraction.get_commits_features('docs', additional=False)

# success:
# featureExtraction.get_commits_features('dev', additional=False)
# featureExtraction.get_commits_features('data', additional=False)
# featureExtraction.get_commits_features('hw', additional=False)
# featureExtraction.get_commits_features('edu', additional=False)
# featureExtraction.get_commits_features('web', additional=False)
# featureExtraction.get_commits_features('other', additional=False)

# must be called all at once
# featureExtraction.get_language_features('dev', additional=False)
# featureExtraction.get_language_features('data', additional=False)
# featureExtraction.get_language_features('docs', additional=False)
# featureExtraction.get_language_features('edu', additional=False)
# featureExtraction.get_language_features('hw', additional=False)
# featureExtraction.get_language_features('web', additional=False)

# featureExtraction.get_repo_features('dev', additional=True)
# featureExtraction.get_repo_features('data', additional=True)
# featureExtraction.get_repo_features('docs', additional=True)
# featureExtraction.get_repo_features('edu', additional=True)
# featureExtraction.get_repo_features('hw', additional=True)
# featureExtraction.get_repo_features('web', additional=True)

# featureExtraction.get_all_languages()

# featureExtraction.get_contents_features('dev', additional=False)
# featureExtraction.get_contents_features('data', additional=False)
# featureExtraction.get_contents_features('docs', additional=False)
# featureExtraction.get_contents_features('edu', additional=False)
# featureExtraction.get_contents_features('hw', additional=False)
# featureExtraction.get_contents_features('web', additional=False)

# featureExtraction.get_commits_interval_features('dev')
# featureExtraction.get_commits_interval_features('data')
# featureExtraction.get_commits_interval_features('docs')
# featureExtraction.get_commits_interval_features('edu')
# featureExtraction.get_commits_interval_features('hw')
# featureExtraction.get_commits_interval_features('web')
#
# featureExtraction.get_repo_features('dev', labelled=True)
# featureExtraction.get_repo_features('data', labelled=True)
# featureExtraction.get_repo_features('docs', labelled=True)
# featureExtraction.get_repo_features('edu', labelled=True)
# featureExtraction.get_repo_features('hw', labelled=True)
# featureExtraction.get_repo_features('web', labelled=True)
# featureExtraction.get_repo_features('other', labelled=True)
#
# featureExtraction.get_language_features('dev', labelled=True, binary=True)
# featureExtraction.get_language_features('data', labelled=True, binary=True)
# featureExtraction.get_language_features('docs', labelled=True, binary=True)
# featureExtraction.get_language_features('edu', labelled=True, binary=True)
# featureExtraction.get_language_features('hw', labelled=True, binary=True)
# featureExtraction.get_language_features('web', labelled=True, binary=True)
# featureExtraction.get_language_features('other', labelled=True, binary=True)

featureExtraction.get_language_features('dev', labelled=True, binary=False)
featureExtraction.get_language_features('data', labelled=True, binary=False)
featureExtraction.get_language_features('docs', labelled=True, binary=False)
featureExtraction.get_language_features('edu', labelled=True, binary=False)
featureExtraction.get_language_features('hw', labelled=True, binary=False)
featureExtraction.get_language_features('web', labelled=True, binary=False)
featureExtraction.get_language_features('other', labelled=True, binary=False)

# featureExtraction.get_contents_features('dev', labelled=True)
# featureExtraction.get_contents_features('data', labelled=True)
# featureExtraction.get_contents_features('docs', labelled=True)
# featureExtraction.get_contents_features('edu', labelled=True)
# featureExtraction.get_contents_features('hw', labelled=True)
# featureExtraction.get_contents_features('web', labelled=True)
# featureExtraction.get_contents_features('other', labelled=True)
# #
# featureExtraction.get_trees_features('dev', labelled=True)
# featureExtraction.get_trees_features('data', labelled=True)
# featureExtraction.get_trees_features('docs', labelled=True)
# featureExtraction.get_trees_features('edu', labelled=True)
# featureExtraction.get_trees_features('hw', labelled=True)
# featureExtraction.get_trees_features('web', labelled=True)
# featureExtraction.get_trees_features('other', labelled=True)

# featureExtraction.get_language_features_str('dev', labelled=True)
# featureExtraction.get_language_features_str('data', labelled=True)
# featureExtraction.get_language_features_str('docs', labelled=True)
# featureExtraction.get_language_features_str('edu', labelled=True)
# featureExtraction.get_language_features_str('hw', labelled=True)
# featureExtraction.get_language_features_str('web', labelled=True)
# featureExtraction.get_language_features_str('other', labelled=True)

# featureExtraction.get_commits_interval_features('dev', labelled=True)
# featureExtraction.get_commits_interval_features('data', labelled=True)
# featureExtraction.get_commits_interval_features('docs', labelled=True)
# featureExtraction.get_commits_interval_features('edu', labelled=True)
# featureExtraction.get_commits_interval_features('hw', labelled=True)
# featureExtraction.get_commits_interval_features('web', labelled=True)
# featureExtraction.get_commits_interval_features('other', labelled=True)
#
# featureExtraction.get_punchcard_features('dev', labelled=True)
# featureExtraction.get_punchcard_features('data', labelled=True)
# featureExtraction.get_punchcard_features('docs', labelled=True)
# featureExtraction.get_punchcard_features('edu', labelled=True)
# featureExtraction.get_punchcard_features('hw', labelled=True)
# featureExtraction.get_punchcard_features('web', labelled=True)
# featureExtraction.get_punchcard_features('other', labelled=True)
#
# featureExtraction.get_commits_features('dev', labelled=True)
# featureExtraction.get_commits_features('data', labelled=True)
# featureExtraction.get_commits_features('docs', labelled=True)
# featureExtraction.get_commits_features('edu', labelled=True)
# featureExtraction.get_commits_features('hw', labelled=True)
# featureExtraction.get_commits_features('web', labelled=True)
# featureExtraction.get_commits_features('other', labelled=True)
#
# featureExtraction.get_readmes_features('dev')
# featureExtraction.get_readmes_features('data')
# featureExtraction.get_readmes_features('docs')
# featureExtraction.get_readmes_features('edu')
# featureExtraction.get_readmes_features('hw')
# featureExtraction.get_readmes_features('web')
# featureExtraction.get_readmes_features('other')
