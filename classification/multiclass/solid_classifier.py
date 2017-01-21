import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import ShuffleSplit
from sklearn.metrics import accuracy_score, precision_score, recall_score, mean_squared_error
from sklearn.externals import joblib

from config.constants import *
from config.helper import Helper
from keyword_spotting import KeywordSpotting
from settings import MODEL_PATH

REPO = "repo"
CI = "commits_interval"
LANG = "languages"
COMMIT = "commit"
README = "readme"
CONTENTS = "contents"
TREES = "trees"

PICKLE_MODEL_NAME = "solid_classifier_model.pkl"

class SolidClassifier():
    
    def __init__(self):
        self.clf = RandomForestClassifier(n_estimators=5000, max_depth=30)
        self.folder_path_data = None

    
    def language_feature_hack(self, aligned_data):
        """hack to get language features names by excluding all the other feature names"""
        LANGUAGE_FEATURES = list(aligned_data.columns.values)
        self.LANGUAGE_FEATURES = [label for label in LANGUAGE_FEATURES
                                  if label not in REPO_FEATURES
                                  and label not in CI_FEATURES
                                  and label not in COMMIT_FEATURES
                                  and label not in ['label', 'repo_name']
                                  and label not in README_FEATURES
                                  and label not in TREE_FEATURES
                                  and label not in CONTENT_FEATURES]

    def build_labels(self, dataframe):
        Y = dataframe['label']
        return Y


    def build_features(self, dataframe):
        self.language_feature_hack(dataframe)
        data = pd.DataFrame(data=dataframe)
        data_raw_features = data[REPO_FEATURES + COMMIT_FEATURES + self.LANGUAGE_FEATURES + CI_FEATURES]
        data_keywords_features = data[["repo_name"] + README_FEATURES + CONTENT_FEATURES]
        # data_keywords_features = data[["repo_name"] + README_FEATURES + CONTENT_FEATURES + ["label"]]

        keyword_spotting = KeywordSpotting()
        data_keywords = keyword_spotting.build_keyword_features(data_keywords_features)

        print np.shape(data_raw_features)
        print np.shape(data_keywords)

        combined_data = np.column_stack((data_raw_features, data_keywords))
        return combined_data

    def train(self, data):
        X, Y = self.build_features(data), self.build_labels(data)
        self.clf.fit(X, Y)

    def evaluate(self, dataframe):
        X, Y = self.build_features(dataframe), self.build_labels(dataframe)
        output = self.clf.predict(X)
        score = precision_score(Y, output, average=None)
        print "PRECISION SCORE: "
        print score
        print np.mean(score)

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
        X = self.build_features(dataframe)
        return self.clf.predict(X)

    def write_proba(self, dataframe_train, dataframe_test):
        X_train, Y_train = self.build_features(dataframe_train), self.build_labels(dataframe_train)
        X_test, Y_test = self.build_features(dataframe_test), self.build_labels(dataframe_test)

        Helper().write_probabilities(self.clf, X_train, dataframe_train['repo_name'], dataframe_train['label'], 'prob/prob_keyword_train')
        Helper().write_probabilities(self.clf, X_test, dataframe_test['repo_name'], dataframe_test['label'], 'prob/prob_keyword_test')

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

if __name__ == '__main__':
    clf = SolidClassifier()
    clf.train()