import os
import re

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import nltk
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import precision_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

# from classification.file_name_based_classification import Y_train
from src.collection import Labels
from sklearn.model_selection import ShuffleSplit
from sklearn.feature_extraction.text import CountVectorizer

train = pd.read_csv("../../exploration/text_data.txt", delimiter=" ", header=0)


# Download stopwords corpus
nltk.download('stopwords')

# keywords_edu = ["course", "slide", "lecture", "assignment", "university", "student", "week", "schedule",
#                 "work"]



keywords_readme_edu = ["course", "coursera", "slide", "lecture", "assignment", "university", "student", "week", "schedule",
                "work", "term", "condition", "education", "class"]
keywords_readme_dev = ["library", "package", "framework", "module", "app", "application", "server", "license", "develop",
                "dependencies", "installation", "api", "client"]
keywords_readme_data = ["data", "dataset", "sample", "set", "database", "table"]
keywords_readme_hw = ["homework", "solution"]
keywords_readme_web = ["web", "website", "homepage", "javascript"]
keywords_readme_doc = ["documentation", "collection", "manuals", "docs"]

keyword_readme_list = []
keyword_readme_list.extend(keywords_readme_edu)
keyword_readme_list.extend(keywords_readme_dev)
keyword_readme_list.extend(keywords_readme_data)
keyword_readme_list.extend(keywords_readme_hw)
keyword_readme_list.extend(keywords_readme_web)
keyword_readme_list.extend(keywords_readme_doc)


keywords_content_edu = ["course", "slide", "lecture", "assignment", "eduation"]
keywords_content_dev = ["scripts", "pom.xml", "framework", "install"]
keywords_content_data = ["dataset"]
keywords_content_hw = ["homework", "hw0", "hw1", "task", "lesson", "week_"]
keywords_content_web = ["website"]
keywords_content_doc = ["doc"]

keyword_content_list = []
keyword_content_list.extend(keywords_content_edu)
keyword_content_list.extend(keywords_content_dev)
keyword_content_list.extend(keywords_content_data)
keyword_content_list.extend(keywords_content_hw)
keyword_content_list.extend(keywords_content_web)
keyword_content_list.extend(keywords_content_doc)

keyword_list = []
keyword_list.extend(keyword_readme_list)
keyword_list.extend(keyword_content_list)



print keyword_list
def readmeContent(filename):
    f = open(filename, 'r')
    return f.read()

def raw_to_words(content):
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

def print_feature_matrix(features, withCorrespondingExample=False):
    if withCorrespondingExample == True:
        for row in range(0, features.shape[0]):
            print features[row]
            print train['label'][row]
            print train['readme_filename'][row]
    else:
        print features

def keyword_spotting(content, keyword_list):
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


def read_contents_data(label):
    features = pd.read_csv("../../exploration/labelled/features/contents_data_%s.txt" % label, delimiter=" ", header=0)

    print features.shape

    #features.to_csv('contents_repo_names_%s' % label, columns=["repo_name"])
    # features = features.drop(labels='repo_name', axis=1)

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

    return features

def extract_contents():
    data = [read_contents_data(Labels.data), read_contents_data(Labels.dev), read_contents_data(Labels.docs), read_contents_data(Labels.edu),
                read_contents_data(Labels.hw), read_contents_data(Labels.web), read_contents_data(Labels.uncertain)]

    data = pd.concat(data)
    print data.shape
    contents = data["fo_and_fi_names"]
    labels = data['label']
    return contents, labels

def extract_all_contents():
    data = [read_contents_data(Labels.data), read_contents_data(Labels.dev), read_contents_data(Labels.docs), read_contents_data(Labels.edu),
                read_contents_data(Labels.hw), read_contents_data(Labels.web), read_contents_data(Labels.uncertain)]

    data = pd.concat(data)
    return data

data = extract_all_contents()

print np.shape(data)
print np.shape(train)

data = train.merge(data, on="repo_name", how="outer")
rows = data['repo_name'].size
for i in xrange(0, rows):
    if (np.isnan(data["label_x"][i])):
        data.loc[i, "label_x"]= data["label_y"][i]

data.to_csv("trash_data.txt", sep=",")



rows = data['repo_name'].size
clean_readmes = []
for i in xrange(0, rows):
    # Call our function for each one, and add the result to the list of
    # clean reviews
    path_to_readme = data['readme_filename'][i]
    if path_to_readme is not np.nan:
        # dirty fix readme path name
        path = "../" + path_to_readme
        if not os.path.exists(path):
            raise IOError("Readme path does not exist!")
        content = readmeContent(path)
        clean_readmes.append(raw_to_words(content))
    else:
        clean_readmes.append(None)




readme_features = []


for repository_readme in clean_readmes:
    keys = keyword_spotting(repository_readme, keyword_list=keyword_readme_list)
    readme_features.append(keys)



# contents, labels = extract_contents()

# labels = np.concatenate((labels,labels_content))
content_features = []


for repository_content in data["fo_and_fi_names"]:
    if repository_content is np.nan:
        repository_content = None
        print "It is naaaaaaaan"
    keys = keyword_spotting(repository_content, keyword_list=keyword_content_list)
    content_features.append(keys)



print "Shape readme features: ", np.shape(readme_features)
print "Shape content features: ", np.shape(content_features)

labels = data['label_x']








X = np.hstack((readme_features, content_features))
print "Shape of stacked features:" , np.shape(X)


Y = np.asarray(labels, dtype=int)
print "Shape labels: ", np.shape(Y)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

param_grid = [{'n_estimators': [100, 200, 300, 400, 500], 'max_depth': [None, 10, 20, 30, 40]}]
svr = RandomForestClassifier(random_state=1)

# clf = GridSearchCV(svr, param_grid, verbose=10000)


# clf1 = AdaBoostClassifier(RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=1, max_depth=5))


clf1 = RandomForestClassifier(n_estimators=500, n_jobs=-1, random_state=1, max_depth=30)
clf1.fit(X_train, Y_train)

clf2 = SVC(kernel="rbf", probability=True)
clf2.fit(X_train, Y_train)

clf3 = GaussianNB()
clf3.fit(X_train, Y_train)

clf4 = LogisticRegression()
clf4.fit(X_train, Y_train)

clf = VotingClassifier(estimators=[('rf', clf1), ('svm',clf2), ('gnb', clf3), ('lr', clf4)], voting='soft')
clf.fit(X_train, Y_train)

print "RANDOM FOREST"
output1 = clf1.predict(X_test)
score = precision_score(Y_test, output1, average=None)
print score
print np.mean(score)
print clf1.score(X_test, Y_test)

print "SVM"
output2 = clf2.predict(X_test)
score = precision_score(Y_test, output2, average=None)
print score
print np.mean(score)
print clf2.score(X_test, Y_test)

print "NAIVE BAYES"
output3 = clf3.predict(X_test)
score = precision_score(Y_test, output3, average=None)
print score
print np.mean(score)
print clf3.score(X_test, Y_test)

print "LOGISTIC REGRESSION"
output4 = clf4.predict(X_test)
score = precision_score(Y_test, output4, average=None)
print score
print np.mean(score)
print clf4.score(X_test, Y_test)


print "COMBINED"
output = clf.predict(X_test)
score = precision_score(Y_test, output, average=None)
print score
print np.mean(score)
print clf.score(X_test, Y_test)
