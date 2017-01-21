import numpy as np

from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import precision_score


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
        user_and_name = repo_name.split('/')
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
    def write_probabilities(forest, data, repo_names, labels, file_location):
        probabilities = forest.predict_log_proba(data)
        f = open(file_location, 'w')
        header = "label_prob repo_name label\n"
        f.write(header)

        for repo_name_idx, row in enumerate(probabilities):
            line = "\""
            for element in row:
                line += str(element) + " "
            line += "\" "
            line += repo_names.values[repo_name_idx]
            line += " "
            line += str(labels.values[repo_name_idx])
            line += "\n"
            f.write(line)
        f.close()

    @staticmethod
    def write_performance_to_file(filename, output, test_labels):
        f = open(filename, 'a')
        f.write("\n\nMean Squared Error \n")
        f.write(str(mean_squared_error(output, test_labels)))
        f.write("\nAccuracy score \n")
        f.write(str(accuracy_score(test_labels, output)))
        f.write("\nPrecision score \n")
        score = precision_score(test_labels, output, average=None)
        f.write(str(score))
        f.write("\nPrecision score mean\n")
        f.write(str(np.mean(score)))
        f.close()