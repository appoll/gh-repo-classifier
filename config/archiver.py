import glob
import sys
import tarfile

sys.path.append('..')

REPO = 'repos'
READ_ME = 'read_mes'
COMMIT_ACTIVITY = 'commit_activities'
UPDATED_REPOS = 'updated_repos'

LABELLED_REPOS = 'labelled_repos'
LABELLED_READMES = 'labelled_readmes'
LABELLED_COMMITS = 'labelled_commits'
LABELLED_CONTENTS = 'labelled_contents'
LABELLED_TREES = 'labelled_trees'


class Archiver:
    def __init__(self):
        self.repos_folder = "../collection/%s/json_repos/"
        self.readmes_folder = "../collection/%s/json_readmes/"
        self.commit_activity_folder = "../collection/%s/json_commit_activity/"
        self.updated_repos_folder = "../collection/%s/json_repos_updated/"

        self.unarchived_repos_folder = "../collection/%s/json_repos_unarchived/"
        self.unarchived_readmes_folder = "../collection/%s/json_readmes_unarchived/"
        self.unarchived_commit_activity_folder = "../collection/%s/json_commit_activity_unarchived/"
        self.updated_unarchived_repos_folder = "../collection/%s/json_repos_updated_unarchived"

        self.repos_folder_updated_labelled = "../collection/%s/json_repos_updated_labelled/"
        self.readmes_repos_folder_labelled = "../collection/%s/json_readmes_unarchived_labelled/"
        self.commits_interval_folder_labelled = "../collection/%s/json_commits_interval_labelled/"
        self.contents_folder_labelled = "../collection/%s/json_contents_labelled/"
        self.trees_folder_labelled = "../collection/%s/json_trees_labelled/"

        self.class_folder = "../collection/%s/"

        self.tar_file_name = "all_%s_%s.tar"

    def archive(self, label, which):
        if which == REPO:
            folder = self.repos_folder % label
        elif which == READ_ME:
            folder = self.readmes_folder % label
        elif which == COMMIT_ACTIVITY:
            folder = self.commit_activity_folder % label
        elif which == UPDATED_REPOS:
            folder = self.updated_repos_folder % label
        else:
            raise ValueError('Which folder do you want to archive?')

        tar_location = self.class_folder % label
        tar_file_name = self.tar_file_name % (label, which)

        file_name = tar_location + tar_file_name
        tar = tarfile.open(file_name, 'w')
        for filename in glob.glob(folder + '*'):
            name = filename.rsplit('/', 1)[1]
            print name
            tar.add(filename, arcname=name)
        tar.close()

    def archive_labelled(self, label, which):
        if which == LABELLED_REPOS:
            folder = self.repos_folder_updated_labelled % label
        elif which == LABELLED_READMES:
            folder = self.readmes_repos_folder_labelled % label
        elif which == LABELLED_COMMITS:
            folder = self.commits_interval_folder_labelled % label
        elif which == LABELLED_CONTENTS:
            folder = self.contents_folder_labelled % label
        elif which == LABELLED_TREES:
            folder = self.trees_folder_labelled % label
        else:
            raise ValueError('Which folder do you want to archive?')

        tar_location = self.class_folder % label
        tar_file_name = self.tar_file_name % (label, which)

        file_name = tar_location + tar_file_name
        tar = tarfile.open(file_name, 'w')
        for filename in glob.glob(folder + '*'):
            name = filename.rsplit('/', 1)[1]
            print name
            tar.add(filename, arcname=name)
        tar.close()

    def unarchive(self, label, which):
        if which == REPO:
            folder = self.unarchived_repos_folder % label
        elif which == READ_ME:
            folder = self.unarchived_readmes_folder % label
        elif which == COMMIT_ACTIVITY:
            folder = self.unarchived_commit_activity_folder % label
        elif which == UPDATED_REPOS:
            folder = self.updated_unarchived_repos_folder % label
        else:
            raise ValueError('Which folder do you want to archive?')
        tar_location = self.class_folder % label
        tar_file_name = self.tar_file_name % (label, which)

        file_name = tar_location + tar_file_name
        tar = tarfile.open(file_name, "r")
        print "Unarchiving ", file_name
        print folder
        tar.extractall(path=folder)
        tar.close()

    def unarchive_labelled(self, label, which):

        if which == LABELLED_REPOS:
            folder = self.repos_folder_updated_labelled % label
        elif which == LABELLED_READMES:
            folder = self.readmes_repos_folder_labelled % label
        elif which == LABELLED_COMMITS:
            folder = self.commits_interval_folder_labelled % label
        elif which == LABELLED_CONTENTS:
            folder = self.contents_folder_labelled % label
        elif which == LABELLED_TREES:
            folder = self.trees_folder_labelled % label
        else:
            raise ValueError('Destination for unarchiving?')

        tar_location = self.class_folder % label
        tar_file_name = self.tar_file_name % (label, which)

        file_name = tar_location + tar_file_name
        tar = tarfile.open(file_name, "r")
        print "Unarchiving ", file_name
        print folder
        tar.extractall(path=folder)
        tar.close()


archiver = Archiver()

# archiver.archive('hw', READ_ME)
# archiver.archive('hw', REPO)
# archiver.archive('hw', COMMIT_ACTIVITY)

# archiver.archive('data', READ_ME)la

# archiver.archive('data', REPO)
# archiver.archive('data', COMMIT_ACTIVITY)

# archiver.archive('dev', READ_ME)
# archiver.archive('dev', REPO)
# archiver.archive('dev', COMMIT_ACTIVITY)
#
#
# archiver.archive('edu', COMMIT_ACTIVITY)
# archiver.archive('docs', COMMIT_ACTIVITY)
#
# archiver.unarchive('hw', READ_ME)
# archiver.unarchive('hw', REPO)
# archiver.unarchive('hw', COMMIT_ACTIVITY)
#
# archiver.unarchive('data', READ_ME)
# archiver.unarchive('data', REPO)
# archiver.unarchive('data', COMMIT_ACTIVITY)
#
# archiver.unarchive('dev', READ_ME)
# archiver.unarchive('dev', REPO)
# archiver.unarchive('dev', COMMIT_ACTIVITY)

# archiver.unarchive('docs', READ_ME)
# archiver.unarchive('docs', REPO)
# archiver.unarchive('docs', COMMIT_ACTIVITY)
#
# archiver.unarchive('edu', READ_ME)
# archiver.unarchive('edu', REPO)
# archiver.unarchive('edu', COMMIT_ACTIVITY)

# archiver.unarchive('web', READ_ME)
# archiver.unarchive('web', REPO)


# archiver.archive('dev', UPDATED_REPOS)
# archiver.unarchive('dev', UPDATED_REPOS)

# archiver.archive('docs', UPDATED_REPOS)

# archiver.unarchive('data', REPO)

# archiver.archive_labelled('edu', LABELLED_TREES)
# archiver.archive_labelled('edu', LABELLED_CONTENTS)
# archiver.archive_labelled('edu', LABELLED_COMMITS)
# archiver.archive_labelled('edu', LABELLED_READMES)
# archiver.archive_labelled('edu', LABELLED_REPOS)
# 
# archiver.archive_labelled('dev', LABELLED_TREES)
# archiver.archive_labelled('dev', LABELLED_CONTENTS)
# archiver.archive_labelled('dev', LABELLED_COMMITS)
# archiver.archive_labelled('dev', LABELLED_READMES)
# archiver.archive_labelled('dev', LABELLED_REPOS)
#
# archiver.archive_labelled('docs', LABELLED_TREES)
# archiver.archive_labelled('docs', LABELLED_CONTENTS)
# archiver.archive_labelled('docs', LABELLED_COMMITS)
# archiver.archive_labelled('docs', LABELLED_READMES)
# archiver.archive_labelled('docs', LABELLED_REPOS)
#
# archiver.archive_labelled('data', LABELLED_TREES)
# archiver.archive_labelled('data', LABELLED_CONTENTS)
# archiver.archive_labelled('data', LABELLED_COMMITS)
# archiver.archive_labelled('data', LABELLED_READMES)
# archiver.archive_labelled('data', LABELLED_REPOS)
#
# archiver.archive_labelled('web', LABELLED_TREES)
# archiver.archive_labelled('web', LABELLED_CONTENTS)
# archiver.archive_labelled('web', LABELLED_COMMITS)
# archiver.archive_labelled('web', LABELLED_READMES)
# archiver.archive_labelled('web', LABELLED_REPOS)
#
# archiver.archive_labelled('other', LABELLED_TREES)
# archiver.archive_labelled('other', LABELLED_CONTENTS)
# archiver.archive_labelled('other', LABELLED_COMMITS)
# archiver.archive_labelled('other', LABELLED_READMES)
# archiver.archive_labelled('other', LABELLED_REPOS)
#
# archiver.archive_labelled('hw', LABELLED_TREES)
# archiver.archive_labelled('hw', LABELLED_CONTENTS)
# archiver.archive_labelled('hw', LABELLED_COMMITS)
# archiver.archive_labelled('hw', LABELLED_READMES)
# archiver.archive_labelled('hw', LABELLED_REPOS)


# uncomment below

archiver.unarchive_labelled('edu', LABELLED_TREES)
archiver.unarchive_labelled('edu', LABELLED_CONTENTS)
archiver.unarchive_labelled('edu', LABELLED_COMMITS)
archiver.unarchive_labelled('edu', LABELLED_READMES)
archiver.unarchive_labelled('edu', LABELLED_REPOS)

archiver.unarchive_labelled('dev', LABELLED_TREES)
archiver.unarchive_labelled('dev', LABELLED_CONTENTS)
archiver.unarchive_labelled('dev', LABELLED_COMMITS)
archiver.unarchive_labelled('dev', LABELLED_READMES)
archiver.unarchive_labelled('dev', LABELLED_REPOS)

archiver.unarchive_labelled('docs', LABELLED_TREES)
archiver.unarchive_labelled('docs', LABELLED_CONTENTS)
archiver.unarchive_labelled('docs', LABELLED_COMMITS)
archiver.unarchive_labelled('docs', LABELLED_READMES)
archiver.unarchive_labelled('docs', LABELLED_REPOS)

archiver.unarchive_labelled('data', LABELLED_TREES)
archiver.unarchive_labelled('data', LABELLED_CONTENTS)
archiver.unarchive_labelled('data', LABELLED_COMMITS)
archiver.unarchive_labelled('data', LABELLED_READMES)
archiver.unarchive_labelled('data', LABELLED_REPOS)

archiver.unarchive_labelled('web', LABELLED_TREES)
archiver.unarchive_labelled('web', LABELLED_CONTENTS)
archiver.unarchive_labelled('web', LABELLED_COMMITS)
archiver.unarchive_labelled('web', LABELLED_READMES)
archiver.unarchive_labelled('web', LABELLED_REPOS)

archiver.unarchive_labelled('other', LABELLED_TREES)
archiver.unarchive_labelled('other', LABELLED_CONTENTS)
archiver.unarchive_labelled('other', LABELLED_COMMITS)
archiver.unarchive_labelled('other', LABELLED_READMES)
archiver.unarchive_labelled('other', LABELLED_REPOS)

archiver.unarchive_labelled('hw', LABELLED_TREES)
archiver.unarchive_labelled('hw', LABELLED_CONTENTS)
archiver.unarchive_labelled('hw', LABELLED_COMMITS)
archiver.unarchive_labelled('hw', LABELLED_READMES)
archiver.unarchive_labelled('hw', LABELLED_REPOS)
