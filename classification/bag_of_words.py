import re

import pandas as pd
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

train = pd.read_csv("../exploration/text_data.txt", delimiter=" ", header=0)


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


rows = train['readme_filename'].size
clean_readmes = []
for i in xrange(0, rows):
    # Call our function for each one, and add the result to the list of
    # clean reviews
    content = readmeContent(train['readme_filename'][i])
    clean_readmes.append(raw_to_words(content))

print clean_readmes[100]

vectorizer = CountVectorizer(analyzer="word",
                             tokenizer=None,
                             preprocessor=None,
                             stop_words=None,
                             max_features=5000)

train_data_features = vectorizer.fit_transform(clean_readmes)
train_data_features = train_data_features.toarray()

print train_data_features[20][30]

print max(train_data_features[20])

vocab = vectorizer.get_feature_names()
print vocab

# Sum up the counts of each vocabulary word
dist = np.sum(train_data_features, axis=0)

# For each, print the vocabulary word and the number of times it
# appears in the training set
for tag, count in zip(vocab, dist):
    print count, tag