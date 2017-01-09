from matplotlib import pyplot as plt

import pandas as pd


def content(label):
    features = pd.read_csv("./additional/features/commit_data_%s.txt" % label, delimiter=" ", header=0)
    print("./additional/features/commit_data_%s.txt" % label)
    return features


def plot(feature):
    plt.figure()
    plt.title(feature)

    plt.plot(dev_commits_features[feature], color="r")
    plt.plot(data_commits_features[feature], color="b")
    plt.plot(docs_commits_features[feature], color="g")
    plt.plot(edu_commits_features[feature], color="y")
    plt.plot(web_commits_features[feature], color="black")
    plt.plot(hw_commits_features[feature], color="#afeeee")
    plt.plot(other_commits_features[feature], color="purple")

    plt.xlim(0, 60)
    plt.show()



dev_commits_features = content('dev')
print dev_commits_features.shape

data_commits_features = content('data')
print data_commits_features.shape

docs_commits_features = content('docs')
print docs_commits_features.shape

edu_commits_features = content('edu')
print edu_commits_features.shape

web_commits_features = content('web')
print web_commits_features.shape

hw_commits_features = content('hw')
print hw_commits_features.shape

other_commits_features = content('other')
print other_commits_features.shape


# plot('weekend_commits')
# plot('weekday_commits')
# plot('work_hrs_commits')
# plot('non_work_hrs_commits')

# plot('commits_per_day_average')
# plot('all_commits')

plot ('author_vs_committer')

# plot_one_vs_all('weekend_commits', 'dev')
# plot_one_vs_all('work_hrs_commits', 'dev')
plot_one_vs_all('inter_commit_distance_average', 'dev')
plot_one_vs_all('all_commits', 'dev')
