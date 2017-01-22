import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score

from collection.labels import Labels
from config.constants import *
from config.helper import Helper

MODEL_LOCATION = '../../models/'


class BaseClassifier():
    def __init__(self, input):
        if input not in [INPUT_COMMIT, INPUT_LANGUAGE, INPUT_REPO, INPUT_PUNCH, INPUT_ALL]:
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

        self.confusion_matrix(Y, output)

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
        self.language_feature_hack(data)

        if self.input_type == INPUT_COMMIT:
            return data[COMMIT_FEATURES]
        elif self.input_type == INPUT_REPO:
            return data[REPO_FEATURES]
        elif self.input_type == INPUT_LANGUAGE:
            return data[self.LANGUAGE_FEATURES]
        # elif self.input == INPUT_PUNCH:
        #     slice_data = training_data[PUNCH_CARD_FEATURES]
        elif self.input_type == INPUT_ALL:
            return data[REPO_FEATURES + COMMIT_FEATURES + self.LANGUAGE_FEATURES]
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

    def write_probabilities(self, train_data, test_data):
        """
        Writes log probabilities to file
        :param train_data: unsliced train data, including 'repo_name' and 'label'
        :param test_data: unsliced test data, including 'repo_name' and 'label'
        """
        X = self.select_features(train_data)
        train_repo_names = train_data['repo_name']
        train_labels = train_data['label']
        Helper().write_probabilities(self.clf, X, train_repo_names, train_labels,
                                     'prob/prob_%s_train' % self.input_type)

        Y = self.select_features(test_data)
        test_repo_names = test_data['repo_name']
        test_labels = test_data['label']
        Helper().write_probabilities(self.clf, Y, test_repo_names, test_labels, 'prob/prob_%s_test' % self.input_type)

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
