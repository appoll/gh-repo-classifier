
class Helper():

    @staticmethod
    def build_path_from_folder_and_repo_name(repo_name, folder, format):
        user, name = Helper.get_user_and_repo_name(repo_name)
        path = folder + format % (user, name)
        return path

    @staticmethod
    def build_path_from_folder_and_repo_link(repo_link, folder, format):
        user, name = Helper.get_user_and_repo_name_from_link(repo_link)
        path = folder + format % (user, name)
        return path

    @staticmethod
    def get_user_and_repo_name(repo_name):
        user_and_name = repo_name[:-1].split('/')
        user = user_and_name[0]
        repo_name = user_and_name[1]
        return user, repo_name

    @staticmethod
    def get_user_and_repo_name_from_link(repo_link):
        user = repo_link.split('/')[3]
        repo_name = repo_link.split('/')[4]
        repo_name = repo_name.rstrip('\r\n')
        return user, repo_name

    @staticmethod
    def build_payload(user, repo_name):
        payload = {"query": "query {repository (owner:\"%s\" name:\"%s\") {description ref(qualifiedName: \"master\"){target {... on Commit {history(first:100) {edges {node {author {date}}}} } }}} }"}
        payload["query"] = payload["query"] % (user, repo_name)
        return payload

    def build_repo_name_from_repo_link(self, repo_link):
        user, name = Helper.get_user_and_repo_name_from_link(repo_link)
        return user + '/' + name.rstrip('\r\n')

    @staticmethod
    def write_probabilities(forest, data, repo_names, file_location):
        input = data.drop(labels='label', axis=1)
        probabilities = forest.predict_log_proba(input)
        f = open(file_location, 'w')
        header = "label_prob repo_name\n"
        f.write(header)

        for repo_name_idx, row in enumerate(probabilities):
            line = "\""
            for element in row:
                line += str(element) + " "
            line += "\" "
            line += repo_names.values[repo_name_idx]
            line += "\n"
            f.write(line)
        f.close()