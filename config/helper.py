import itertools
import matplotlib.pyplot as plt

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
        payload = {
            "query": "query {repository (owner:\"%s\" name:\"%s\") {description ref(qualifiedName: \"master\"){target {... on Commit {history(first:100) {edges {node {author {date}}}} } }}} }"}
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

    @staticmethod
    def plot_confusion_matrix(input_type, cm, classes,
                              normalize=False,
                              title='Confusion matrix',
                              cmap=plt.cm.Blues):
        """
        This function prints and plots the confusion matrix.
        Normalization can be applied by setting `normalize=True`.

        Courtesy of
        http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
        """
        plt.figure()
        plt.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.title(title)
        plt.colorbar()
        tick_marks = np.arange(len(classes))
        plt.xticks(tick_marks, classes, rotation=45)
        plt.yticks(tick_marks, classes)

        np.set_printoptions(precision=2)

        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
            cm = np.array([[round(s,2) for s in xs] for xs in cm])
        #     print("Normalized confusion matrix")
        # else:
        #     print('Confusion matrix, without normalization')

        thresh = cm.max() / 2.
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            plt.text(j, i, cm[i, j],
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")

        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')

        plt.savefig('cnf_m_%s_%s' % (normalize, input_type))
