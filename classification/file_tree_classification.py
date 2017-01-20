import csv
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score
import sys
sys.path.append('..')

from collection.labels import Labels


def cleanString(s):
    p = re.compile('(?<=[a-z])(?=[A-Z])')
    newS = p.sub(r' ',s)
    newS = re.sub('[0-9]+',' NN ',newS)
    newS = re.sub('[^a-zA-Z]',' ',newS)
    newS = re.sub('\W+',' ',newS)
    return newS.strip().lower()

def normalizeFile(paths):
    
    newPaths = ''
    for path in paths.split(' '):
        count = 0
        splited_string = path.split('/')
        newPath = ''
        for s in splited_string:
            if s != '':
                newPath += '/'+str(count)
                count = count + 1
        newPaths += newPath +' '
    return newPaths

    
file_names = list()
# file_names.append('../exploration/features/contents_data_data.txt')
# file_names.append('../exploration/features/contents_data_dev.txt')
# file_names.append('../exploration/features/contents_data_web.txt')
# file_names.append('../exploration/features/contents_data_hw.txt')
# file_names.append('../exploration/features/contents_data_docs.txt')
# file_names.append('../exploration/features/contents_data_edu.txt')

file_names.append('../exploration/labelled/features/trees_data_%s.txt' % Labels.data)
file_names.append('../exploration/labelled/features/trees_data_%s.txt' % Labels.dev)
file_names.append('../exploration/labelled/features/trees_data_%s.txt' % Labels.web)
file_names.append('../exploration/labelled/features/trees_data_%s.txt' % Labels.hw)
file_names.append('../exploration/labelled/features/trees_data_%s.txt' % Labels.docs)
file_names.append('../exploration/labelled/features/trees_data_%s.txt' % Labels.edu)
file_names.append('../exploration/labelled/features/trees_data_%s.txt' % Labels.uncertain)
csv.field_size_limit(sys.maxsize)
data = list()
Y    = list()
for i in range(len(file_names)):
    f = open(file_names[i],'rb')
    csv_content = csv.reader(f,delimiter=' ',quotechar='\"')
    for row in csv_content:
        Y.append(i)
        repo = row[0]
        repo = cleanString(repo)
        data.append( repo)


print normalizeFile('/hello/this/is/me  /hello/again')

cV = CountVectorizer(ngram_range=(1,4),max_features=7000,binary=True)
X = cV.fit_transform(data)



Y = np.asarray(Y,dtype=int)


X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.2,random_state=0)

# C_range = np.logspace(-2, 10, 13)
# gamma_range = np.logspace(-9, 3, 13)
# gS = GridSearchCV(SVC(),{'kernel':['rbf'],'C':C_range,'gamma':gamma_range},n_jobs=-1)
n_estimators = [1000]
clf = GridSearchCV(RandomForestClassifier(n_jobs=-1),{'n_estimators':n_estimators})

# gS.fit(X_train,Y_train)
clf.fit(X_train,Y_train)
Y_pred = clf.predict(X_test)
s = precision_score(Y_test,Y_pred, average  = None)
print s
print clf.score(X_test,Y_test)

