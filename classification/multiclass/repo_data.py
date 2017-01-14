import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import precision_score
from sklearn.model_selection import train_test_split

from collection.labels import Labels


def features(label):
    features = pd.read_csv("../../exploration/labelled/features/repo_data_%s.txt" % label, delimiter=" ",
                           header=0)

    #features.to_csv('repo_repo_names_%s' % label, columns=["repo_name"])
    features = features.drop(labels='repo_name', axis=1)

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


features = [features(Labels.data), features(Labels.dev), features(Labels.docs), features(Labels.edu),
            features(Labels.hw), features(Labels.web), features(Labels.uncertain)]

data = pd.concat(features)

train_data, test_data = train_test_split(data, test_size=0.2)

train_labels = train_data['label']
test_labels = test_data['label']

train_data = train_data.drop(labels='label', axis=1)
test_data = test_data.drop(labels='label', axis=1)

print data.shape
print train_data.shape
print test_data.shape

forest_classifier = RandomForestClassifier(n_estimators=500, max_depth=5, max_features=3)
forest = forest_classifier.fit(train_data, train_labels)

output = forest.predict(test_data)

print mean_squared_error(output, test_labels)
print accuracy_score(test_labels, output)
score = precision_score(test_labels, output, average=None)
print score
print np.mean(score)
