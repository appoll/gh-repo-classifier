import glob
import sys
import tarfile

sys.path.append('..')

REPO = 'repos'
READ_ME = 'read_mes'
COMMIT_ACTIVITY = 'commit_activities'
UPDATED_REPOS = 'updated_repos'


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


archiver = Archiver()

# archiver.archive('hw', READ_ME)
# archiver.archive('hw', REPO)
# archiver.archive('hw', COMMIT_ACTIVITY)

# archiver.archive('data', READ_ME)
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
archiver.unarchive('dev', UPDATED_REPOS)