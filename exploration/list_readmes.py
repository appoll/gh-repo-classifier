import glob

from collection.labels import Labels

readmes_folder_path = '../collection/%s/json_readmes_unarchived_labelled/'

repos_folders = []
dict_label_path = {}
dict_label_readmes = {}
dict_label_repo_name = {}

for label in Labels.toArray():
    readme_folder_path = readmes_folder_path % label
    repos_folders.append(readme_folder_path)
    dict_label_path[label] = readme_folder_path

print dict_label_path

for label in Labels.toArray():
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
for label in Labels.toArray():
    repoNames = dict_label_repo_name[label]
    readmeFilenames = dict_label_readmes[label]
    for i in range(0, len(repoNames)):
        line = ""
        if label == Labels.data:
            line = line + "0" + " "
        elif label == Labels.dev:
            line = line + "1" + " "
        elif label == Labels.docs:
            line = line + "2" + " "
        elif label == Labels.edu:
            line = line + "3" + " "
        elif label == Labels.hw:
            line = line + "4" + " "
        elif label == Labels.web:
            line = line + "5" + " "
        elif label == Labels.uncertain:
            line = line + "6" + " "
        else:
            raise ValueError("Wrong label value!")

        line = line + readmeFilenames[i]
        f.write(line)
        f.write('\n')
f.close()
