import os
import re

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score

from config.constants import *
from config.helper import Helper
from settings import STOPWORDS_PATH, MODEL_PATH

STOPWORDS_LANGUAGE = "english"


class ReadmeClassifier():
    def __init__(self, seed):
        self.clf = RandomForestClassifier(n_estimators=1000, max_depth=30, random_state=seed)

        self.vectorizer = TfidfVectorizer(analyzer="word",
                                          tokenizer=None,
                                          preprocessor=None,
                                          ngram_range=(1, 3),
                                          max_features=2000
                                          )
        self.seed = seed
        self.input_type = README_CLF

    def train(self, train_data):
        """
        Trains the classifier on the slice corresponding to the readme features.

        :param train_data: pandas dataframe with all features, including 'repo_name' and 'label'
        """
        Y = train_data['label']

        train_data_readmes = pd.DataFrame(data=self.select_features(train_data))
        train_data_readmes['clean_readmes'] = train_data_readmes.apply(lambda row: self.row_to_words(row), axis=1)

        # fit only the training data
        self.vectorizer.fit(train_data_readmes['clean_readmes'])
        # transform both training and test data
        x_train = self.vectorizer.transform(train_data_readmes['clean_readmes'])

        self.clf.fit(X=x_train, y=Y)

    def evaluate(self, test_data):
        """
        Evaluates current classifier on the slice corresponding to the input features of interest.

        :param test_data: pandas dataframe with all features, including 'repo_name' and 'label'
        """
        Y = test_data['label']

        test_data_trees = pd.DataFrame(data=self.select_features(test_data))
        test_data_trees['clean_readmes'] = test_data_trees.apply(lambda row: self.row_to_words(row), axis=1)
        x_test = self.vectorizer.transform(test_data_trees['clean_readmes'])

        output = self.clf.predict(x_test)

        # score = precision_score(Y, output, average=None)
        # print "\nEvaluating ReadmeClassifier"
        # print "PRECISION SCORE: "
        # print score
        # print np.mean(score)
        score = f1_score(Y, output, average=None)
        print "\nEvaluating %s ReadmeClassifier" % self.input_type
        print "F1 SCORE: "
        print score
        print np.mean(score)
        return score, np.mean(score), self.input_type, self.seed

    def select_features(self, data):
        """
        Slices input dataframe to columns corresponding to features of interest

        :param data: pandas dataframe with all features, including 'repo_name' and 'label'; can be train or test data
        """
        return data[README_FEATURES]

    def save_model(self):
        """
        Saves trained model to file.
        """
        joblib.dump(self.clf, self.build_model_filename(), compress=3)
        joblib.dump(self.vectorizer, self.build_vectorizer_filename(), compress = 3)
        print "Successfully saved ReadmeClassifier!"

    def load_model(self):
        """
        Loads trained model from file.
        """
        self.clf = joblib.load(self.build_model_filename())
        self.vectorizer = joblib.load(self.build_vectorizer_filename())
        print "Successfully loaded ReadmeClassifier!"

    def build_model_filename(self):
        return MODEL_PATH + 'readme_clf' + ".pkl"

    def build_vectorizer_filename(self):
        return MODEL_PATH + 'readme_clf_vectorizer' + ".pkl"

    def write_probabilities(self, train_data, test_data):
        """
        Writes log probabilities to file. To be called only with a fitted model.
        :param train_data: unsliced train data, including 'repo_name' and 'label'
        :param test_data: unsliced test data, including 'repo_name' and 'label'
        """
        train_data_trees = pd.DataFrame(data=self.select_features(train_data))
        train_data_trees['clean_readmes'] = train_data_trees.apply(lambda row: self.row_to_words(row), axis=1)
        x_train = self.vectorizer.transform(train_data_trees['clean_readmes'])
        train_repo_names = train_data['repo_name']
        train_labels = train_data['label']

        Helper().write_probabilities(self.clf, x_train, train_repo_names, train_labels,
                                     'prob/prob_%s_train' % 'readmes')

        test_data_trees = pd.DataFrame(data=self.select_features(test_data))
        test_data_trees['clean_readmes'] = test_data_trees.apply(lambda row: self.row_to_words(row), axis=1)
        x_test = self.vectorizer.transform(test_data_trees['clean_readmes'])

        test_repo_names = test_data['repo_name']
        test_labels = test_data['label']
        Helper().write_probabilities(self.clf, x_test, test_repo_names, test_labels, 'prob/prob_%s_test' % 'readmes')

    def get_train_prob(self, train_data):
        """
        Writes log probabilities to file. To be called only with a fitted model.
        :param train_data: unsliced train data, including 'repo_name' and 'label'
        :param test_data: unsliced test data, including 'repo_name' and 'label'
        """
        train_data_trees = pd.DataFrame(data=self.select_features(train_data))
        train_data_trees['clean_readmes'] = train_data_trees.apply(lambda row: self.row_to_words(row), axis=1)
        x_train = self.vectorizer.transform(train_data_trees['clean_readmes'])

        return self.clf.predict_log_proba(x_train)

    def get_test_prob(self, test_data):
        test_data_trees = pd.DataFrame(data=self.select_features(test_data))
        test_data_trees['clean_readmes'] = test_data_trees.apply(lambda row: self.row_to_words(row), axis=1)
        x_test = self.vectorizer.transform(test_data_trees['clean_readmes'])

        # test_repo_names = test_data['repo_name']
        # test_labels = test_data['label']
        return self.clf.predict_log_proba(x_test)

    def row_to_words(self, row):
        if row['readme_filename'] is not np.nan:
            path = "../" + row['readme_filename']
            if not os.path.exists(path):
                print 'missing %s ' % path
            content = self.readmeContent(path)
            words = self.raw_to_words(content)
        else:
            words = ""

        return words

    def raw_to_words(self, content):
        """
        https://www.kaggle.com/c/word2vec-nlp-tutorial/details/part-1-for-beginners-bag-of-words
        Method for performing text preprocessing
        :param content: the raw content of the markdown readme file
        """
        # Remove HTML Markup
        text = BeautifulSoup(content, 'lxml').getText()

        # Remove non - letters ??
        text = re.sub("[^a-zA-Z]", " ", text)

        # Convert to lower case, split into individual words
        words = text.lower().split()

        # 4. In Python, searching a set is much faster than searching
        #   a list, so convert the stop words to a set
        stops = set(STOPWORDS_PATH + STOPWORDS_LANGUAGE)
        # 5. Remove stop words
        meaningful_words = [w for w in words if not w in stops]
        return (" ".join(meaningful_words))

    def readmeContent(self, filename):
        f = open(filename, 'r')
        return f.read()
