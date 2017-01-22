import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib

from settings import FEATURE_TRAIN_PATH
from settings import FEATURE_PREDICT_PATH
from config.constants import *
from config.helper import Helper
from keyword_spotting import KeywordSpotting
from solid_classifier import SolidClassifier

from collection.labels import Labels

FEATURE_DATA_FORMAT_TRAIN = "%s_data_%s.txt"
FEATURE_DATA_FORMAT_PREDICT = "%s_data.txt"

REPO = "repo"
CI = "commits_interval"
LANG = "languages"
COMMIT = "commit"
README = "readme"
CONTENTS = "contents"
TREES = "trees"

LABELS = [Labels.data, Labels.dev, Labels.docs, Labels.edu, Labels.hw, Labels.web, Labels.uncertain]

class FeaturePreparation():
    def __init__(self, is_train = False):
        self.is_train = is_train

    def read_features_from_file(self, which):
        features_list = []
        if self.is_train:
            for label in LABELS:
                path = FEATURE_TRAIN_PATH + FEATURE_DATA_FORMAT_TRAIN % (which, label)
                features = pd.read_csv(path, delimiter=" ", header=0, skipfooter=1)
                print path
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
                elif label == Labels.uncertain:
                    features['label'] = 6
                features_list.append(features)
        else:
            path = FEATURE_PREDICT_PATH + FEATURE_DATA_FORMAT_PREDICT % (which)
            features_list = [pd.read_csv(path, delimiter=" ", header=0)]
        return features_list


    def build_feature_data(self):
        repo_features = self.read_features_from_file(REPO)
        ci_features = self.read_features_from_file(CI)
        lang_features = self.read_features_from_file(LANG)
        commit_features = self.read_features_from_file(COMMIT)
        readme_features = self.read_features_from_file(README)
        contents_features = self.read_features_from_file(CONTENTS)
        # trees_features = self.read_features_from_file(TREES)

        repo_data = pd.concat(repo_features)
        ci_data = pd.concat(ci_features)
        lang_data = pd.concat(lang_features)
        commit_data = pd.concat(commit_features)
        readme_data = pd.concat(readme_features)
        contents_data = pd.concat(contents_features)
        # trees_data = pd.concat(trees_features)

        self.repo_data = repo_data.drop_duplicates(subset=['repo_name'])
        self.ci_data = ci_data.drop_duplicates(subset=['repo_name'])
        self.commit_data = commit_data.drop_duplicates(subset=['repo_name'])
        self.lang_data = lang_data.drop_duplicates(subset=['repo_name'])
        self.readme_data = readme_data.drop_duplicates(subset=['repo_name'])
        self.contents_data = contents_data.drop_duplicates(subset=['repo_name'])
        # self.trees_data = trees_data.drop_duplicates(subset=['repo_name'])

        print 'Repo Data Shape'
        print repo_data.shape
        print 'Commits Interval Shape'
        print ci_data.shape
        print 'Languages Shape'
        print lang_data.shape
        print 'Commits Shape'
        print commit_data.shape
        print 'Readme Shape'
        print readme_data.shape
        print 'Contents Shape'
        print contents_data.shape
        # print 'Trees Shape'
        # print trees_data.shape

    def align_feature_data(self):
        if self.is_train:

            data = self.repo_data.merge(self.commit_data, on=["repo_name", "label"], how="inner")
            data = data.merge(self.lang_data, on=["repo_name", "label"], how="inner")
            data = data.merge(self.contents_data, on=["repo_name", "label"], how="inner")
            data = data.merge(self.ci_data, on=["repo_name", "label"], how="inner")
            data = data.merge(self.readme_data, on=["repo_name", "label"], how="left")
        else:
            data = self.repo_data.merge(self.commit_data, on=["repo_name"], how="inner")
            data = data.merge(self.lang_data, on=["repo_name"], how="inner")
            data = data.merge(self.contents_data, on=["repo_name"], how="inner")
            data = data.merge(self.ci_data, on=["repo_name"], how="inner")
            data = data.merge(self.readme_data, on=["repo_name"], how="left")
        data.to_csv('data_aligned')
        print data.shape
        return data

    def build_data(self):
        self.build_feature_data()
        data = self.align_feature_data()
        return data

class ClassificationExecutor():
    def __init__(self, is_train=False):
        self.is_train = is_train
        self.feature_prep = FeaturePreparation(is_train=is_train)
        self.data = self.feature_prep.build_data()
        self.input_repo_names = self.data['repo_name']
        print 'input repo names:'
        print self.input_repo_names
        return

    def run_solid_classifier(self):
        clf = SolidClassifier(is_train=False)
        clf.load_model()
        predictions = clf.predict(self.data)
        return predictions, self.input_repo_names

    def run_keyword_classifier(self):
        clf = KeywordSpotting(is_train=False)
        clf.load_model()
        predictions = clf.predict(self.data)
        return predictions, self.input_repo_names

if __name__ == '__main__':
    exe = ClassificationExecutor(is_train=True)
    # exe.run_keyword_classifier(exe.data)
    exe.run_solid_classifier(exe.data)