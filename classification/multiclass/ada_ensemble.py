import csv
import re

import numpy as np
import pandas as pd
import sys

from classification.multiclass.readme_classifier import ReadmeClassifier
from classification.multiclass.tree_classifier import TreeClassifier
from config.constants import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import precision_score
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
from base_classifier import BaseClassifier
from config.helper import Helper
from keyword_spotting import KeywordSpotting

from collection.labels import Labels
csv.field_size_limit(sys.maxsize)
REPO_FEATURES = ["size", "labels", "tags", "issues", "branches", "languages", "forks", "commits", "comments"]
COMMIT_FEATURES = ["all_commits", "weekend_commits", "weekday_commits", "work_hrs_commits", "non_work_hrs_commits",
                   "inter_commit_distance_average", "commits_per_day_average", "authors_count", "author_vs_committer",
                   "active_days"]
CI_FEATURES = ["commits_count", "commits_interval_days", "commits_per_day"]

README_FEATURES = ["readme_filename"]

CONTENT_FEATURES = ["total", "dirs", "files", "folder_names", "file_names", "fo_and_fi_names"]

TREE_FEATURES = ["blob_paths"]

REPO = "repo"
CI = "commits_interval"
LANG = "languages"
COMMIT = "commit"

README = "readme"

CONTENTS = "contents"

TREES = "trees"


def get_features(label, which):
    path = "../../exploration/labelled/features/%s_data_%s.txt" % (which, label)
    features = pd.read_csv(path, delimiter=" ",
                           header=0, skipfooter=1)
    print path
    print features.shape

    # features.to_csv('repo_repo_names_%s' % label, columns=["repo_name"])

    if label == Labels.data:
        features['label'] = 0
    elif label == Labels.dev:
        features['label'] = 1
    elif label == Labels.docs:
        features['label'] = 2
    elif label == Labels.edu:
        features['label'] = 3
    elif label == Labels.hw:
        features['label'] = 4
    elif label == Labels.web:
        features['label'] = 5
    elif label == Labels.uncertain:
        features['label'] = 6
    return features


def row_to_words(row):
    blob_paths = row['blob_paths']
    content = cleanString(blob_paths)
    return content


def cleanString(s):
    p = re.compile('(?<=[a-z])(?=[A-Z])')
    newS = p.sub(r' ', s)
    newS = re.sub('[0-9]+', ' NN ', newS)
    newS = re.sub('[^a-zA-Z]', ' ', newS)
    newS = re.sub('\W+', ' ', newS)
    return newS.strip().lower()

repo_features = [get_features(Labels.data, REPO), get_features(Labels.dev, REPO), get_features(Labels.docs, REPO),
                 get_features(Labels.edu, REPO),
                 get_features(Labels.hw, REPO), get_features(Labels.web, REPO), get_features(Labels.uncertain, REPO)]

ci_features = [get_features(Labels.data, CI), get_features(Labels.dev, CI), get_features(Labels.docs, CI),
               get_features(Labels.edu, CI),
               get_features(Labels.hw, CI), get_features(Labels.web, CI), get_features(Labels.uncertain, CI)]

lang_features = [get_features(Labels.data, LANG), get_features(Labels.dev, LANG), get_features(Labels.docs, LANG),
                 get_features(Labels.edu, LANG),
                 get_features(Labels.hw, LANG), get_features(Labels.web, LANG), get_features(Labels.uncertain, LANG)]

commit_features = [get_features(Labels.data, COMMIT), get_features(Labels.dev, COMMIT),
                   get_features(Labels.docs, COMMIT),
                   get_features(Labels.edu, COMMIT),
                   get_features(Labels.hw, COMMIT), get_features(Labels.web, COMMIT),
                   get_features(Labels.uncertain, COMMIT)]

readme_features = [get_features(Labels.data, README), get_features(Labels.dev, README),
                   get_features(Labels.docs, README),
                   get_features(Labels.edu, README),
                   get_features(Labels.hw, README), get_features(Labels.web, README),
                   get_features(Labels.uncertain, README)]

trees_features = [get_features(Labels.data, TREES), get_features(Labels.dev, TREES),
                   get_features(Labels.docs, TREES),
                   get_features(Labels.edu, TREES),
                   get_features(Labels.hw, TREES), get_features(Labels.web, TREES),
                   get_features(Labels.uncertain, TREES)]

contents_features = [get_features(Labels.data, CONTENTS), get_features(Labels.dev, CONTENTS),
                     get_features(Labels.docs, CONTENTS),
                     get_features(Labels.edu, CONTENTS),
                     get_features(Labels.hw, CONTENTS), get_features(Labels.web, CONTENTS),
                     get_features(Labels.uncertain, CONTENTS)]

repo_data = pd.concat(repo_features)
ci_data = pd.concat(ci_features)
lang_data = pd.concat(lang_features)
commit_data = pd.concat(commit_features)

readme_data = pd.concat(readme_features)

contents_data = pd.concat(contents_features)

trees_data = pd.concat(trees_features)

repo_data = repo_data.drop_duplicates(subset=['repo_name'])
ci_data = ci_data.drop_duplicates(subset=['repo_name'])
commit_data = commit_data.drop_duplicates(subset=['repo_name'])
lang_data = lang_data.drop_duplicates(subset=['repo_name'])

readme_data = readme_data.drop_duplicates(subset=['repo_name'])

contents_data = contents_data.drop_duplicates(subset=['repo_name'])

trees_data = trees_data.drop_duplicates(subset=['repo_name'])

print 'Repo Data Shape'
print repo_data.shape
print 'Commits Interval Shape'
print ci_data.shape
print 'Languages Shape'
print lang_data.shape
print 'Commits Shape'
print commit_data.shape
print 'Readme Shape'
print readme_data.shape
print 'Contents Shape'
print contents_data.shape
print 'Trees Shape'
print trees_data.shape
print '\n'

data_1 = repo_data.merge(commit_data, on=["repo_name", "label"], how="inner")
data_1 = data_1.merge(lang_data, on=["repo_name", "label"], how="inner")

print data_1.shape
data_1.to_csv('data_set_1')

data_2 = data_1.merge(contents_data, on=["repo_name","label"], how="inner")
print data_2.shape
data_1.to_csv('data_set_1')

data_2 = data_2.merge(trees_data, on=["repo_name", "label"], how="left")

data_3 = data_2.merge(readme_data, on=["repo_name", "label"], how="left")

data_3.to_csv('data_set_3')
print data_3.shape

# hack to get language features names by excluding all the other feature names

LANGUAGE_FEATURES = list(data_3.columns.values)
LANGUAGE_FEATURES = [label for label in LANGUAGE_FEATURES if label not in REPO_FEATURES and label not in CI_FEATURES and label not in COMMIT_FEATURES and label not in ['label','repo_name'] and label not in README_FEATURES and label not in TREE_FEATURES and label not in CONTENT_FEATURES]


# below dataframes have all the features which need to be separated
train_data, test_data = train_test_split(data_3, test_size=0.2, random_state=2)

# first classifier

commit_clf = BaseClassifier(INPUT_COMMIT)
commit_clf.train(train_data)
commit_clf.save_model()
commit_clf.write_probabilities(train_data, test_data)
commit_clf.evaluate(test_data)

lang_clf = BaseClassifier(INPUT_LANGUAGE)
lang_clf.train(train_data)
lang_clf.save_model()
lang_clf.write_probabilities(train_data, test_data)
lang_clf.evaluate(test_data)

repo_clf = BaseClassifier(INPUT_REPO)
repo_clf.train(train_data)
repo_clf.save_model()
repo_clf.write_probabilities(train_data, test_data)
repo_clf.evaluate(test_data)

all_clf = BaseClassifier(INPUT_ALL)
all_clf.train(train_data)
all_clf.save_model()
all_clf.write_probabilities(train_data, test_data)
all_clf.evaluate(test_data)

new_clf = BaseClassifier(INPUT_COMMIT)
new_clf.load_model()
new_clf.evaluate(test_data)


# second classifier
# train_data_2 = train_data[["repo_name"] + README_FEATURES + CONTENT_FEATURES + ["label"]]
# test_data_2 = test_data[["repo_name"] + README_FEATURES + CONTENT_FEATURES + ["label"]]
#
#
# clf = KeywordSpotting()
# clf.train(train_data_2)
#
# clf.write_proba(dataframe_train=train_data_2, dataframe_test=test_data_2)


# third classifier
# tree_clf = TreeClassifier()
# tree_clf.train(train_data)
# tree_clf.write_probabilities(train_data, test_data)
#
# tree_clf.evaluate(test_data)

# fourth classifier
# readme_clf = ReadmeClassifier()
# readme_clf.train(train_data)
# readme_clf.write_probabilities(train_data, test_data)
# readme_clf.evaluate(test_data)
