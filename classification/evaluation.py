from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt


class Evaluator:
    def __init__(self, classifier, parameters, cv = 3, seeds = 10, score = 'f1'):
        self.classifier = classifier
        self.parameters = parameters
        self.cv = cv
        self.score = score
        self.best_score = 0.0
        self.results = []
        self.seeds = seeds

    def evaluate(self, data):

        for seed in range(self.seeds):
            self.classifier.set_params(random_state = seed)

            data_train, data_test  = train_test_split(data, test_size=0.1, random_state=seed)

            y_train = data_train['label']
            y_test = data_test['label']

            X_train = data_train.drop(labels='label', axis=1)
            X_test = data_test.drop(labels='label', axis=1)

            clf = GridSearchCV(self.classifier, self.parameters, cv=self.cv, scoring='%s_macro' % self.score)
            clf.fit(X_train, y_train.values)

            y_true, y_pred = y_test, clf.predict(X_test)
            current_score = metrics.f1_score(y_true,y_pred,average='macro')

            print classification_report(y_true,y_pred)

            if self.best_score < current_score:
                self.best_score = current_score
                self.best_params = clf.best_params_

            self.results.append(current_score)

    def plot_results(self):

        plt.figure(0)
        plt.boxplot(self.results)
        plt.show()