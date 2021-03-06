import pandas as pd

from collection.labels import Labels

def features(label):
    features = pd.read_csv("../../exploration/labelled/features/contents_data_%s.txt" % label, delimiter=" ", header=0)

    print features.shape

    #features.to_csv('contents_repo_names_%s' % label, columns=["repo_name"])
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
    elif label == Labels.uncertain:
        features['label'] = 6

    return features


features = [features(Labels.data), features(Labels.dev), features(Labels.docs), features(Labels.edu),
            features(Labels.hw), features(Labels.web), features(Labels.uncertain)]

data = pd.concat(features)
repo_names = data['repo_name']
data = data.drop(labels='repo_name', axis=1)

print data.shape
#
# train_data = data
# train_data = train_data[(train_data.T != 0).any()]
# labels = train_data['label']
# train_data = train_data.drop(labels='label', axis=1)

print data.shape
# print train_data.shape
# print labels.shape

