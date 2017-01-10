import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.svm import SVC

from collection.labels import Labels


def features(label):
    features = pd.read_csv("../../exploration/labelled/features/languages_data_%s.txt" % label.value, delimiter=" ",
                           header=0)

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


features = [features(Labels.edu), features(Labels.data), features(Labels.hw), features(Labels.web), features(Labels.dev),
        features(Labels.docs)]

data = pd.concat(features)

linear_svc = LinearSVC()

rbf_svc = SVC(kernel='rbf')

# sample 100 times and get average performance scores
linear_svc_precision_sum = 0
linear_svc_accuracy_sum = 0

rbf_svc_precision_sum = 0
rbf_svc_accuracy_sum = 0

sample_runs = 100
for i in range(sample_runs):
    labels = data['label']
    trimmed_data = data.drop(labels='label', axis=1)

    x_train, x_test, y_train, y_test = train_test_split(trimmed_data, labels, random_state=0)

    linear_svc.fit(x_train, y_train)
    rbf_svc.fit(x_train, y_train)

    y_pred_linear = linear_svc.predict(x_test)
    y_pred_rbf = rbf_svc.predict(x_test)

    linear_svc_precision = precision_score(y_test, y_pred_linear, average='micro')
    linear_svc_precision_sum += linear_svc_precision * 100
    rbf_svc_precision = precision_score(y_test, y_pred_rbf, average='micro')
    rbf_svc_precision_sum += rbf_svc_precision * 100

    linear_svc_accuracy = accuracy_score(y_test, y_pred_linear)
    linear_svc_accuracy_sum += linear_svc_accuracy * 100
    rbf_svc_accuracy = accuracy_score(y_test, y_pred_rbf)
    rbf_svc_accuracy_sum += rbf_svc_accuracy * 100

linear_svc_accuracy_average = linear_svc_accuracy_sum / sample_runs
linear_svc_precision_average = linear_svc_precision_sum / sample_runs

rbf_svc_accuracy_average = rbf_svc_accuracy_sum / sample_runs
rbf_svc_precision_average = rbf_svc_precision_sum / sample_runs

print "Linear SVC: average accuracy and precision"
print linear_svc_accuracy_average
print linear_svc_precision_average

print "rbf SVC: average accuracy and precision"
print rbf_svc_accuracy_average
print rbf_svc_precision_average
