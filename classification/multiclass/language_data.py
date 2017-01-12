import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import mean_squared_error
from sklearn.metrics import precision_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

from collection.labels import Labels


def features(label):
    features = pd.read_csv("../../exploration/labelled/features/languages_data_%s.txt" % label.value, delimiter=" ",
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


def compare_performance_scores(linear_svc, rbf_svc, data):
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


def tune_rbf_svc_hyperparameters(rbf_svc, data):
    """
    Search the hyper-parameter space for the best classifier performance based on the cross-validation score

    http://scikit-learn.org/stable/modules/cross_validation.html#cross-validation

    http://scikit-learn.org/stable/auto_examples/model_selection/grid_search_digits.html#sphx-glr-auto-examples-model-selection-grid-search-digits-py
    :param rbf_svc:
    :param data:
    """
    labels = data['label']
    trimmed_data = data.drop(labels='label', axis=1)

    x_train, x_test, y_train, y_test = train_test_split(trimmed_data, labels, random_state=0)

    # http: // scikit - learn.org / stable / auto_examples / model_selection / grid_search_digits.html  # sphx-glr-auto-examples-model-selection-grid-search-digits-py
    # Set the parameters by cross-validation ?
    C_range = np.logspace(-2, 10, 13)
    gamma_range = np.logspace(-9, 3, 13)

    tuned_parameters = [{'kernel': ['rbf'], 'gamma': gamma_range,
                         'C': C_range}]

    clf = GridSearchCV(rbf_svc, tuned_parameters, scoring='precision_macro', n_jobs=-1)
    clf.fit(x_train, y_train)
    print("Best parameters set found on development set:")
    print()
    print(clf.best_params_)
    print()
    print("Grid scores on development set:")
    print()
    means = clf.cv_results_['mean_test_score']
    stds = clf.cv_results_['std_test_score']
    for mean, std, params in zip(means, stds, clf.cv_results_['params']):
        print("%0.3f (+/-%0.03f) for %r"
              % (mean, std * 2, params))
    print()

    print("Detailed classification report:")
    print()
    print("The model is trained on the full development set.")
    print("The scores are computed on the full evaluation set.")
    print()
    y_true, y_pred = y_test, clf.predict(x_test)
    print(classification_report(y_true, y_pred))
    print()


    #
    #     cv_count = 5
    #    C_range = [1e-2, 1, 1e2]
    #  gamma_range = [1e-1, 1, 1e1]

    # # use 'score' method of the estimator OR
    # # specify parameter scoring = '...' http://scikit-learn.org/stable/modules/model_evaluation.html#scoring-parameter
    # scores = cross_val_score(estimator=rbf_svc, X=trimmed_data, y=labels, cv=cv_count)
    #
    #
    # # compare with previous score
    #
    # print scores


features = [features(Labels.edu), features(Labels.data), features(Labels.hw), features(Labels.web),
            features(Labels.dev),
            features(Labels.docs)]

data = pd.concat(features)

train_data, test_data = train_test_split(data, test_size=0.2)

train_labels = train_data['label']
test_labels = test_data['label']

train_data = train_data.drop(labels='label', axis=1)
test_data = test_data.drop(labels='label', axis=1)

forest_classifier = RandomForestClassifier(n_estimators=500, max_depth=5)
forest = forest_classifier.fit(train_data, train_labels)

output = forest.predict(test_data)

print mean_squared_error(output, test_labels)
print accuracy_score(test_labels, output)
print precision_score(test_labels, output, average=None)



# linear_svc = LinearSVC()
# rbf_svc = SVC(kernel='rbf')

# compare_performance_scores(linear_svc=linear_svc, rbf_svc=rbf_svc, data=data)
# tune_rbf_svc_hyperparameters(rbf_svc, data)

# rbf_svc = SVC(kernel='rbf', C=1, gamma=0.01)
# compare_performance_scores(linear_svc=linear_svc, rbf_svc=rbf_svc, data=data)
