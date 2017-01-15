import glob
import json

import numpy as np

from classification import svc
from src.collection import Labels

WINDOW = 4


def extract_commit_info(label):
    weeks = []
    commit_activity_folder = "../collection/%s/json_commit_activity_unarchived/" % label.value
    for filename in glob.glob(commit_activity_folder + '*'):
        f = open(filename, 'r')
        year = json.load(f)
        f.close()

        weekly_activity = [week['total'] for week in year]
        weeks.append(weekly_activity)

    weeks = np.array(weeks)
    return weeks


examples = []
labels = []

for i in range(4):
    i_ = Labels.toArray()[i]
    print i_
    info = extract_commit_info(i_)
    y = np.ones((info.shape[0], 1)) * i
    examples.append(info)
    labels.append(y)

examples = np.vstack(examples)
labels = np.vstack(labels)
labels = np.ravel(labels)

count = 0
indeces = []
for i in range(examples.shape[0]):
    max = 0
    max_index = 0
    for j in range(examples.shape[1] - WINDOW):
        t = np.sum(examples[i, j:j + WINDOW])
        if t > max:
            max = t
            max_index = j
    #examples[i, :] = np.roll(examples[i, :], -1 * max_index)
    print max_index, max
    if max == 0:
        indeces.append(i)

examples = np.delete(examples, indeces, axis=0)
labels = np.delete(labels, indeces)
print "the count is ", count

print examples.shape
print labels.shape

svc_object, training_score, testing_score = svc.runLinear(examples, labels)
print training_score
print testing_score
