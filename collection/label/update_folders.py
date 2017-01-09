import glob
import os
import shutil

from collection.labels import Labels


def update(label, source, dest):
    source = source % label
    dest = dest % label

    labelled_file = "../labelled_%s" % label

    file = open(labelled_file, 'r')
    labelled_repos = file.readlines()

    labelled_repos_names = []

    for line in labelled_repos:
        labelled_repos_names.append(line.rstrip('\n'))

    total = len(labelled_repos_names)
    count = 0
    for filename in glob.glob(source + '*'):
        split = filename.split('/')
        repo_name_json = split[len(split) - 1]

        # below assumes that '_' would not appear in a github user name
        repo_name_extension = repo_name_json.replace('_', '/', 1)

        if repo_name_extension.count('/') > 1:
            print 'da'
            print repo_name_extension

        if '.json' in repo_name_extension:
            repo_name = repo_name_extension[:-len('.json')]
        elif '.md' in repo_name_extension:
            repo_name = repo_name_extension[:-len('.md')]
        else:
            raise Exception('should not be!')

        if repo_name in labelled_repos_names:
            if not os.path.exists(os.path.dirname(dest)):
                os.makedirs(os.path.dirname(dest))
            shutil.copy(filename, dest)
            print 'copied to %s' % dest
            count += 1
        else:
            pass
            #print 'Not there, not copying.'

    print 'copied %d out of %d for the %s label' % (count, total, label)

repos_folder = "../%s/json_repos_unarchived/"
repos_folder_updated = "../%s/json_repos_updated/"
readmes_repos_folder = "../%s/json_readmes_unarchived/"

repos_folder_labelled = "../%s/json_repos_unarchived_labelled/"
repos_folder_updated_labelled = "../%s/json_repos_updated_labelled/"
readmes_repos_folder_labelled = "../%s/json_readmes_unarchived_labelled/"

# update(Labels.web.value, repos_folder, repos_folder_labelled)
# update(Labels.web.value, repos_folder_updated, repos_folder_updated_labelled)
# update(Labels.web.value, readmes_repos_folder, readmes_repos_folder_labelled)


update(Labels.dev.value, repos_folder, repos_folder_labelled)
update(Labels.dev.value, repos_folder_updated, repos_folder_updated_labelled)
update(Labels.dev.value, readmes_repos_folder, readmes_repos_folder_labelled)

update(Labels.data.value, repos_folder, repos_folder_labelled)
update(Labels.data.value, repos_folder_updated, repos_folder_updated_labelled)
update(Labels.data.value, readmes_repos_folder, readmes_repos_folder_labelled)

update(Labels.docs.value, repos_folder, repos_folder_labelled)
update(Labels.docs.value, repos_folder_updated, repos_folder_updated_labelled)
update(Labels.docs.value, readmes_repos_folder, readmes_repos_folder_labelled)

update(Labels.hw.value, repos_folder, repos_folder_labelled)
update(Labels.hw.value, repos_folder_updated, repos_folder_updated_labelled)
update(Labels.hw.value, readmes_repos_folder, readmes_repos_folder_labelled)

update(Labels.uncertain.value, repos_folder, repos_folder_labelled)
update(Labels.uncertain.value, repos_folder_updated, repos_folder_updated_labelled)
update(Labels.uncertain.value, readmes_repos_folder, readmes_repos_folder_labelled)

update(Labels.edu.value, repos_folder, repos_folder_labelled)
update(Labels.edu.value, repos_folder_updated, repos_folder_updated_labelled)
update(Labels.edu.value, readmes_repos_folder, readmes_repos_folder_labelled)
