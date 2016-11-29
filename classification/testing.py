import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold


def read():
    initial_matrix = np.genfromtxt(open("../exploration/data.txt", "r"), delimiter=" ", dtype=int)
    return np.array(initial_matrix).astype('int')

mat = read()

features_and_samples = mat[25:56,:-1]
classes = mat[25:56,-1:]
classes = np.ravel(classes)


skf = StratifiedKFold(n_splits=5,random_state=0,shuffle=True)
for train, test in skf.split(features_and_samples, classes):
    #print("%s %s" % (train, test))
    clf = SVC(kernel='rbf')
    clf.fit(features_and_samples[train], classes[train])


    #predicted = clf.predict(features_and_samples[test])
    #print np.bitwise_xor(predicted,classes[test])
    print clf.score(features_and_samples[test],classes[test])
