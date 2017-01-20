import os
import re

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import nltk
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score
from sklearn.model_selection import ShuffleSplit
from sklearn.externals import joblib

from collection.labels import Labels


CONTENT_FEATURE_NAME = "fo_and_fi_names"
README_FILE_NAME = "readme_filename"
REPOSITORY_NAME = "repo_name"

PICKLE_FILE_PATH = "keyword_spotting.pkl"

readmes = pd.read_csv("../../exploration/text_data.txt", delimiter=" ", header=0)

# Download stopwords corpus
class KeywordSpotting():
    def __init__(self):
        nltk.download('stopwords')
        self.build_keyword_lists()

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
        stops = set(nltk.corpus.stopwords.words("english"))

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

    def merge_readmes_and_contents(self, readmes, contents):

        data = readmes.merge(contents, on=REPOSITORY_NAME, how="inner")

        rows = data[REPOSITORY_NAME].size
        for i in xrange(0, rows):
            if (np.isnan(data["label_x"][i])):
                data.loc[i, "label_x"] = data["label_y"][i]
        return data

    def clean_readme_data(self, data):
        # all bullshit
        rows = data[REPOSITORY_NAME].size
        print rows
        clean_readmes = []
        for i in xrange(0, rows):
            # Call our function for each one, and add the result to the list of
            # clean reviews
            print i
            path_to_readme = data[README_FILE_NAME][i]
            if path_to_readme is not np.nan:
                # dirty fix readme path name
                path = "../" + path_to_readme
                if not os.path.exists(path):
                    raise IOError("Readme path does not exist!")
                content = self.readmeContent(path)
                clean_readmes.append(self.raw_to_words(content))
            else:
                clean_readmes.append(None)
        return clean_readmes

    def row_to_words(self, row):
        if row[README_FILE_NAME] is not np.nan:

            path = "../" + row[README_FILE_NAME]
            if not os.path.exists(path):
                print 'missing %s ' % path
            content = self.readmeContent(path)
            # print content
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
        print binary_vector
        return binary_vector

    def read_contents_data(self, label):
        features = pd.read_csv("../../exploration/labelled/features/contents_data_%s.txt" % label, delimiter=" ", header=0)

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

    def extract_all_contents(self):
        data = [self.read_contents_data(Labels.data), self.read_contents_data(Labels.dev), self.read_contents_data(Labels.docs), self.read_contents_data(Labels.edu),
                    self.read_contents_data(Labels.hw), self.read_contents_data(Labels.web), self.read_contents_data(Labels.uncertain)]
        data = pd.concat(data)
        return data

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

    def build_x_and_y(self, data):

        print "SHAPE BEFORE ALL: ", np.shape(data)
        data['readme_words'] = data.apply(lambda row: self.row_to_words(row), axis=1)

        clean_readmes = data['readme_words'].tolist()
        print "SHAPE OF CLEAN READMES :", np.shape(clean_readmes)
        readme_features = self.extract_readme_features(clean_readmes, self.keyword_readme_list)
        content_features = self.extract_content_features(data, self.keyword_content_list)

        print "Shape readme features: ", np.shape(readme_features)
        print "Shape content features: ", np.shape(content_features)

        X = np.hstack((readme_features, content_features))

        labels = data['label']

        Y = np.asarray(labels, dtype=int)
        print "Shape of stacked features:", np.shape(X)
        print "Shape labels: ", np.shape(Y)
        # print labels
        return X, Y


    def train(self, dataframe):

        X, Y = self.build_x_and_y(dataframe)

        self.clf.fit(X, Y)

    def evaluate(self, dataframe):

        X, Y = self.build_x_and_y(dataframe)
        output = self.clf.predict(X)
        score = precision_score(Y, output, average=None)
        print "PRECISION SCORE: "
        print score
        print np.mean(score)

    def train_and_evaluate(self, dataframe, num_iterations=3, test_size=0.3):
        X, Y = self.build_x_and_y(dataframe)
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

    def predict(self, X):
        return self.clf.predict(X)

    def predict_proba(self, X):
        return self.clf.predict_proba(X)

    def predict_log_proba(self, X):
        return self.clf.predict_log_proba(X)

    def save_classifier(self):
        joblib.dump(self.clf, PICKLE_FILE_PATH, compress=3)
        return

    def load_classifier(self):
        self.clf = joblib.load(PICKLE_FILE_PATH)

if __name__ == '__main__':
    spotting = KeywordSpotting()
    spotting.train_and_evaluate()