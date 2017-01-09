import pandas as pd

from classification import svc_linear
from collection.labels import Labels


def features(label):
    features = pd.read_csv("../../exploration/features/commit_data_%s.txt" % label.value, delimiter=" ", header=0)

    features = features.drop(labels='repo_name', axis=1)

    if label == Labels.dev:
        features['label'] = 1
    else:
        features['label'] = 0
    return features


data = [features(Labels.edu), features(Labels.data), features(Labels.hw), features(Labels.web), features(Labels.dev),
        features(Labels.docs)]

data = pd.concat(data)

train_data = data.drop(labels='label', axis=1)

labels = data['label']

print data.shape
print train_data.shape
print labels.shape

training_score, testing_score = svc_linear.run(train_data, labels)

print training_score
print testing_score
