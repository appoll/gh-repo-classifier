import re

import pandas as pd
import sys

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import precision_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

sys.path.append('../..')
from collection.labels import Labels


def features(label):
    print('The label is :%s '%label)
    features = pd.read_csv("../../exploration/labelled/features/trees_data_%s.txt" % label, delimiter=" ", header=0)

    print features.shape

    features.to_csv('trees_repo_names_%s' % label, columns=["repo_name"])
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

def row_to_words(row):
    blob_paths = row['blob_paths']
    content = cleanString(blob_paths)
    return content

def cleanString(s):
    p = re.compile('(?<=[a-z])(?=[A-Z])')
    newS = p.sub(r' ',s)
    newS = re.sub('[0-9]+',' NN ',newS)
    newS = re.sub('[^a-zA-Z]',' ',newS)
    newS = re.sub('\W+',' ',newS)
    return newS.strip().lower()


features = [features(Labels.data), features(Labels.dev), features(Labels.docs), features(Labels.edu),
            features(Labels.hw), features(Labels.web), features(Labels.uncertain)]

data = pd.concat(features)
print data.shape

data['blob_paths_updated'] = data.apply(lambda row: row_to_words(row), axis=1)

cV = CountVectorizer(ngram_range=(1,4),max_features=7000, binary=True)
X = cV.fit_transform(data['blob_paths_updated'])

Y = data['label']

X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.2,random_state=0)

# C_range = np.logspace(-2, 10, 13)
# gamma_range = np.logspace(-9, 3, 13)
# gS = GridSearchCV(SVC(),{'kernel':['rbf'],'C':C_range,'gamma':gamma_range},n_jobs=-1)
n_estimators = [1000]
clf = GridSearchCV(RandomForestClassifier(),{'n_estimators':n_estimators})

# gS.fit(X_train,Y_train)
clf.fit(X_train,Y_train)
Y_pred = clf.predict(X_test)
s = precision_score(Y_test,Y_pred, average  = None)
print s
print clf.score(X_test,Y_test)