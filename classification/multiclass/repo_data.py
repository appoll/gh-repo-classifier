import numpy as np
import pandas as pd
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from collection.labels import Labels


def get_features(label):
    features = pd.read_csv("../../exploration/labelled/features/repo_data_%s.txt" % label, delimiter=" ",
                           header=0)
    print("./exploration/labelled/features/repo_data_%s.txt" % label)
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


features = [get_features(Labels.data), get_features(Labels.dev), get_features(Labels.docs), get_features(Labels.edu),
            get_features(Labels.hw), get_features(Labels.web), get_features(Labels.uncertain)]

data = pd.concat(features)
repo_names = data['repo_name']
data = data.drop(labels='repo_name', axis=1)

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

svc_classifier = SVC(kernel="rbf", probability=True)
# C_range = np.logspace(-2, 10, 13)
# gamma_range = np.logspace(-9, 3, 13)
#
# tuned_parameters = [{'kernel': ['rbf'], 'gamma': gamma_range,
#                          'C': C_range}]
#
# svc_classifier = GridSearchCV(svc_classifier, tuned_parameters, scoring='precision_macro', n_jobs=-1)

svc = svc_classifier.fit(train_data, train_labels)

knn_classifier = KNeighborsClassifier(n_neighbors=8)
knn = knn_classifier.fit(train_data, train_labels)

gaussian_classifier = GaussianNB()
gaussian = gaussian_classifier.fit(train_data, train_labels)

logistic_regression_clf = LogisticRegression()
log_reg = logistic_regression_clf.fit(train_data, train_labels)

ada_boost_clf = AdaBoostClassifier()
ada_boost = ada_boost_clf.fit(train_data, train_labels)

voting_classifier = VotingClassifier(estimators=[('fc', forest), ('knn', knn), ('rbf', svc), ('gaussian', gaussian)],
                                     voting='soft')
voting = voting_classifier.fit(train_data, train_labels)

svc_output = svc.predict(test_data)
score = precision_score(test_labels, svc_output, average=None)
print '\nsvc'
print score
print np.mean(score)

knn_output = knn.predict(test_data)
score = precision_score(test_labels, knn_output, average=None)
print '\nknn'
print score
print np.mean(score)

forest_output = forest.predict(test_data)
score = precision_score(test_labels, forest_output, average=None)
print '\nforest'
print score
print np.mean(score)

gaussian_output = gaussian.predict(test_data)
score = precision_score(test_labels, gaussian_output, average=None)
print '\ngaussian'
print score
print np.mean(score)

log_reg_output = log_reg.predict(test_data)
score = precision_score(test_labels, log_reg_output, average=None)
print '\nlogistic regression'
print score
print np.mean(score)

ada_boost_output = ada_boost.predict(test_data)
score = precision_score(test_labels, ada_boost_output, average=None)
print '\nAda Boost'
print score
print np.mean(score)

output = voting.predict(test_data)
print '\nvoting'
print accuracy_score(test_labels, output)
score = precision_score(test_labels, output, average=None)
print score
print np.mean(score)

# Helper().write_probabilities(forest, data, repo_names, 'prob/prob_repo_data')