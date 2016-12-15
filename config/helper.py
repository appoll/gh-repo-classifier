
class Helper():

    @staticmethod
    def build_path_from_folder_and_repo_name(repo_name, folder, format):
        user_and_name = repo_name[:-1].split('/')
        user = user_and_name[0]
        repo_name = user_and_name[1]
        path = folder + format % (user, repo_name)
        return path