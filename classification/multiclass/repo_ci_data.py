import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import precision_score
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import train_test_split

from collection.labels import Labels

REPO = "repo"
CI = "commits_interval"
LANG = "languages"
COMMIT = "commit"
PUNCH = "punch_card"

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

punch_card_features = [get_features(Labels.data, PUNCH), get_features(Labels.dev, PUNCH),
                   get_features(Labels.docs, PUNCH),
                   get_features(Labels.edu, PUNCH),
                   get_features(Labels.hw, PUNCH), get_features(Labels.web, PUNCH),
                   get_features(Labels.uncertain, PUNCH)]


repo_data = pd.concat(repo_features)
ci_data = pd.concat(ci_features)
lang_data = pd.concat(lang_features)
commit_data = pd.concat(commit_features)
punch_card_data = pd.concat(punch_card_features)

repo_data = repo_data.drop_duplicates(subset=['repo_name'])
ci_data = ci_data.drop_duplicates(subset=['repo_name'])
commit_data = commit_data.drop_duplicates(subset=['repo_name'])
lang_data = lang_data.drop_duplicates(subset=['repo_name'])
punch_card_data = punch_card_data.drop_duplicates(subset=['repo_name'])

print 'Repo Data Shape'
print repo_data.shape
print 'Commits Interval Shape'
print ci_data.shape
print 'Languages Shape'
print lang_data.shape
print 'Commits Shape'
print commit_data.shape
print 'Punch Card Shape'
print punch_card_data.shape
print '\n'

# data = repo_data.merge(ci_data, on="repo_name", how="inner")
# data = data.merge(lang_data, on="repo_name", how="inner")

data = repo_data.merge(commit_data, on=["repo_name",'label'], how="inner")
data = data.merge(lang_data, on=["repo_name",'label'], how="inner")

# data = data.drop(labels=['label_x'], axis =1 )
# data = data.merge(punch_card_data, on="repo_name", how="inner")

# repo_data = repo_data.drop(labels='repo_name', axis=1)
# ci_data = ci_data.drop(labels='repo_name', axis=1)

data.to_csv('repo_ci_data_set')

ss = ShuffleSplit(n_splits=5, test_size=0.2, random_state=0)

all_labels = np.asarray(data['label'], dtype=int)
data_no_labels = np.asarray(data.drop(labels=['label', 'repo_name'], axis=1))

for train_index, test_index in ss.split(X=data_no_labels):
    train_data, test_data, train_labels, test_labels = data_no_labels[train_index], data_no_labels[test_index], \
                                                       all_labels[train_index], all_labels[test_index]
    print '\n'
    print data.shape
    print train_data.shape
    print test_data.shape

    forest_classifier = RandomForestClassifier(n_estimators=5000, max_depth=30)
    forest = forest_classifier.fit(train_data, train_labels)

    output = forest.predict(test_data)
    print mean_squared_error(output, test_labels)
    print accuracy_score(test_labels, output)
    score = precision_score(test_labels, output, average=None)
    print score
    print np.mean(score)
