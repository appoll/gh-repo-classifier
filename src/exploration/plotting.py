from mpl_toolkits.mplot3d import Axes3D
from sklearn import decomposition
from sklearn.model_selection import learning_curve
import matplotlib.pyplot as plt
import numpy as np
from classification.data_io import read


def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
                        n_jobs=1, train_sizes=np.linspace(.1, 1.0, 5)):
    """
    Generate a simple plot of the test and training learning curve.

    Parameters
    ----------
    estimator : object type that implements the "fit" and "predict" methods
        An object of that type which is cloned for each validation.

    title : string
        Title for the chart.

    X : array-like, shape (n_samples, n_features)
        Training vector, where n_samples is the number of samples and
        n_features is the number of features.

    y : array-like, shape (n_samples) or (n_samples, n_features), optional
        Target relative to X for classification or regression;
        None for unsupervised learning.

    ylim : tuple, shape (ymin, ymax), optional
        Defines minimum and maximum yvalues plotted.

    cv : int, cross-validation generator or an iterable, optional
        Determines the cross-validation splitting strategy.
        Possible inputs for cv are:
          - None, to use the default 3-fold cross-validation,
          - integer, to specify the number of folds.
          - An object to be used as a cross-validation generator.
          - An iterable yielding train/test splits.

        For integer/None inputs, if ``y`` is binary or multiclass,
        :class:`StratifiedKFold` used. If the estimator is not a classifier
        or if ``y`` is neither binary nor multiclass, :class:`KFold` is used.

        Refer :ref:`User Guide <cross_validation>` for the various
        cross-validators that can be used here.

    n_jobs : integer, optional
        Number of jobs to run in parallel (default 1).
    """
    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")
    return plt

def plot_histograms(data_list,title_list=None,range=None):

    colors = ['red',  # forks
              'blue',  # size
              'yellow',  # open_issues
              'green',  # stargazers_count
              'black',  # watchers_count
              'gray',  # subscribers_count
              'purple',  # network_count
              'orange',
              'brown',
              'pink',
              'magenta'
              ]


    i = 0
    for data in data_list:
        plt.figure(i)
        plt.hist(data,range=range,color=colors[:data.shape[1]])
        i = i +1


def plot_pca(samples, classes):

    fig = plt.figure(1, figsize=(4, 3))
    plt.clf()
    ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)

    plt.cla()
    pca = decomposition.PCA(n_components=3)
    pca.fit(samples)
    features_and_samples = pca.transform(samples)

    for name, label in [(0, 0), (1, 1)]:
        ax.text3D(features_and_samples[classes == label, 0].mean(),
                  features_and_samples[classes == label, 1].mean() + 1.5,
                  features_and_samples[classes == label, 2].mean(), name,
                  horizontalalignment='center',
                  bbox=dict(alpha=.5, edgecolor='w', facecolor='w'))
    ## Reorder the labels to have colors matching the cluster results
    classes = np.choose(classes, [1, 2, 0]).astype(np.float)
    ax.scatter(features_and_samples[:, 0], features_and_samples[:, 1], features_and_samples[:, 2], c=classes,
               cmap=plt.cm.rainbow)

    ax.w_xaxis.set_ticklabels([])
    ax.w_yaxis.set_ticklabels([])
    ax.w_zaxis.set_ticklabels([])

# example data
#samples, classes = read("../exploration/data.txt")

# example for plot_pca
#plot_pca(samples,classes)
#plt.show()

# example for plot_histograms
#dev_data = samples[np.where(classes == 1)]
#other_data = samples[np.where(classes == 0)]
#range = (0,10000)
#plot_histograms(data_list=[dev_data,other_data],title_list=["dev data","other data"],range=range)
#plt.show()

