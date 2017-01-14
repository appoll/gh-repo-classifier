import codecs
import glob
import os
import shutil

from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

def extract_labelled_repos_names(labelled):
    try:
        file = open(labelled, 'r')
    except IOError:
        print 'labelled % has not been created'
        return []

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
    labelled_web = "labelled_web"
    labelled_dev = "labelled_dev"
    labelled_data = "labelled_data"
    labelled_docs = "labelled_docs"
    labelled_edu = "labelled_edu"
    labelled_hw = "labelled_hw"
    labelled_other = "labelled_other"

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
            print repo_name_extension
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


def extract_non_english_repo_names_from_readmes(readmes_repos_folder_labelled):
    repo_names = []
    for filename in glob.glob(readmes_repos_folder_labelled + '*'):
        split = filename.split('/')
        repo_name_md = split[len(split) - 1]
        repo_name = repo_name_md[:-len('.md')]

        f = codecs.open(filename, 'r', 'utf-8')
        readme_content = f.read()
        try:
            language = detect(readme_content)
        except LangDetectException:
            continue
        if language != 'en':
            #print "%s not english" % repo_name
            repo_names.append(repo_name)
    return repo_names


def move_non_english_repos(source_folder, repo_names):
    count = 0
    for filename in glob.glob(source_folder + '*'):
        dest_folder = source_folder.replace("json_", "json_nen_")
        if not os.path.exists(os.path.dirname(dest_folder)):
            os.makedirs(os.path.dirname(dest_folder))

        new_filename = filename.replace("json_", "json_nen_")
        split = filename.split('/')
        repo_name_extension = split[len(split) - 1]
        if '.json' in repo_name_extension:
            repo_name = repo_name_extension[:-len('.json')]
        elif '.md' in repo_name_extension:
            repo_name = repo_name_extension[:-len('.md')]
        if repo_name in repo_names:
            print 'moving %s from %s to %s' % (repo_name, filename, new_filename)
            shutil.move(filename, new_filename)
            count += 1
    if count == len(repo_names):
        print "moved %d from %s to %s" % (count, filename, new_filename)
    else:
        print "Moving of repos to %s failed. %d out of %d" %(dest_folder, count, len(repo_names))


def update_non_english(label):
    repos_folder_labelled = "../%s/json_repos_unarchived_labelled/" % label
    repos_folder_updated_labelled = "../%s/json_repos_updated_labelled/" % label
    readmes_repos_folder_labelled = "../%s/json_readmes_unarchived_labelled/" % label
    commits_interval_folder_labelled = "../%s/json_commits_interval_labelled/" % label
    commits_folder_labelled = "../%s/json_commits_labelled/" % label
    contents_folder_labelled = "../%s/json_contents_labelled/" % label
    trees_folder_labelled = "../%s/json_trees_labelled/" % label
    punch_card_folder_labelled = "../%s/json_punch_card_labelled/" % label

    repo_names = extract_non_english_repo_names_from_readmes(readmes_repos_folder_labelled)

    move_non_english_repos(repos_folder_updated_labelled, repo_names)
    move_non_english_repos(repos_folder_labelled, repo_names)
    move_non_english_repos(commits_interval_folder_labelled, repo_names)
    move_non_english_repos(commits_folder_labelled, repo_names)
    move_non_english_repos(contents_folder_labelled, repo_names)
    move_non_english_repos(trees_folder_labelled, repo_names)
    move_non_english_repos(punch_card_folder_labelled, repo_names)

    # move readmes last !
    move_non_english_repos(readmes_repos_folder_labelled, repo_names)
    print '%d repos of the %s class are not in english according to readme files' % (len(repo_names), label)

repos_folder = "../%s/json_repos_unarchived/"
repos_folder_updated = "../%s/json_repos_updated/"
readmes_repos_folder = "../%s/json_readmes_unarchived/"
commits_interval_folder = "../%s/json_commits_interval/"
commits_folder = "../%s/json_commits/"
contents_folder = "../%s/json_contents/"
trees_folder = "../%s/json_trees/"
punch_card_folder = "../%s/json_punch_card/"

repos_folder_labelled = "../%s/json_repos_unarchived_labelled/"
repos_folder_updated_labelled = "../%s/json_repos_updated_labelled/"
readmes_repos_folder_labelled = "../%s/json_readmes_unarchived_labelled/"
commits_interval_folder_labelled = "../%s/json_commits_interval_labelled/"
commits_folder_labelled = "../%s/json_commits_labelled/"
contents_folder_labelled = "../%s/json_contents_labelled/"
trees_folder_labelled = "../%s/json_trees_labelled/"
punch_card_folder_labelled = "../%s/json_punch_card_labelled/"

#update_non_english(Labels.uncertain)
# update_non_english(Labels.dev)
# update_non_english(Labels.data)
# update_non_english(Labels.docs)
# update_non_english(Labels.edu)
# update_non_english(Labels.hw)
# update_non_english(Labels.web)

# update(Labels.web, repos_folder, repos_folder_labelled)
# update(Labels.web, repos_folder_updated, repos_folder_updated_labelled)
# update(Labels.web, readmes_repos_folder, readmes_repos_folder_labelled)
# update(Labels.web, commits_interval_folder, commits_interval_folder_labelled)
# update(Labels.web, contents_folder, contents_folder_labelled)
# update(Labels.web, trees_folder, trees_folder_labelled)
# update(Labels.web, punch_card_folder, punch_card_folder_labelled)
# update(Labels.web, commits_folder, commits_folder_labelled)


# update(Labels.hw, repos_folder, repos_folder_labelled)
# update(Labels.hw, repos_folder_updated, repos_folder_updated_labelled)
# update(Labels.hw, readmes_repos_folder, readmes_repos_folder_labelled)
# update(Labels.hw, commits_interval_folder, commits_interval_folder_labelled)
# update(Labels.hw, contents_folder, contents_folder_labelled)
# update(Labels.hw, trees_folder, trees_folder_labelled)
# update(Labels.hw, punch_card_folder, punch_card_folder_labelled)
# update(Labels.hw, commits_folder, commits_folder_labelled)


# update(Labels.data, repos_folder, repos_folder_labelled)
# update(Labels.data, repos_folder_updated, repos_folder_updated_labelled)
# update(Labels.data, readmes_repos_folder, readmes_repos_folder_labelled)
# update(Labels.data, commits_interval_folder, commits_interval_folder_labelled)
# update(Labels.data, contents_folder, contents_folder_labelled)
# update(Labels.data, trees_folder, trees_folder_labelled)
# update(Labels.data, punch_card_folder, punch_card_folder_labelled)
# update(Labels.data, commits_folder, commits_folder_labelled)


# update(Labels.docs, repos_folder, repos_folder_labelled)
# update(Labels.docs, repos_folder_updated, repos_folder_updated_labelled)
# update(Labels.docs, readmes_repos_folder, readmes_repos_folder_labelled)
# update(Labels.docs, commits_interval_folder, commits_interval_folder_labelled)
# update(Labels.docs, contents_folder, contents_folder_labelled)
# update(Labels.docs, trees_folder, trees_folder_labelled)
# update(Labels.docs, punch_card_folder, punch_card_folder_labelled)
# update(Labels.docs, commits_folder, commits_folder_labelled)

#
# update(Labels.edu, repos_folder, repos_folder_labelled)
# update(Labels.edu, repos_folder_updated, repos_folder_updated_labelled)
# update(Labels.edu, readmes_repos_folder, readmes_repos_folder_labelled)
# update(Labels.edu, commits_interval_folder, commits_interval_folder_labelled)
# update(Labels.edu, contents_folder, contents_folder_labelled)
# update(Labels.edu, trees_folder, trees_folder_labelled)
# update(Labels.edu, punch_card_folder, punch_card_folder_labelled)
# update(Labels.edu, commits_folder, commits_folder_labelled)
