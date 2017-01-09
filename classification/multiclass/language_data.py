import numpy as np
import pandas as pd

from classification import svc_linear
from collection.labels import Labels


def content(label):
    features = pd.read_csv("../exploration/features/languages_data_%s.txt" % label.value, delimiter=" ", header=0)
    print("./exploration/features/languages_data_%s.txt" % label.value)
    return features


def features(label):
    features = pd.read_csv("../exploration/features/languages_data_%s.txt" % label.value, delimiter=" ", header=0)
    print("./exploration/features/languages_data_%s.txt" % label.value)

    print features.shape

    features = features.drop(labels='repo_name', axis=1)

    print features.shape

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

    return features


data = [features(Labels.edu), features(Labels.data), features(Labels.hw), features(Labels.web), features(Labels.dev),
        features(Labels.docs)]

data = pd.concat(data)

train_data = data
train_data = train_data[(train_data.T != 0).any()]
labels = train_data['label']
train_data = train_data.drop(labels='label', axis=1)

print data.shape
print train_data.shape
print labels.shape

training_score, testing_score = svc_linear.run(train_data, labels)

print training_score
print testing_score
