import json
import re
from sklearn.feature_extraction import DictVectorizer
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# open stored meta data of an example repo
f1 = open('data exploration/DEV_homeworkr_basics.txt', 'r')
f2 = open('data exploration/DATA_housing_basics.txt', 'r')

# conversion from json data types to python data types
object1 = json.load(f1)
object2 = json.load(f2)

regexExclusions = [
    '.*url', # useless
    '.*_at', # useless
    'owner', # useless(?)
    'permissions', # useless
    'homepage', # useless
    'description', # word list -> further processing
    'full_name', # further processing (?)
    'name', # further processing (?)
    'default_branch',
    'id'
]

combinedRegexes= "(" + ")|(".join(regexExclusions) + ")"

# omit irrelevant fields like url's, dates and owner
features1 = filter(lambda x: not(re.search(combinedRegexes,x)), object1.keys())
features2 = filter(lambda x: not(re.search(combinedRegexes,x)), object2.keys())

featureDict1 = dict()
featureDict2 = dict()

# print all features
#for feature in features:
#    print str(feature)+': '+str(type(object[feature]))

for feature in features1:
    featureDict1[feature] = object1[feature]

for feature in features2:
    featureDict2[feature] = object2[feature]

vec = DictVectorizer()
print vec.fit_transform([featureDict1,featureDict2]).toarray()

# pca = pca()
# pca.fit_transform(vec.fit_transform([featuredict1,featuredict2]).toarray())
# print pca.explained_variance_
print vec.get_feature_names()
#
# plt.figure(1, figsize=(4, 3))
# plt.clf()
# plt.axes([.2, .2, .7, .7])
# plt.plot(pca.explained_variance_, linewidth=2)
# plt.axis('tight')
# plt.xlabel('n_components')
# plt.ylabel('explained_variance_')
# plt.show()

