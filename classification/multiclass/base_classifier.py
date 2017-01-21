import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.metrics import precision_score
from config.constants import *

MODEL_LOCATION = '../../models/'


class BaseClassifier():
    def __init__(self, input):
        if input not in [INPUT_COMMIT, INPUT_LANGUAGE, INPUT_REPO, INPUT_PUNCH]:
            raise ValueError("Mind your input! Base classifier does not handle this kind of input.")

        self.input_type = input
        self.clf = RandomForestClassifier(n_estimators=5000, random_state=1, max_depth=30)

    def train(self, train_data):
        """
        Trains the classifier on the slice corresponding to the input features of interest.

        :param train_data: pandas dataframe with all features, including 'repo_name' and 'label'
        """
        X = self.select_features(train_data)
        Y = train_data['label']

        self.clf.fit(X=X, y=Y)

    def evaluate(self, test_data):
        """
        Evaluates current classifier on the slice corresponding to the input features of interest.

        :param test_data: pandas dataframe with all features, including 'repo_name' and 'label'
        """
        X = self.select_features(test_data)
        Y = test_data['label']

        output = self.clf.predict(X)

        score = precision_score(Y, output, average=None)
        print "\nEvaluating %s BaseClassifier" % self.input_type
        print "PRECISION SCORE: "
        print score
        print np.mean(score)

    def select_features(self, data):
        """
        Slices input dataframe to columns corresponding to features of interest

        :param data: pandas dataframe with all features, including 'repo_name' and 'label'; can be train or test data
        """
        if self.input_type == INPUT_COMMIT:
            return data[COMMIT_FEATURES]
        elif self.input_type == INPUT_REPO:
            return data[REPO_FEATURES]
        # elif self.input_type == INPUT_LANGUAGE:
        #     return data[LANGUAGE_FEATURES]
        # elif self.input == INPUT_PUNCH:
        #     slice_data = training_data[PUNCH_CARD_FEATURES]
        elif self.input_type == INPUT_ALL:
            return data[REPO_FEATURES + COMMIT_FEATURES] #+ LANGUAGE_FEATURES]
        else:
            raise Exception("BaseClassifier select_features() - invalid state.")

    def save_model(self):
        """
        Saves trained model to file.
        """
        joblib.dump(self.clf, self.build_model_filename(), compress=3)
        print "Successfully saved BaseClassifier!"

    def load_model(self):
        """
        Loads trained model from file.
        """
        self.clf = joblib.load(self.build_model_filename())
        print "Successfully loaded BaseClassifier!"

    def build_model_filename(self):
        return MODEL_LOCATION + self.input_type + ".pkl"
