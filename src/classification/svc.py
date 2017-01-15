import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC


def runLinear(examples, labels):
    svc = SVC(kernel='linear')
    # x, y = shuffle(examples, labels)
    x, y = examples, labels
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0)
    print("X_train shape: %s" % repr(x_train.shape))
    print("y_train shape: %s" % repr(y_train.shape))
    print("X_test shape: %s" % repr(x_test.shape))
    print("y_test shape: %s" % repr(y_test.shape))

    svc.fit(x_train, y_train)

    # calculation takes unexpectedly long
    return score(svc, x_train, y_train), score(svc,x_test, y_test)
    # Unresolved attribute reference for class svc
    # return svc.score(x_train, y_train), svc.score(x_test, y_test)


def runPolynomial(examples, labels):
    svc = SVC(kernel='poly')
    # x, y = shuffle(examples, labels)
    x, y = examples, labels
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0)
    print("X_train shape: %s" % repr(x_train.shape))
    print("y_train shape: %s" % repr(y_train.shape))
    print("X_test shape: %s" % repr(x_test.shape))
    print("y_test shape: %s" % repr(y_test.shape))

    svc.fit(x_train, y_train)
    # never ending 100% processor usage
    return score(svc, x_train, y_train), score(svc, x_test, y_test)


def shuffle(examples, labels):
    n_sample = examples.shape[0]
    # np.random.seed(0)
    order = np.random.permutation(n_sample)
    examples = examples[order]
    labels = labels[order].astype(np.float)
    return examples, labels

def score(svc, x_test, y_test):
    return accuracy_score(y_test, svc.predict(x_test))
