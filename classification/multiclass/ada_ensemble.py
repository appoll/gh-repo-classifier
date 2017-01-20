import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import precision_score
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
import sys
sys.path.append('../..')
from config.helper import Helper
from keyword_spotting import KeywordSpotting

from collection.labels import Labels

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

# trees_features = [get_features(Labels.data, TREES), get_features(Labels.dev, TREES),
#                    get_features(Labels.docs, TREES),
#                    get_features(Labels.edu, TREES),
#                    get_features(Labels.hw, TREES), get_features(Labels.web, TREES),
#                    get_features(Labels.uncertain, TREES)]

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

# trees_data = pd.concat(trees_features)

repo_data = repo_data.drop_duplicates(subset=['repo_name'])
ci_data = ci_data.drop_duplicates(subset=['repo_name'])
commit_data = commit_data.drop_duplicates(subset=['repo_name'])
lang_data = lang_data.drop_duplicates(subset=['repo_name'])

readme_data = readme_data.drop_duplicates(subset=['repo_name'])

contents_data = contents_data.drop_duplicates(subset=['repo_name'])

# trees_data = trees_data.drop_duplicates(subset=['repo_name'])

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
# print 'Trees Shape'
# print trees_data.shape
print '\n'

data_1 = repo_data.merge(commit_data, on=["repo_name", "label"], how="inner")
data_1 = data_1.merge(lang_data, on=["repo_name", "label"], how="inner")

print data_1.shape
data_1.to_csv('data_set_1')

data_2 = data_1.merge(contents_data, on=["repo_name","label"], how="inner")
print data_2.shape
data_1.to_csv('data_set_1')

data_3 = data_2.merge(readme_data, on=["repo_name", "label"], how="left")

data_3.to_csv('data_set_3')
print data_3.shape

# hack to get language features names by excluding all the other feature names

LANGUAGE_FEATURES = list(data_3.columns.values)
LANGUAGE_FEATURES = [label for label in LANGUAGE_FEATURES if label not in REPO_FEATURES and label not in CI_FEATURES and label not in COMMIT_FEATURES and label not in ['label','repo_name'] and label not in README_FEATURES and label not in TREE_FEATURES and label not in CONTENT_FEATURES]


# below dataframes have all the features which need to be separated
train_data, test_data = train_test_split(data_3, test_size=0.2, random_state=2)


# first classifier
clf_data_1 = [train_data, test_data]
clf_data_1 = pd.concat(clf_data_1)
repo_names_1 = clf_data_1['repo_name']

clf_data_1 = clf_data_1[REPO_FEATURES + COMMIT_FEATURES +LANGUAGE_FEATURES]
train_data_1 = train_data[REPO_FEATURES + COMMIT_FEATURES + LANGUAGE_FEATURES]
test_data_1 = test_data[REPO_FEATURES + COMMIT_FEATURES + LANGUAGE_FEATURES]

train_labels_1 = train_data['label']
test_labels_1 = test_data['label']

# np.any(np.isinf(train_repo_labels))
# np.all(np.isfinite(train_repo_labels))
# np.any(np.isinf(train_repo_data))
# np.all(np.isfinite(train_repo_data))

forest_classifier = RandomForestClassifier(n_estimators=5000, max_depth=30)
forest = forest_classifier.fit(train_data_1, train_labels_1)

output = forest.predict(test_data_1)
print mean_squared_error(output, test_labels_1)
print accuracy_score(test_labels_1, output)
score = precision_score(test_labels_1, output, average=None)
print score
print np.mean(score)

# Helper().write_probabilities(forest, clf_data_1, repo_names_1, 'prob/prob_repo_lang_commit_data')

# second classifier
train_data_2 = train_data[["repo_name"] + README_FEATURES + CONTENT_FEATURES + ["label"]]
test_data_2 = test_data[["repo_name"] + README_FEATURES + CONTENT_FEATURES + ["label"]]

train_data_2.to_csv("train_data_trash.txt", sep=",")



clf = KeywordSpotting()
# clf.train(train_data_2)
# clf.save_classifier()

clf.load_classifier()

clf.evaluate(test_data_2)
#
#
predict_1 = forest_classifier.predict_proba(train_data_1)
predict_2 = clf.predict_proba(train_data_2)
predict = np.column_stack((predict_1, predict_2))

ada = RandomForestClassifier(n_estimators=5000, max_depth=20)

ada.fit(X=predict, y=train_labels_1)

eval_1 = forest_classifier.predict_proba(test_data_1)
eval_2 = clf.predict_proba(test_data_2)
eval = np.column_stack((eval_1, eval_2))

eval_out = ada.predict(eval)

joblib.dump(ada, filename="final_rf.pkl", compress=3)
print "MSE ADABOOST: "
print mean_squared_error(eval_out, test_labels_1)
print "ACCURACY ADABOOST: "
print accuracy_score(test_labels_1, eval_out)
score = precision_score(test_labels_1, eval_out, average=None)
print "PRECISION ADABOOST: "
print score
print np.mean(score)



# clf.load("path")


# third classifier
