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
        header = "weekend_commits weekday_commits work_hrs_commits non_work_hrs_commits inter_commit_distance_average repo_name\n"
        f.write(header)

        for filename in glob.glob(folder + '*'):
            json_file = open(filename, 'r')
            name = os.path.basename(filename)
            commits_list = json.load(json_file)
            json_file.close()

            total_commits = len(commits_list)

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
                    print 'distance '
                    print prev_date - author_date
                    distance = prev_date - author_date
                    hours = distance.total_seconds() / 3600
                    print hours
                    inter_commit_distance += hours
                prev_date = author_date

            line = "%.2f" % (float(weekend_commits_count) / total_commits)
            line = line + " " + "%.2f" % (float(weekday_commits_count) / total_commits)
            line = line + " " + "%.2f" % (float(work_hrs_commits_count) / total_commits)
            line = line + " " + "%.2f" % (float(non_work_hrs_commits_count) / total_commits)
            line = line + " " + "%.2f" % (float(inter_commit_distance) / (total_commits - 1))

            line = line + " " + name.split('.')[0]

            f.write(line)
            f.write('\n')
        print "Wrote commits features to %s" % f.name
        f.close()


featureExtraction = FeatureExtraction()
featureExtraction.get_commits_features('docs')

# featureExtraction.get_commits_features('dev')
# featureExtraction.get_commits_features('data')
# featureExtraction.get_commits_features('hw')
# featureExtraction.get_commits_features('edu')
# featureExtraction.get_commits_features('web')
# featureExtraction.get_commits_features('other')
