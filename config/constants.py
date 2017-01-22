"""Defines the column labels for the used features (excluding language features, see language_feature_hack)"""
REPO_FEATURES = ["size", "labels", "tags", "issues", "branches", "languages", "forks", "commits",
                      "comments"]
COMMIT_FEATURES = ["all_commits", "weekend_commits", "weekday_commits", "work_hrs_commits",
                        "non_work_hrs_commits",
                        "inter_commit_distance_average", "commits_per_day_average", "authors_count",
                        "author_vs_committer",
                        "active_days"]
CI_FEATURES = ["commits_count", "commits_interval_days", "commits_per_day"]
README_FEATURES = ["readme_filename"]
CONTENT_FEATURES = ["total", "dirs", "files", "folder_names", "file_names", "fo_and_fi_names"]
TREE_FEATURES = ["blob_paths"]

"""Defines the type of input considered by the BaseClassifier"""
INPUT_CI = 'input_ci'
INPUT_COMMIT = 'input_commit'
INPUT_LANGUAGE = 'input_language'
INPUT_REPO = 'input_repo'
INPUT_PUNCH = 'input_punch'
INPUT_ALL = 'input_all'

LANGUAGE_FEATURES_NAME_FILE = "languages.pkl"
