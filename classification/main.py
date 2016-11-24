from matplotlib import pyplot as plt

import numpy as np
from sklearn.svm import SVC

from logistic_regression import LogisticRegression
from sklearn import svm

def read():
    initial_matrix = np.genfromtxt(open("../exploration/data.txt", "r"), delimiter=" ", dtype=int)
    print initial_matrix
    print '###'
    return np.array(initial_matrix).astype('int')

mat = read()
print mat

features_and_samples = mat[:-10,:-1]
classes = mat[:-10,-1:]
classes = np.ravel(classes)

clf = svm.SVC()
print clf.fit(features_and_samples, classes)

#predicted = clf.predict([[55, 2310, 11, 133, 133, 62, 55]])
predicted = clf.predict([[5695, 24191, 135, 15393, 15393, 592, 5695]])
print predicted