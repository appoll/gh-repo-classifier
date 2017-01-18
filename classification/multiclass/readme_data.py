import os
import re

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import precision_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

from collection.labels import Labels


def get_features(label):
    path = "../../exploration/labelled/features/readme_data_%s.txt" % label
    features = pd.read_csv(path, delimiter=" ",
                           header=0, skipfooter=1)
    print path
    print features.shape

    # features.to_csv('readmes_repo_names_%s' % label, columns=["repo_name"])

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


features = [get_features(Labels.data), get_features(Labels.dev), get_features(Labels.docs), get_features(Labels.edu),
            get_features(Labels.hw), get_features(Labels.web), get_features(Labels.uncertain)]

train = pd.concat(features)

print train.shape

# nltk.download()

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
    stops = set(stopwords.words("english"))

    # 5. Remove stop words
    meaningful_words = [w for w in words if not w in stops]
    return (" ".join(meaningful_words))

# panda dataframe row
def row_to_words(row):
    path = "../" + row['readme_filename']
    if not os.path.exists(path):
        print 'missing %s ' % path
    content = readmeContent(path)
    # print content
    words = raw_to_words(content)
    return words

train['readme_words'] = train.apply(lambda row: row_to_words(row), axis=1)

print train.shape

vectorizer = TfidfVectorizer(analyzer="word",
                             tokenizer=None,
                             preprocessor=None,
                             stop_words=['docs', 'framework', 'homework', 'course', 'data']
                             , ngram_range=(1, 3)
                             , max_features=2000
                             )

clean_readmes = train['readme_words'].tolist()

print clean_readmes[0]
print clean_readmes[10]
X = vectorizer.fit_transform(clean_readmes)
print X.shape

labels = train['label']
Y = np.asarray(labels, dtype=int)
print Y.shape

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

C_range = np.logspace(-2, 10, 13)
gamma_range = np.logspace(-9, 3, 13)
gS = GridSearchCV(SVC(), {'kernel': ['rbf'], 'C': C_range, 'gamma': gamma_range}, n_jobs=-1)
clf = RandomForestClassifier(n_estimators=1000, n_jobs=-1, random_state=0, max_depth=30)
clf.fit(X_train, Y_train)

output = clf.predict(X_test)

score = precision_score(Y_test, output, average=None)
print score

print np.mean(score)

print clf.score(X_test, Y_test)
