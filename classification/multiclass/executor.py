import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib

from config.constants import *
from config.helper import Helper
from keyword_spotting import KeywordSpotting
from solid_classifier import SolidClassifier

from collection.labels import Labels

FEATURE_TRAIN_LOCATION = "../../exploration/labelled/features/"

FEATURE_DATA_FORMAT = "%s_data_%s.txt"

REPO = "repo"
CI = "commits_interval"
LANG = "languages"
COMMIT = "commit"
README = "readme"
CONTENTS = "contents"
TREES = "trees"


class FeaturePreparation():
    def __init__(self):
        # self.clf = RandomForestClassifier(n_estimators=10000, max_depth=60)
        self.folder_path_data = FEATURE_TRAIN_LOCATION

    def read_features_from_file(self, label, which):
        path = self.folder_path_data + FEATURE_DATA_FORMAT % (which, label)
        features = pd.read_csv(path, delimiter=" ", header=0, skipfooter=1)
        print path
        print features.shape

        # features.to_csv('repo_repo_names_%s' % label, columns=["repo_name"])

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

    def build_feature_data(self):

        repo_features = [self.read_features_from_file(Labels.data, REPO),
                         self.read_features_from_file(Labels.dev, REPO),
                         self.read_features_from_file(Labels.docs, REPO),
                         self.read_features_from_file(Labels.edu, REPO),
                         self.read_features_from_file(Labels.hw, REPO),
                         self.read_features_from_file(Labels.web, REPO),
                         self.read_features_from_file(Labels.uncertain, REPO)]

        ci_features = [self.read_features_from_file(Labels.data, CI),
                       self.read_features_from_file(Labels.dev, CI),
                       self.read_features_from_file(Labels.docs, CI),
                       self.read_features_from_file(Labels.edu, CI),
                       self.read_features_from_file(Labels.hw, CI),
                       self.read_features_from_file(Labels.web, CI),
                       self.read_features_from_file(Labels.uncertain, CI)]

        lang_features = [self.read_features_from_file(Labels.data, LANG),
                         self.read_features_from_file(Labels.dev, LANG),
                         self.read_features_from_file(Labels.docs, LANG),
                         self.read_features_from_file(Labels.edu, LANG),
                         self.read_features_from_file(Labels.hw, LANG),
                         self.read_features_from_file(Labels.web, LANG),
                         self.read_features_from_file(Labels.uncertain, LANG)]

        commit_features = [self.read_features_from_file(Labels.data, COMMIT),
                           self.read_features_from_file(Labels.dev, COMMIT),
                           self.read_features_from_file(Labels.docs, COMMIT),
                           self.read_features_from_file(Labels.edu, COMMIT),
                           self.read_features_from_file(Labels.hw, COMMIT),
                           self.read_features_from_file(Labels.web, COMMIT),
                           self.read_features_from_file(Labels.uncertain, COMMIT)]

        readme_features = [self.read_features_from_file(Labels.data, README),
                           self.read_features_from_file(Labels.dev, README),
                           self.read_features_from_file(Labels.docs, README),
                           self.read_features_from_file(Labels.edu, README),
                           self.read_features_from_file(Labels.hw, README),
                           self.read_features_from_file(Labels.web, README),
                           self.read_features_from_file(Labels.uncertain, README)]

        # trees_features = [self.read_features_from_file(Labels.data, TREES), self.read_features_from_file(Labels.dev, TREES),
        #                    self.read_features_from_file(Labels.docs, TREES),
        #                    self.read_features_from_file(Labels.edu, TREES),
        #                    self.read_features_from_file(Labels.hw, TREES), self.read_features_from_file(Labels.web, TREES),
        #                    self.read_features_from_file(Labels.uncertain, TREES)]

        contents_features = [self.read_features_from_file(Labels.data, CONTENTS),
                             self.read_features_from_file(Labels.dev, CONTENTS),
                             self.read_features_from_file(Labels.docs, CONTENTS),
                             self.read_features_from_file(Labels.edu, CONTENTS),
                             self.read_features_from_file(Labels.hw, CONTENTS),
                             self.read_features_from_file(Labels.web, CONTENTS),
                             self.read_features_from_file(Labels.uncertain, CONTENTS)]

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
        data = self.repo_data.merge(self.commit_data, on=["repo_name", "label"], how="inner")
        data = data.merge(self.lang_data, on=["repo_name", "label"], how="inner")
        data = data.merge(self.contents_data, on=["repo_name", "label"], how="inner")
        data = data.merge(self.ci_data, on=["repo_name", "label"], how="inner")
        data = data.merge(self.readme_data, on=["repo_name", "label"], how="left")
        data.to_csv('data_aligned')
        print data.shape
        return data

    def build_data(self):
        self.build_feature_data()
        data = self.align_feature_data()
        return data


class ClassificationExecutor():
    def __init__(self):
        self.feature_prep = FeaturePreparation()
        self.data = self.feature_prep.build_data()
        return

    def run_solid_classifier(self, data):
        clf = SolidClassifier()
        clf.train(data)
        clf.save_model()

    def run_keyword_classifier(self, data):

        train_data_2 = data[["repo_name"] + README_FEATURES + CONTENT_FEATURES + ["label"]]
        test_data_2 = data[["repo_name"] + README_FEATURES + CONTENT_FEATURES + ["label"]]

        train_data_2.to_csv("train_data_trash.txt", sep=",")

        clf = KeywordSpotting()
        # clf.predict(self.data)
        # clf.train(train_data_2)
        # clf.save_classifier()

        clf.load_model()

        predictions = clf.predict(test_data_2)
        print predictions

if __name__ == '__main__':
    exe = ClassificationExecutor()
    exe.run_keyword_classifier(exe.data)
    # exe.run_solid_classifier(exe.data)