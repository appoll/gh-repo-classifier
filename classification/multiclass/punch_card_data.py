import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import precision_score
from sklearn.model_selection import ShuffleSplit

from collection.labels import Labels
import numpy as np

def features(label):
    path = "../../exploration/labelled/features/punch_card_data_%s.txt" % label
    features = pd.read_csv(path, delimiter=" ", header=0, skipfooter=1)

    print path
    print features.shape

    features.to_csv('punch_repo_names_%s' % label, columns=["repo_name"])

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
print data.shape
data = data.drop_duplicates(subset=['repo_name'])
print data.shape

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


