import json
import re
from sklearn.feature_extraction import DictVectorizer
import os

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

regexInclusions = [
    'forks',
    'size',
    #'language',
    'open_issues',
    'stargazers_count',
    'has_issues',
    'has_downloads',
    'watchers_count',
    'subscribers_count',
    'network_count'
]

combinedRegexes= "(^" + "$)|(^".join(regexInclusions) + "$)"
print combinedRegexes

featureDicts = []
targets = []

for file in os.listdir("data collection/dev/repos"):
    if file.endswith(".json"):
        # load file
        repoFile = open("data collection/dev/repos/"+file,'r')
        # decode json object
        repo = json.load(repoFile)
        # omit irrelevant fields like url's, dates and owner
        features = filter(lambda x: (re.search(combinedRegexes,x)), repo.keys())
        featureDict = dict()
        for feature in features:
            featureDict[feature] = repo[feature]
        featureDicts.append(featureDict.values())
        targets.append("DEV")

for file in os.listdir("data collection/data/repos"):
    if file.endswith(".json"):
        # load file
        repoFile = open("data collection/data/repos/"+file,'r')
        # decode json object
        repo = json.load(repoFile)
        # omit irrelevant fields like url's, dates and owner
        features = filter(lambda x: (re.search(combinedRegexes,x)), repo.keys())
        featureDict = dict()
        for feature in features:
            featureDict[feature] = repo[feature]
        featureDicts.append(featureDict.values())
        targets.append("DATA")

print featureDicts
print targets