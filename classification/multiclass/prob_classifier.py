import numpy as np
from sklearn.externals import joblib
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.svm import SVC

from classification.multiclass.readme_classifier import ReadmeClassifier
from classification.multiclass.tree_classifier import TreeClassifier
from settings import MODEL_PATH


class ProbClassifier():
    def __init__(self, is_train):
        self.clf = SVC(C=0.111)
        self.is_train = is_train

        self.tree_clf = TreeClassifier()
        self.readme_clf = ReadmeClassifier()

        self.tree_clf.load_model()
        self.readme_clf.load_model()

    def train(self, train_data):
        Y = train_data['label']

        tree_prob_train = self.tree_clf.get_train_prob(train_data)

        readme_prob_train = self.readme_clf.get_train_prob(train_data)

        tree_prob_train[tree_prob_train == -np.inf] = -10
        readme_prob_train[readme_prob_train == -np.inf] = -10

        prob_train = np.hstack([tree_prob_train, readme_prob_train])
        prob_train = np.exp(prob_train)

        self.train_mean = np.mean(prob_train, axis=0)
        self.train_std = np.std(prob_train, axis=0)

        prob_train = prob_train - self.train_mean
        prob_train = prob_train / self.train_std

        self.clf.fit(prob_train, Y)

    def evaluate(self, test_data):
        Y = test_data['label']

        tree_prob_test = self.tree_clf.get_test_prob(test_data)
        readme_prob_test = self.readme_clf.get_test_prob(test_data)

        tree_prob_test[tree_prob_test == -np.inf] = -10
        readme_prob_test[readme_prob_test == -np.inf] = -10

        prob_test = np.hstack([tree_prob_test, readme_prob_test])
        prob_test = np.exp(prob_test)

        prob_test = prob_test - self.train_mean
        prob_test = prob_test / self.train_std

        output = self.clf.predict(prob_test)

        score = precision_score(Y, output, average=None)
        recall = recall_score(Y, output, average=None)
        print "\nEvaluating ProbClassifier"
        print "PRECISION SCORE: "
        print score
        print np.mean(score)
        print "RECALL SCORE: "
        print recall
        print np.mean(recall)

    def save_model(self):
        """
        Saves trained model to file.
        """
        joblib.dump(self.clf, self.build_model_filename(), compress=3)
        print "Successfully saved Prob Classifier!"

    def load_model(self):
        """
        Loads trained model from file.
        """
        self.clf = joblib.load(self.build_model_filename())
        print "Successfully loaded Prob Classifier!"

    def build_model_filename(self):
        return MODEL_PATH + 'prob_clf' + ".pkl"
