import numpy as np
from sklearn.svm import LinearSVC

from classification import svc
from classification import svc_linear


def read():
    initial_matrix = np.genfromtxt(open("../exploration/data.txt", "r"), delimiter=" ", dtype=int)
    print initial_matrix
    print '###'
    mat = np.array(initial_matrix).astype('int')
    examples = mat[:, :-1]
    labels = mat[:, -1:]
    labels = np.ravel(labels)
    return examples, labels


x, y = read()

training_score, testing_score = svc_linear.run(x, y)

print training_score
print testing_score

# training_score, testing_score = svc.runLinear(x, y)
# print training_score
# print testing_score

# training_score, testing_score = svc.runPolynomial(x, y)
# print training_score
# print testing_score

