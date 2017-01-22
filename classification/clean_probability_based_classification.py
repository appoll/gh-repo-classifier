import csv
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import precision_score
from sklearn.linear_model import LogisticRegression
import sys
sys.path.append('..')

from collection.labels import Labels


def read_data(prefix, classifier_names, train ):
    if train:
        postfix = 'train'
    else:
        postfix = 'test'
    Y    = list()
    X    = list()
    for i in range(len(classifier_names)):
        X.append(list())
    for i in range(len(classifier_names)):
        f = open(prefix+classifier_names[i]+'_'+postfix,'rb')
        csv_content = csv.reader(f,delimiter=' ',quotechar='\"',)
        next(csv_content, None)  # skip the headers
        for row in csv_content:
            X[i].append(get_num_py_row(row[0]))
            if i == 0:
                Y.append(int(row[2]))
    X_temp = list()
    for i in range(len(classifier_names)):
        X_temp.append(np.vstack(X[i]))
    X = np.hstack(X_temp)
    Y = np.array(Y)

    return X,Y

def get_num_py_row(str_row):
  
    num_list = str_row.split(' ')
    row = list()
    for num in num_list:
        if num.strip() == '':
            continue
        elif num.strip() == '-inf':
            row.append(-10.0)
        else:
            row.append(float(num))
    return np.reshape(np.array(row),(1,-1))


prefix = './multiclass/prob/prob_'
classifier_names = ['trees','keyword']#,'input_all']#,'input_language','input_repo','trees']#,'input_all']#,'trees']#,'r_c_l']
# classifier_names = ['commit','keyword','lang','repo']
X_train, Y_train = read_data(prefix,classifier_names,True)
X_test, Y_test   = read_data(prefix,classifier_names,False)
X_train = np.exp(X_train)
X_test  = np.exp(X_test)

m = np.mean(X_train, axis=0)
s  = np.std(X_train,axis = 0)
X_train = X_train - m
X_train = X_train / s
X_test = X_test - m
X_test = X_test / s

n_estimators = [10,20,50,100,1000]
C_range      = np.linspace(0.01,10,100)
lr_range     = np.linspace(0.5,5,100)
clf = GridSearchCV(SVC(),{'C':C_range},n_jobs = -1)#{'n_estimators':n_estimators},n_jobs = -1)
#clf = GridSearchCV(AdaBoostClassifier(LogisticRegression()),{'n_estimators':n_estimators,'learning_rate':lr_range},n_jobs = -1) 
#clf = RandomForestClassifier(n_estimators=1000,max_depth=30,n_jobs = -1)
clf.fit(X_train,Y_train)

print clf.score(X_test,Y_test)
from sklearn.metrics import precision_score,recall_score
Y_pred = clf.predict(X_test)
precision  = precision_score(Y_test,Y_pred,average = None)
recall     = recall_score(Y_test,Y_pred,average = None)
print precision
print recall
print np.mean(precision)
print np.mean(recall)
