import glob
import json

from collection.labels import Labels

repos_folder_path = "../collection/%s/updated_repos/"

repos_folders = []
dict_label_path = {}
dict_label_repos = {}
dict_label_repo_name = {}

features = [
    'forks',
    'size',
    'open_issues',
    'stargazers_count',
    #'has_issues',
    #'has_downloads',
    'watchers_count',
    'subscribers_count',
    'network_count',
    'languages_count',
    'labels_count',
    'contributors_count',
    'tags_count'
]

for label in Labels.toArray():
    repo_folder_path = repos_folder_path % label
    repos_folders.append(repo_folder_path)
    dict_label_path[label] = repo_folder_path

print dict_label_path

for label in sorted(dict_label_path.keys()):
    print label
    repoObjects = []
    repoNames = []
    repos_folder = dict_label_path.get(label)
    for filename in glob.glob(repos_folder + '*'):
        repoNames.append(filename.split('/')[4].split('.')[0])
        f = open(filename, 'r')
        repoObject = json.load(f)
        f.close()
        repoObjects.append(repoObject)
    dict_label_repos[label] = repoObjects
    dict_label_repo_name[label] = repoNames

print dict_label_repos.get(Labels.data.value)
print dict_label_repo_name.get(Labels.data.value)

f = open("data.txt", 'w')
for label in sorted(dict_label_path.keys()):
    repoNames = dict_label_repo_name[label]
    repoObjects = dict_label_repos[label]
    print repoNames
    print repoObjects
    for i in range (0, len(repoNames)):
        #line = repoNames[i]
        line = ""
        for feature in features:
            #line = line + " " + str(repoObjects[i][feature])
            line = line + str(repoObjects[i][feature]) + " "
        if label == Labels.dev.value:
            #line = line + " " + "1"
            line = line + "1"
        else:
            line = line + "0"
        #line = line + " " + label
        f.write(line)
        f.write('\n')
f.close()