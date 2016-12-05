import glob

from collection.labels import Labels

# repos_folder_path = "../collection/%s/updated_repos/"
readmes_folder_path = '../collection/%s/readmes/'

repos_folders = []
dict_label_path = {}
dict_label_readmes = {}
dict_label_repo_name = {}

for label in Labels.toArray():
    readme_folder_path = readmes_folder_path % label
    repos_folders.append(readme_folder_path)
    dict_label_path[label] = readme_folder_path

print dict_label_path

for label in sorted(dict_label_path.keys()):
    print label
    readmeFilenames = []
    repoNames = []
    repos_folder = dict_label_path.get(label)
    for filename in glob.glob(repos_folder + '*'):
        # print filename
        repoNames.append(filename.split('/')[4].split('.')[0])
        # f = open(filename, 'r')
        # textObject = f.read()
        # f.close()
        readmeFilenames.append(filename)
    dict_label_readmes[label] = readmeFilenames
    dict_label_repo_name[label] = repoNames


f = open("text_data.txt", 'w')
header = "label readme_filename\n"
f.write(header)
for label in sorted(dict_label_path.keys()):
    repoNames = dict_label_repo_name[label]
    readmeFilenames = dict_label_readmes[label]
    for i in range(0, len(repoNames)):
        line = ""
        if label == Labels.dev.value:
            line = line + "1" + " "
        else:
            line = line + "0" + " "
        line = line + readmeFilenames[i]
        f.write(line)
        f.write('\n')
f.close()
