import glob
import json

from collection.labels import Labels

repos_folder_path = "../collection/%s/repos/"

repos_folders = []
dict_label_path = {}
dict_label_repos = {}
dict_label_repo_name = {}

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
        f.write(repoNames[i] + "," + str(repoObjects[i]['language']) + "," + label)
        f.write('\n')
f.close()