import os
import re

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import nltk
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import precision_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from collection.labels import Labels

from sklearn.feature_extraction.text import CountVectorizer

train = pd.read_csv("../../exploration/text_data.txt", delimiter=" ", header=0)


# Download stopwords corpus
nltk.download('stopwords')

# keywords_edu = ["course", "slide", "lecture", "assignment", "university", "student", "week", "schedule",
#                 "work"]



keywords_edu = ["course", "coursera", "slide", "lecture", "assignment", "university", "student", "week", "schedule",
                "work", "term", "condition", "education", "class"]
keywords_dev = ["library", "package", "framework", "module", "app", "application", "server", "license", "develop",
                "dependencies", "installation", "api", "client"]
keywords_data = ["data", "dataset", "sample", "set", "database", "table"]
keywords_hw = ["homework", "solution"]
keywords_web = ["web", "website", "homepage", "javascript"]
keywords_doc = ["documentation", "collection", "manuals", "docs"]



# keywords_edu = ["course", "slide", "lecture", "assignment", "eduation"]
# keywords_dev = ["scripts", "pom.xml", "framework", "install"]
# keywords_data = ["dataset"]
# keywords_hw = ["homework", "hw0", "hw1", "task", "lesson", "week_"]
# keywords_web = ["website"]
# keywords_doc = ["doc"]




keyword_list = []
keyword_list.extend(keywords_edu)
keyword_list.extend(keywords_dev)
keyword_list.extend(keywords_data)
keyword_list.extend(keywords_hw)
keyword_list.extend(keywords_web)
keyword_list.extend(keywords_doc)

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
    for index, key in enumerate(keyword_list):
        word_set = content.split(" ")
        for word in word_set:
            if key in word:
                binary_vector[index] = 1
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

# data = extract_all_contents()
#
# print np.shape(data)
# print np.shape(train)
#
# test = train.merge(data, on="repo_name", how="outer")
#
# test.to_csv("trash_data.txt", sep=" ")

X = []


rows = train['readme_filename'].size
clean_readmes = []
for i in xrange(0, rows):
    # Call our function for each one, and add the result to the list of
    # clean reviews
    path_to_readme = train['readme_filename'][i]
    # dirty fix readme path name
    path = "../" + path_to_readme

    if not os.path.exists(path):
        raise IOError("Readme path does not exist!")

    content = readmeContent(path)

    clean_readmes.append(raw_to_words(content))



for repository_readme in clean_readmes:
    keys = keyword_spotting(repository_readme, keyword_list=keyword_list)
    X.append(keys)

labels = train['label']



# contents, labels = extract_contents()
#
# # labels = np.concatenate((labels,labels_content))
#
# for repository_content in contents:
#     keys = keyword_spotting(repository_content, keyword_list=keyword_list)
#     X.append(keys)






Y = np.asarray(labels, dtype=int)
X = np.array(X)
print X.shape
print Y.shape
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)



clf = RandomForestClassifier(n_estimators=1000, n_jobs=-1, random_state=1, max_depth=30)
clf.fit(X_train, Y_train)

output = clf.predict(X_test)

score = precision_score(Y_test, output, average=None)

print score

print np.mean(score)
print clf.score(X_test, Y_test)
