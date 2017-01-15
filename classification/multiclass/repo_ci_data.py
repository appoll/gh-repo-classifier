import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import precision_score
from sklearn.model_selection import train_test_split

from collection.labels import Labels

REPO = "repo"
CI = "commits_interval"
LANG = "languages"


def get_features(label, which):
    path = "../../exploration/labelled/features/%s_data_%s.txt" % (which, label)
    features = pd.read_csv(path, delimiter=" ",
                           header=0)
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

repo_data = pd.concat(repo_features)
ci_data = pd.concat(ci_features)
lang_data = pd.concat(lang_features)

print repo_data.shape

print ci_data.shape

data = repo_data.merge(ci_data, on="repo_name", how="inner")
data = data.merge(lang_data, on="repo_name", how="inner")
# repo_data = repo_data.drop(labels='repo_name', axis=1)
# ci_data = ci_data.drop(labels='repo_name', axis=1)

data.to_csv('repo_ci_data_set')

train_data, test_data = train_test_split(data, test_size=0.2)

train_labels = train_data['label_x']
test_labels = test_data['label_x']

train_data = train_data.drop(labels=['label_x', 'label_y', 'repo_name'], axis=1)
test_data = test_data.drop(labels=['label_x', 'label_y', 'repo_name'], axis=1)

print data.shape
print train_data.shape
print test_data.shape

train_data.to_csv('train_repo_ci_data_set')

forest_classifier = RandomForestClassifier(n_estimators=500, max_depth=5, max_features=3)
forest = forest_classifier.fit(train_data, train_labels)

output = forest.predict(test_data)
print mean_squared_error(output, test_labels)
print accuracy_score(test_labels, output)
score = precision_score(test_labels, output, average=None)
print score
print np.mean(score)
