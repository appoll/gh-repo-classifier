import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.svm import SVC

from src.collection import Labels


def features(label):
    features = pd.read_csv("../../exploration/labelled/features/languages_data_%s.txt" % label, delimiter=" ",
                           header=0)

    features = features.drop(labels='repo_name', axis=1)

    if label == Labels.dev:
        features['label'] = 1
    else:
        features['label'] = 0
    return features


positives = features(Labels.dev)

negatives = [features(Labels.edu), features(Labels.data), features(Labels.hw), features(Labels.web),
             features(Labels.docs)]
negatives = pd.concat(negatives)

linear_svc = LinearSVC()

rbf_svc = SVC(kernel='rbf')

# sample 100 times and get average performance scores
linear_svc_precision_sum = 0
linear_svc_accuracy_sum = 0

rbf_svc_precision_sum = 0
rbf_svc_accuracy_sum = 0

sample_runs = 50
for i in range(sample_runs):
    neg = negatives.sample(n=positives.shape[0])
    data = [positives, neg]
    data = pd.concat(data)

    labels = data['label']
    data = data.drop(labels='label', axis=1)

    x_train, x_test, y_train, y_test = train_test_split(data, labels, random_state=0)

    linear_svc.fit(x_train, y_train)
    rbf_svc.fit(x_train, y_train)

    y_pred_linear = linear_svc.predict(x_test)
    y_pred_rbf = rbf_svc.predict(x_test)

    linear_svc_precision = precision_score(y_test, y_pred_linear)
    linear_svc_precision_sum += linear_svc_precision * 100
    rbf_svc_precision = precision_score(y_test, y_pred_rbf)
    rbf_svc_precision_sum += rbf_svc_precision * 100

    linear_svc_accuracy = accuracy_score(y_test, y_pred_linear)
    linear_svc_accuracy_sum += linear_svc_accuracy * 100
    rbf_svc_accuracy = accuracy_score(y_test, y_pred_rbf)
    rbf_svc_accuracy_sum += rbf_svc_accuracy * 100

    # # same as accuracy_score
    # linear_svc_score = linear_svc.score(x_test, y_test)
    # print linear_svc_score

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