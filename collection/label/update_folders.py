import glob
import os
import shutil

from collection.labels import Labels


def extract_labelled_repos_names(labelled):
    file = open(labelled, 'r')
    labelled_repos = file.readlines()

    labelled_repos_names = []

    for line in labelled_repos:
        labelled_repos_names.append(line.rstrip('\n'))
    return labelled_repos_names


def update(label, source, dest):
    """
    :param label: the label which has been manually validated
    :param source: the source folder where repo info already exists
    :param dest: the destination folder of labelled repo info
    """
    source = source % label
    labelled_web = "../labelled_web"
    labelled_dev = "../labelled_dev"
    labelled_data = "../labelled_data"
    labelled_docs = "../labelled_docs"
    labelled_edu = "../labelled_edu"
    labelled_hw = "../labelled_hw"
    labelled_other = "../labelled_other"

    dev_labelled_repos_names = extract_labelled_repos_names(labelled_dev)
    data_labelled_repos_names = extract_labelled_repos_names(labelled_data)
    docs_labelled_repos_names = extract_labelled_repos_names(labelled_docs)
    edu_labelled_repos_names = extract_labelled_repos_names(labelled_edu)
    hw_labelled_repos_names = extract_labelled_repos_names(labelled_hw)
    other_labelled_repos_names = extract_labelled_repos_names(labelled_other)
    web_labelled_repos_names = extract_labelled_repos_names(labelled_web)

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

        if repo_name in dev_labelled_repos_names:
            dest_folder = dest % 'dev'
        elif repo_name in data_labelled_repos_names:
            dest_folder = dest % 'data'
        elif repo_name in docs_labelled_repos_names:
            dest_folder = dest % 'docs'
        elif repo_name in edu_labelled_repos_names:
            dest_folder = dest % 'edu'
        elif repo_name in hw_labelled_repos_names:
            dest_folder = dest % 'hw'
        elif repo_name in other_labelled_repos_names:
            dest_folder = dest % 'other'
        elif repo_name in web_labelled_repos_names:
            dest_folder = dest % 'web'
        else:
            print 'not labelled'
            continue

        if not os.path.exists(os.path.dirname(dest_folder)):
            os.makedirs(os.path.dirname(dest_folder))
        shutil.copy(filename, dest_folder)
        print 'copied to %s folder' % dest_folder


repos_folder = "../%s/json_repos_unarchived/"
repos_folder_updated = "../%s/json_repos_updated/"
readmes_repos_folder = "../%s/json_readmes_unarchived/"

repos_folder_labelled = "../%s/json_repos_unarchived_labelled/"
repos_folder_updated_labelled = "../%s/json_repos_updated_labelled/"
readmes_repos_folder_labelled = "../%s/json_readmes_unarchived_labelled/"

update(Labels.web.value, repos_folder, repos_folder_labelled)
update(Labels.web.value, repos_folder_updated, repos_folder_updated_labelled)
update(Labels.web.value, readmes_repos_folder, readmes_repos_folder_labelled)
