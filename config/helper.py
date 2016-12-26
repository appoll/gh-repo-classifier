
class Helper():

    @staticmethod
    def build_path_from_folder_and_repo_name(repo_name, folder, format):
        user, name = Helper.get_user_and_repo_name(repo_name)
        path = folder + format % (user, name)
        return path

    @staticmethod
    def get_user_and_repo_name(repo_name):
        user_and_name = repo_name[:-1].split('/')
        user = user_and_name[0]
        repo_name = user_and_name[1]
        return user, repo_name

    @staticmethod
    def build_payload(user, repo_name):
        payload = {"query": "query {repository (owner:\"%s\" name:\"%s\") {description ref(qualifiedName: \"master\"){target {... on Commit {history(first:100) {edges {node {author {date}}}} } }}} }"}
        payload["query"] = payload["query"] % (user, repo_name)
        return payload