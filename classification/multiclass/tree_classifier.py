import re

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import precision_score

from config.constants import TREE_FEATURES
from config.helper import Helper

MODEL_LOCATION = '../../models/'


class TreeClassifier():
    def __init__(self):
        self.clf = RandomForestClassifier(n_estimators=1000)
        self.cV = CountVectorizer(ngram_range=(1,4),max_features=200, binary=True)

    def train(self, train_data):
        """
        Trains the classifier on the slice corresponding to the tree features.

        :param train_data: pandas dataframe with all features, including 'repo_name' and 'label'
        """
        Y = train_data['label']

        train_data_trees = pd.DataFrame(data=self.select_features(train_data))
        train_data_trees['blob_paths_updated'] = train_data_trees.apply(lambda row: self.row_to_words(row), axis=1)

        # fit only the training data
        self.cV.fit(train_data_trees['blob_paths_updated'])
        # transform both training and test data
        x_train = self.cV.transform(train_data_trees['blob_paths_updated'])


        self.clf.fit(X=x_train, y=Y)

    def evaluate(self, test_data):
        """
        Evaluates current classifier on the slice corresponding to the input features of interest.

        :param test_data: pandas dataframe with all features, including 'repo_name' and 'label'
        """
        Y = test_data['label']

        test_data_trees = pd.DataFrame(data=self.select_features(test_data))
        test_data_trees['blob_paths_updated'] = test_data_trees.apply(lambda row: self.row_to_words(row), axis=1)
        x_test = self.cV.transform(test_data_trees['blob_paths_updated'])

        output = self.clf.predict(x_test)

        score = precision_score(Y, output, average=None)
        print "\nEvaluating TreeClassifier"
        print "PRECISION SCORE: "
        print score
        print np.mean(score)

    def select_features(self, data):
        """
        Slices input dataframe to columns corresponding to features of interest

        :param data: pandas dataframe with all features, including 'repo_name' and 'label'; can be train or test data
        """
        return data[TREE_FEATURES]

    def save_model(self):
        """
        Saves trained model to file.
        """
        joblib.dump(self.clf, self.build_model_filename(), compress=3)
        print "Successfully saved TreeClassifier!"

    def load_model(self):
        """
        Loads trained model from file.
        """
        self.clf = joblib.load(self.build_model_filename())
        print "Successfully loaded TreeClassifier!"

    def build_model_filename(self):
        return MODEL_LOCATION + 'tree_clf' + ".pkl"

    def write_probabilities(self, train_data, test_data):
        """
        Writes log probabilities to file. To be called only with a fitted model.
        :param train_data: unsliced train data, including 'repo_name' and 'label'
        :param test_data: unsliced test data, including 'repo_name' and 'label'
        """
        train_data_trees = pd.DataFrame(data=self.select_features(train_data))
        train_data_trees['blob_paths_updated'] = train_data_trees.apply(lambda row: self.row_to_words(row), axis=1)
        x_train = self.cV.transform(train_data_trees['blob_paths_updated'])
        train_repo_names = train_data['repo_name']
        train_labels = train_data['label']

        Helper().write_probabilities(self.clf, x_train, train_repo_names, train_labels, 'prob/prob_%s_train' % 'trees')

        test_data_trees = pd.DataFrame(data=self.select_features(test_data))
        test_data_trees['blob_paths_updated'] = test_data_trees.apply(lambda row: self.row_to_words(row), axis=1)
        x_test = self.cV.transform(test_data_trees['blob_paths_updated'])

        test_repo_names = test_data['repo_name']
        test_labels = test_data['label']
        Helper().write_probabilities(self.clf, x_test, test_repo_names, test_labels, 'prob/prob_%s_test' % 'trees')

    def row_to_words(self, row):
        blob_paths = row['blob_paths']
        content = self.cleanString(blob_paths)
        return content

    def cleanString(self, s):
        p = re.compile('(?<=[a-z])(?=[A-Z])')
        newS = p.sub(r' ', s)
        newS = re.sub('[0-9]+', ' NN ', newS)
        newS = re.sub('[^a-zA-Z]', ' ', newS)
        newS = re.sub('\W+', ' ', newS)
        return newS.strip().lower()
