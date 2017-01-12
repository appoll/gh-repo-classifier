import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import mean_squared_error
from sklearn.metrics import precision_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.svm import SVC

from classification import svc
from collection.labels import Labels
import numpy as np


def features(label):
    features = pd.read_csv("../../exploration/labelled/features/languages_str_data_%s.txt" % label.value, delimiter=" ",
                           header=0)
    print '/labelled/features/languages_data_%s' % label
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

features = [features(Labels.edu), features(Labels.data), features(Labels.hw), features(Labels.web),
            features(Labels.dev),
            features(Labels.docs)]

data = pd.concat(features)

languages_list = data['languages_str']

vectorizer = CountVectorizer(analyzer="word",
                             #stop_words=['docs', 'framework', 'homework', 'course', 'data'],
                             ngram_range=(1, 3)
                             ,max_features = 1000
                             )


train_data_features = vectorizer.fit_transform(languages_list)
train_data_features = train_data_features.toarray()


labels = data['label']


X = vectorizer.fit_transform(languages_list)
print X.shape


Y = np.asarray(labels,dtype=int)
print Y.shape

X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.2,random_state=0)

C_range = np.logspace(-2, 10, 13)
gamma_range = np.logspace(-9, 3, 13)
gS = GridSearchCV(SVC(),{'kernel':['rbf'],'C':C_range,'gamma':gamma_range},n_jobs=-1)
clf = RandomForestClassifier(n_estimators=1000,n_jobs=-1,random_state=0, max_depth=30)
# gS.fit(X_train,Y_train)
clf.fit(X_train,Y_train)
print clf.score(X_test,Y_test)


