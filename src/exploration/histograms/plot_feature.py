import argparse
import glob
import json
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("repoclass", help="the desired repository class", type=str)
parser.add_argument("feature", help="the desired feature", type=str)
args = parser.parse_args()

repos = []

for filename in glob.glob(args.repoclass + '*'):
    print filename
    f = open(filename, 'r')
    repoObject = json.load(f)
    repos.append(repoObject)

feature_values = []

for repo in repos:
    feature_values.append(repo[args.feature])

print feature_values
plt.hist(feature_values, 10, range=[0, 10000])
plt.ylabel(args.feature)
plt.savefig('histo_' + args.repoclass + '_' + args.feature)
