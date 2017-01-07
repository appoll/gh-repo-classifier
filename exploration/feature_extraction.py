import collections
import glob
import json
import math
import os
from datetime import datetime

import dateutil.parser

from collection.labels import Labels


class FeatureExtraction:
    def __init__(self):
        self.additional_commits_folder = "../exploration/additional/json_commits_%s/"
        self.additional_features_folder = "../exploration/additional/features/"

        self.commits_folder = "../collection/%s/json_commits/"
        self.features_folder = "../exploration/features/"

        self.repos_folder = "../collection/%s/json_repos_updated/"

        self.all_languages = {}

    def get_commits_features(self, label, additional):
        if additional:
            folder = self.additional_commits_folder % label
            name = self.additional_features_folder + "commit_data_%s.txt" % label
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

        first_commit_author_date = dateutil.parser.parse(first_commit['author_date'])
        last_commit_author_date = dateutil.parser.parse(last_commit['author_date'])
        commits_interval = last_commit_author_date - first_commit_author_date
        days = commits_interval.total_seconds() / day_in_seconds
        if days > 1:
            return all_commits_count / days
        return all_commits_count

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

    def get_language_features(self, label, additional):
        if additional:
            folder = self.repos_folder % label
            name = self.additional_features_folder + "languages_data_%s.txt" % label
        else:
            folder = self.repos_folder % label
            name = self.features_folder + "languages_data_%s.txt" % label

        if len(self.all_languages.keys()) == 0:
            print 'Initialize all languages dict'
            self.all_languages = self.get_all_languages()

        if not os.path.exists(os.path.dirname(name)):
            os.makedirs(os.path.dirname(name))
        f = open(name, 'w')
        header = "languages_count total_bytes "
        for language in self.all_languages:
            language = language.replace(" ", "_")
            header += language + " "

        header += "repo_name\n"
        f.write(header)

        for filename in glob.glob(folder + '*'):
            print filename
            print len(self.all_languages)
            current_languages = self.all_languages.fromkeys(self.all_languages, 0)
            json_file = open(filename, 'r')
            name = os.path.basename(filename)
            repo = json.load(json_file)

            try:
                languages = repo["languages"]
            except KeyError:
                print "Key Error in %s" % filename
                continue

            all_languages_count = len(languages)
            total_bytes = sum(languages.itervalues())

            for language, bytes in languages.iteritems():
                print language
                if language not in current_languages:
                    raise ValueError("Should not be!")
                try:
                    current_languages[language] = "%.2f" % (float(bytes) / total_bytes)
                except ZeroDivisionError:
                    current_languages[language] = "%.2f" % total_bytes

            print 'heee'
            print len(current_languages)

            line = "%.2f" % all_languages_count
            line = line + " " + "%.2f" % total_bytes
            for bytes in current_languages.values():
                line = line + " " + str(bytes)

            line = line + " " + name.split('.')[0]

            f.write(line)
            f.write('\n')
        print "Wrote languages features to %s" % f.name
        f.close()

    def get_all_languages(self):
        used_languages = {}
        for label in Labels.toArray():
            print label
            folder = self.repos_folder % label.value
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

    def get_repo_features(self, label, additional):
        if additional:
            folder = self.repos_folder % label
            name = self.additional_features_folder + "repo_data_%s.txt" % label
        else:
            folder = self.repos_folder % label
            name = self.features_folder + "repo_data_%s.txt" % label

        if not os.path.exists(os.path.dirname(name)):
            os.makedirs(os.path.dirname(name))
        f = open(name, 'w')
        header = "size labels tags issues branches languages forks repo_name\n"
        f.write(header)

        for filename in glob.glob(folder + '*'):
            print filename
            json_file = open(filename, 'r')
            name = os.path.basename(filename)
            repo = json.load(json_file)
            json_file.close()

            # size in KB
            size = repo['size']
            labels = repo['labels_count']
           # contributors = repo['contributors_count']
            tags = repo['tags_count']
            issues = repo['issues_count']
            branches = repo['branches_count']
            languages = repo['languages_count']
            forks = repo['forks']

            line = "%d" % size
            line = line + " " + "%d" % labels
            #line = line + " " + "%d" % contributors
            line = line + " " + "%d" % tags
            line = line + " " + "%d" % issues
            line = line + " " + "%d" % branches
            line = line + " " + "%d" % languages
            line = line + " " + "%d" % forks

            line = line + " " + name.split('.')[0]

            f.write(line)
            f.write('\n')
        print "Wrote repo features to %s" % f.name
        f.close()

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

# featureExtraction.get_repo_features('dev', additional=False)
# featureExtraction.get_repo_features('data', additional=False)
# featureExtraction.get_repo_features('docs', additional=False)
# featureExtraction.get_repo_features('edu', additional=False)
# featureExtraction.get_repo_features('hw', additional=False)
# featureExtraction.get_repo_features('web', additional=False)

# featureExtraction.get_all_languages()
