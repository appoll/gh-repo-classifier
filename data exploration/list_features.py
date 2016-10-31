import json
import re

# open stored meta data of an example repo
f = open('../data exploration/DEV_homeworkr_basic.txt', 'r')

# conversion from json data types to python data types
object = json.load(f)

# omit irrelevant fields like url's, dates and owner
features = filter(lambda x: not(re.search('.*_url',x) or re.search('.*_at',x) or re.search('owner',x)), object.keys())

# print all features
for feature in features:
    print str(feature)+': '+str(object[feature])
