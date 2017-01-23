import os
import re

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.model_selection import ShuffleSplit
from sklearn.externals import joblib

from config.constants import INPUT_KS
from config.helper import Helper
from settings import STOPWORDS_PATH
from settings import MODEL_PATH

CONTENT_FEATURE_NAME = "fo_and_fi_names"
README_FILE_NAME = "readme_filename"
REPOSITORY_NAME = "repo_name"

STOPWORDS_LANGUAGE = "english"

PICKLE_FILE_NAME = "keyword_spotting.pkl"

class KeywordSpotting():
    def __init__(self, is_train, seed):
        self.build_keyword_lists()
        self.is_train = is_train
        self.seed = seed
        self.input_type = INPUT_KS
        self.clf = RandomForestClassifier(n_estimators=500, n_jobs=-1, random_state=1, max_depth=20)

    def readmeContent(self, filename):
        f = open(filename, 'r')
        return f.read()

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

    def build_keyword_lists(self):
        keywords_readme_edu = ["course", "coursera", "slide", "lecture", "assignment", "university", "student", "week",
                               "schedule",
                               "work", "term", "education", "class", "condition"]
        keywords_readme_dev = ["library", "package", "framework", "module", "app", "application", "server", "license",
                               "develop",
                               "dependencies", "installation", "api", "client", "build", "release", "version", "script"]
        keywords_readme_data = ["data", "dataset", "sample", "set", "database", "lesson"]
        keywords_readme_hw = ["homework", "solution", "deadline", "problem", "definition"]
        keywords_readme_web = ["web", "website", "homepage", "javascript", "template"]
        keywords_readme_doc = ["documentation", "collection", "manuals", "docs"]

        keyword_readme_list = []
        keyword_readme_list.extend(keywords_readme_edu)
        keyword_readme_list.extend(keywords_readme_dev)
        keyword_readme_list.extend(keywords_readme_data)
        keyword_readme_list.extend(keywords_readme_hw)
        keyword_readme_list.extend(keywords_readme_web)
        keyword_readme_list.extend(keywords_readme_doc)

        keywords_content_edu = ["course", "slide", "lecture", "assignment", "education"]
        keywords_content_dev = ["scripts", "pom.xml", "framework", "install", "test", "bin", "src", "app", "plugin", "js"]
        keywords_content_data = ["dataset", "csv", "pdf", "html"]
        keywords_content_hw = ["homework", "hw0", "hw1", "task", "lesson", "week_"]
        keywords_content_web = ["website", "css", "img", "images"]
        keywords_content_doc = ["doc"]

        keyword_content_list = []
        keyword_content_list.extend(keywords_content_edu)
        keyword_content_list.extend(keywords_content_dev)
        keyword_content_list.extend(keywords_content_data)
        keyword_content_list.extend(keywords_content_hw)
        keyword_content_list.extend(keywords_content_web)
        keyword_content_list.extend(keywords_content_doc)


        self.keyword_readme_list = keyword_readme_list
        self.keyword_content_list = keyword_content_list


    def row_to_words(self, row):
        if row[README_FILE_NAME] is not np.nan:
            if self.is_train:
                path = "../" + row[README_FILE_NAME]
            else:
                path = row[README_FILE_NAME]
            if not os.path.exists(path):
                print 'missing %s ' % path
            content = self.readmeContent(path)
            words = self.raw_to_words(content)
        else:
            words = None
        return words


    def write_to_csv(self, dataframe, filename="trash_data.txt"):
        dataframe.to_csv(filename, sep=",")

    def keyword_spotting(self, content, keyword_list):
        # init binary vector with zeros
        binary_vector = np.zeros(len(keyword_list))
        if content is not None:
            for index, key in enumerate(keyword_list):
                word_set = content.split(" ")
                for word in word_set:
                    if key in word:
                        binary_vector[index] = 1
        return binary_vector

    def extract_readme_features(self, clean_readmes, keyword_list):
        readme_features = []

        for repository_readme in clean_readmes:
            keys = self.keyword_spotting(repository_readme, keyword_list=keyword_list)
            readme_features.append(keys)

        return readme_features

    def extract_content_features(self, contents, keyword_list):
        content_features = []

        for repository_content in contents[CONTENT_FEATURE_NAME]:
            if repository_content is np.nan:
                repository_content = None
            keys = self.keyword_spotting(repository_content, keyword_list=keyword_list)
            content_features.append(keys)

        return content_features

    def build_keyword_features(self, slice_data):
        data = pd.DataFrame(data=slice_data)

        data['readme_words'] = data.apply(lambda row: self.row_to_words(row), axis=1)
        clean_readmes = data['readme_words'].tolist()

        readme_features = self.extract_readme_features(clean_readmes, self.keyword_readme_list)
        content_features = self.extract_content_features(data, self.keyword_content_list)

        X = np.hstack((readme_features, content_features))
        return X

    def build_labels(self, slice_data):
        data = pd.DataFrame(data=slice_data)
        labels = data['label']

        Y = np.asarray(labels, dtype=int)
        return Y


    def train(self, dataframe):
        X, Y = self.build_keyword_features(dataframe), self.build_labels(dataframe)
        self.clf.fit(X, Y)

    def evaluate(self, dataframe):

        X, Y = self.build_keyword_features(dataframe), self.build_labels(dataframe)
        output = self.clf.predict(X)
        # score = precision_score(Y, output, average=None)
        # print "PRECISION SCORE: "
        # print score
        # print np.mean(score)

        score = f1_score(Y, output, average=None)
        print "\nEvaluating %s BaseClassifier" % self.input_type
        print "F1 SCORE: "
        print score
        print np.mean(score)
        return score, np.mean(score), self.input_type, self.seed

    def train_and_evaluate(self, dataframe, num_iterations=3, test_size=0.3):
        X, Y = self.build_keyword_features(dataframe), self.build_labels(dataframe)
        iteration = 0
        average_test_precision = 0
        ss = ShuffleSplit(n_splits=num_iterations, test_size=test_size, random_state=0)
        for train_index, test_index in ss.split(X):
            X_train, X_test, Y_train, Y_test = X[train_index], X[test_index], Y[train_index], Y[test_index]

            clf = RandomForestClassifier(n_estimators=500, n_jobs=-1, random_state=1, max_depth=20)
            clf.fit(X_train, Y_train)

            print "PRECISION SCORES ITERATION " + str(iteration) + ": "
            output = clf.predict(X_test)
            score = precision_score(Y_test, output, average=None)
            print score
            print np.mean(score)
            average_test_precision += score
            print clf.score(X_test, Y_test)

            iteration += 1

        average_test_precision /= iteration
        print "AVERAGE TEST PRECISION OVER " + str(iteration) + " ITERATIONS: "
        print average_test_precision

    def predict(self, dataframe):
        X = self.build_keyword_features(dataframe)
        return self.clf.predict(X)

    def write_proba(self, dataframe_train, dataframe_test):
        X_train, Y_train = self.build_keyword_features(dataframe_train), self.build_labels(dataframe_train)
        X_test, Y_test = self.build_keyword_features(dataframe_test), self.build_labels(dataframe_test)

        Helper().write_probabilities(self.clf, X_train, dataframe_train['repo_name'], dataframe_train['label'], 'prob/prob_keyword_train')
        Helper().write_probabilities(self.clf, X_test, dataframe_test['repo_name'], dataframe_test['label'], 'prob/prob_keyword_test')

    def predict_proba(self, dataframe):
        X = self.build_keyword_features(dataframe)
        return self.clf.predict_proba(X)

    def predict_log_proba(self, dataframe):
        X = self.build_keyword_features(dataframe)
        return self.clf.predict_log_proba(X)

    def save_model(self):
        joblib.dump(self.clf, MODEL_PATH + PICKLE_FILE_NAME, compress=3)
        print "Successfully saved keyword spotting model!"

    def load_model(self):
        self.clf = joblib.load(MODEL_PATH + PICKLE_FILE_NAME)
        print "Successfully loaded keyword spotting model!"
