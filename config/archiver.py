import glob
import tarfile

from collection.labels import Labels


class Archiver:
    def __init__(self):
        self.repos_folder = "../collection/%s/repos/"
        self.unarchived_repos_folder = "../collection/%s/unarchived_repos/"
        self.class_folder = "../collection/%s/"
        self.tar_file_name = "all_%s_repos.tar"

    def archive(self, label):
        folder = self.repos_folder % label
        tar_location = self.class_folder % label
        file_name = tar_location + self.tar_file_name % label
        tar = tarfile(file_name)
        for filename in glob.glob(folder + '*'):
            tar.add(filename)
        tar.close()

    def unarchive(self, label):
        folder = self.unarchived_repos_folder % label
        tar_location = self.class_folder % label
        file_name = tar_location + self.tar_file_name % label
        tar = tarfile.open(file_name, "r")
        print "Unarchiving ", file_name
        tar.extractall(path=folder)
        tar.close()



#archiver = Archiver()

#archiver.archive(Labels.web.value)
