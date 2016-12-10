from sklearn.metrics import *
from sklearn.model_selection import StratifiedKFold
from sklearn.svm import SVC

from classification.data_io import read

samples, classes = read()

skf = StratifiedKFold(n_splits=5,random_state=0,shuffle=True)
clf = SVC(kernel='rbf',gamma=0.001)


for train, test in skf.split(samples, classes):
    #print("%s %s" % (train, test))
    clf = SVC(kernel='rbf')
    clf.fit(samples[train], classes[train])


    predicted = clf.predict(samples[test])
    #print np.bitwise_xor(predicted,classes[test])
    #print predicted
    #print classes[test]
    #print clf.score(features_and_samples[test],classes[test])
    print precision_score(classes[test],predicted)


#plt.show()









