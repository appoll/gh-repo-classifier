import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score, recall_score
from sklearn.model_selection import ShuffleSplit

from collection.labels import Labels
from config.constants import *
from config.helper import Helper
from keyword_spotting import KeywordSpotting
from settings import MODEL_PATH, LANGUAGE_FEATURES_NAME_PATH

REPO = "repo"
CI = "commits_interval"
LANG = "languages"
COMMIT = "commit"
README = "readme"
CONTENTS = "contents"
TREES = "trees"

PICKLE_MODEL_NAME = "solid_classifier_model.pkl"


class SolidClassifier():
    def __init__(self, is_train):
        self.clf = RandomForestClassifier(n_estimators=5000, max_depth=30)
        self.folder_path_data = None
        self.is_train = is_train

    def build_labels(self, dataframe):
        Y = dataframe['label']
        return Y

    def build_features(self, dataframe):
        data = pd.DataFrame(data=dataframe)
        self.LANGUAGE_FEATURES = joblib.load(LANGUAGE_FEATURES_NAME_PATH + LANGUAGE_FEATURES_NAME_FILE)
        data_raw_features = data[REPO_FEATURES + COMMIT_FEATURES + self.LANGUAGE_FEATURES + CI_FEATURES]
        data_keywords_features = data[["repo_name"] + README_FEATURES + CONTENT_FEATURES]

        keyword_spotting = KeywordSpotting(self.is_train)
        data_keywords = keyword_spotting.build_keyword_features(data_keywords_features)

        # print np.shape(data_raw_features)
        # print np.shape(data_keywords)

        combined_data = np.column_stack((data_raw_features, data_keywords))
        return combined_data

    def train(self, data):
        X, Y = self.build_features(data), self.build_labels(data)
        self.clf.fit(X, Y)

    def evaluate(self, dataframe):
        X, Y = self.build_features(dataframe), self.build_labels(dataframe)
        output = self.clf.predict(X)
        score = precision_score(Y, output, average=None)
        recall = recall_score(Y, output, average=None)
        f1 = f1_score(Y, output, average='micro')
        print "PRECISION SCORE: "
        print score
        print np.mean(score)
        print "RECALL: "
        print recall
        print np.mean(recall)
        print "F1: "
        print f1
        print np.mean(f1)

    def train_and_evaluate(self, dataframe, num_iterations=3, test_size=0.3):
        X, Y = self.build_features(dataframe), self.build_labels(dataframe)
        iteration = 0
        average_test_precision = 0
        ss = ShuffleSplit(n_splits=num_iterations, test_size=test_size, random_state=0)
        for train_index, test_index in ss.split(X):
            X_train, X_test, Y_train, Y_test = X[train_index], X[test_index], Y[train_index], Y[test_index]

            self.clf.fit(X_train, Y_train)

            print "PRECISION SCORES ITERATION " + str(iteration) + ": "
            output = self.clf.predict(X_test)
            score = precision_score(Y_test, output, average=None)
            print score
            print np.mean(score)
            average_test_precision += score
            print self.clf.score(X_test, Y_test)

            iteration += 1

        average_test_precision /= iteration
        print "AVERAGE TEST PRECISION OVER " + str(iteration) + " ITERATIONS: "
        print average_test_precision

    def predict(self, dataframe):
        print 'predict method dataframe repo names'
        print dataframe['repo_name']
        X = self.build_features(dataframe)
        return self.clf.predict(X)

    def write_proba(self, dataframe_train, dataframe_test):
        X_train, Y_train = self.build_features(dataframe_train), self.build_labels(dataframe_train)
        X_test, Y_test = self.build_features(dataframe_test), self.build_labels(dataframe_test)

        Helper().write_probabilities(self.clf, X_train, dataframe_train['repo_name'], dataframe_train['label'],
                                     'prob/prob_keyword_train')
        Helper().write_probabilities(self.clf, X_test, dataframe_test['repo_name'], dataframe_test['label'],
                                     'prob/prob_keyword_test')

    def predict_proba(self, dataframe):
        X = self.build_features(dataframe)
        return self.clf.predict_proba(X)

    def predict_log_proba(self, dataframe):
        X = self.build_features(dataframe)
        return self.clf.predict_log_proba(X)

    def save_model(self):
        joblib.dump(self.clf, MODEL_PATH + PICKLE_MODEL_NAME, compress=9)
        print "Successfully saved solid classifier model!"

    def load_model(self):
        self.clf = joblib.load(MODEL_PATH + PICKLE_MODEL_NAME)
        print "Successfully loaded solid classifier model!"

    def confusion_matrix(self, y_test, y_pred):
        """
        Saves confusion matrix to file

        :param y_test: test labels
        :param y_pred: predicted labels
        """
        confusion_m = confusion_matrix(y_test, y_pred)

        Helper().plot_confusion_matrix(self.input_type, confusion_m, normalize=True, classes=Labels.toArray(),
                                       title='Confusion matrix for %s classifier' % self.input_type)
        Helper().plot_confusion_matrix(self.input_type, confusion_m, normalize=False, classes=Labels.toArray(),
                                       title='Confusion matrix for %s classifier' % self.input_type)
