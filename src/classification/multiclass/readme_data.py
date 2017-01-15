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

train = pd.read_csv("../../exploration/text_data.txt", delimiter=" ", header=0)


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


def print_words_and_count(vectorizer):
    vocab = vectorizer.get_feature_names()
    # print vocab
    # Sum up the counts of each vocabulary word
    dist = np.sum(train_data_features, axis=0)
    # print dist

    # For each, print the vocabulary word and the number of times it
    # appears in the training set
    for tag, count in zip(vocab, dist):
        print count, tag


def print_feature_matrix(features, withCorrespondingExample=False):
    if withCorrespondingExample == True:
        for row in range(0, features.shape[0]):
            print features[row]
            print train['label'][row]
            print train['readme_filename'][row]
    else:
        print features


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
#
# vectorizer = CountVectorizer(analyzer="word",
#                              tokenizer=None,
#                              preprocessor=None,
#                              stop_words=None,
#                              max_features=1000)

vectorizer = TfidfVectorizer(analyzer="word",
                             tokenizer=None,
                             preprocessor=None,
                             stop_words=['docs', 'framework', 'homework', 'course', 'data']
                             ,ngram_range=(1, 3)
                             , max_features=2000
                             )

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