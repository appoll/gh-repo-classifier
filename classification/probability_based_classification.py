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
def get_repo_classes():
    file_names  = list()
    labels      = list()
    file_names.append('../exploration/labelled/features/trees_data_%s.txt' % Labels.data)
    labels.append(Labels.data)
    file_names.append('../exploration/labelled/features/trees_data_%s.txt' % Labels.dev)
    labels.append(Labels.dev)
    file_names.append('../exploration/labelled/features/trees_data_%s.txt' % Labels.web)
    labels.append(Labels.web)
    file_names.append('../exploration/labelled/features/trees_data_%s.txt' % Labels.hw)
    labels.append(Labels.hw)
    file_names.append('../exploration/labelled/features/trees_data_%s.txt' % Labels.docs)
    labels.append(Labels.docs)
    file_names.append('../exploration/labelled/features/trees_data_%s.txt' % Labels.edu)
    labels.append(Labels.edu)
    file_names.append('../exploration/labelled/features/trees_data_%s.txt' % Labels.uncertain)
    labels.append(Labels.uncertain)
    csv.field_size_limit(sys.maxsize)
    repo_label = dict()
    repo_label_num = dict()
    Y    = list()
    for i in range(len(file_names)):
        f = open(file_names[i],'rb')
        csv_content = csv.reader(f,delimiter=' ',quotechar='\"')
        for row in csv_content:
            repo_label[row[1]] = labels[i]
            repo_label_num[row[1]] = i

    return repo_label,repo_label_num

def get_num_py_row(str_row):
  
    num_list = str_row.split(' ')
    row = list()
    for num in num_list:
        if num.strip() == '':
            continue
        row.append(float(num))
    return np.reshape(np.array(row),(1,-1))

def get_probabilities_from_file(f,repo_label):
    csv_content = csv.reader(open(f,'rb'),delimiter=' ',quotechar='\"')
    commit_interval_data = dict()
    count = 0
    for row in csv_content:
        if row[1] in repo_label:
            commit_interval_data[row[1]] = get_num_py_row(row[0])
        else:
            count +=1
    return commit_interval_data

def align_data_and_labels(prob_data,repo_label_num):
    tmp_data = prob_data[0] # Just take arbitrary data to list the rpo names
    X = list()
    Y = list()
    for key in tmp_data:
        row = list()
        for i in range(len(prob_data)):
            if key in prob_data[i]:
                row.append(prob_data[i][key])
            else:
                row.append(np.ones((1,7))* np.log(1.0/7.0)) 
        row = np.hstack(row)
        X.append(row)
        Y.append(repo_label_num[key])
    X = np.vstack(X)
    Y = np.vstack(Y)
    return X,Y

prob_files = list()
prob_files.append('/home/waleed/informaticup/gh-repo-classifier/classification/multiclass/prob/prob_commit_interval_data')
prob_files.append('/home/waleed/informaticup/gh-repo-classifier/classification/multiclass/prob/prob_language_data')
prob_files.append('/home/waleed/informaticup/gh-repo-classifier/classification/multiclass/prob/prob_repo_data')
prob_data = list()
repo_label,repo_label_num = get_repo_classes()
for prob_file in prob_files:
    commit_interval_data = get_probabilities_from_file(f =prob_file ,repo_label=repo_label)
    prob_data.append(commit_interval_data)
X,Y = align_data_and_labels(prob_data,repo_label)
print X.shape
print Y.shape
