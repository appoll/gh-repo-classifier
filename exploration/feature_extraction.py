import glob
import json
import os
from datetime import datetime

import dateutil.parser


class FeatureExtraction:
    def __init__(self):
        self.additional_commits_folder = "../exploration/additional/json_commits_%s/"
        self.additional_features_folder = "../exploration/additional/features/"

        self.commits_folder = "../exploration/additional/json_commits_%s/"
        self.features_folder = "../exploration/additional/features/"

    def get_commits_features(self, label):
        folder = self.additional_commits_folder % label
        name = self.additional_features_folder + "commit_data_%s.txt" % label

        if not os.path.exists(os.path.dirname(name)):
            os.makedirs(os.path.dirname(name))
        f = open(name, 'w')
        header = "all_commits weekend_commits weekday_commits work_hrs_commits non_work_hrs_commits inter_commit_distance_average commits_per_day_average authors_count author_vs_committer repo_name\n"
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


featureExtraction = FeatureExtraction()
featureExtraction.get_commits_features('docs')

featureExtraction.get_commits_features('dev')
featureExtraction.get_commits_features('data')
featureExtraction.get_commits_features('hw')
featureExtraction.get_commits_features('edu')
featureExtraction.get_commits_features('web')
featureExtraction.get_commits_features('other')
