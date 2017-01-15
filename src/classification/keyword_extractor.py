import glob
import re

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

from classification import svc
from src.collection import Labels

readmes_folder_path = '../collection/%s/json_readmes_unarchived/'

repos_folders = []
dict_label_path = {}
dict_label_readmes = {}
dict_label_repo_name = {}

for label in Labels.toArray():
    readme_folder_path = readmes_folder_path % label.value
    repos_folders.append(readme_folder_path)
    dict_label_path[label] = readme_folder_path

print dict_label_path

for label in Labels.toArray():
    print label
    readmeFilenames = []
    repoNames = []
    repos_folder = dict_label_path.get(label)
    for filename in glob.glob(repos_folder + '*'):
        # print filename
        repoNames.append(filename.split('/')[4].split('.')[0])
        # f = open(filename, 'r')
        # textObject = f.read()
        # f.close()
        readmeFilenames.append(filename)
    dict_label_readmes[label.value] = readmeFilenames
    dict_label_repo_name[label.value] = repoNames


def get_readmes_for_label(param_label):
    name = "text_data_%s.txt" % param_label
    f = open(name, 'w')
    header = "label readme_filename\n"
    f.write(header)
    for label in Labels.toArray():
        repoNames = dict_label_repo_name[label.value]
        readmeFilenames = dict_label_readmes[label.value]
        for i in range(0, len(repoNames)):
            line = ""
            if label.value == param_label:
                line = line + "1" + " "
            else:
                line = line + "-1" + " "

            line = line + readmeFilenames[i]
            f.write(line)
            f.write('\n')
    f.close()


get_readmes_for_label(Labels.edu.value)
get_readmes_for_label(Labels.dev.value)
get_readmes_for_label(Labels.data.value)
get_readmes_for_label(Labels.docs.value)
get_readmes_for_label(Labels.hw.value)
get_readmes_for_label(Labels.web.value)


# use svm to do binary classification

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
    dist = pd.np.sum(train_data_features, axis=0)
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


def binary_classification(label):
    global train, train_data_features
    name = "../classification/text_data_%s.txt" % label

    train = pd.read_csv(name, delimiter=" ", header=0)
    rows = train['readme_filename'].size
    clean_readmes = []
    for i in xrange(0, rows):
        # Call our function for each one, and add the result to the list of
        # clean reviews
        content = readmeContent(train['readme_filename'][i])
        clean_readmes.append(raw_to_words(content))
    #
    # vectorizer = CountVectorizer(analyzer="word",
    #                              tokenizer=None,
    #                              preprocessor=None,
    #                              stop_words=None,
    #                              max_features=1000)
    vectorizer = CountVectorizer(analyzer="word",
                                 tokenizer=None,
                                 preprocessor=None,
#                                 stop_words=['docs', 'framework', 'homework', 'course', 'data']
                                  ngram_range=(2, 3)
                                 , max_features=1000
                                 , binary=True
                                 )
    train_data_features = vectorizer.fit_transform(clean_readmes)
    train_data_features = train_data_features.toarray()
    print_words_and_count(vectorizer=vectorizer)
    print_feature_matrix(train_data_features)
    # print_feature_matrix(train_data_features, withCorrespondingExample=True)
    labels = train['label']
    svc_object, training_score, testing_score = svc.runLinear(train_data_features, labels)

    # weights of each word, as assigned by the svm
    coef_ = svc_object.coef_
    argsort = np.argsort(coef_)
    print coef_.shape

    argmax = np.argmax(coef_)

    # flip the asc sorted array
    argsort[0] = argsort[0][::-1]


    vocab = vectorizer.get_feature_names()
    print vocab[argmax]

    for i in range(10):
        print coef_[0, argsort[0][i]]
        print vocab[argsort[0][i]]

    print training_score
    print testing_score


#binary_classification(Labels.dev.value)
#binary_classification(Labels.hw.value)
# assignments ok

#binary_classification(Labels.docs.value)

#binary_classification(Labels.data.value)
#binary_classification(Labels.edu.value)
