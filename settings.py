import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "")
STOPWORDS_PATH = os.path.join(PROJECT_ROOT, "config", "stopwords", "")
FEATURE_TRAIN_PATH = os.path.join(PROJECT_ROOT, "exploration", "labelled", "features", "")
FEATURE_PREDICT_PATH = os.path.join(PROJECT_ROOT, "prediction", "features", "")

JSON_README_FOLDER_PREDICT = os.path.join(PROJECT_ROOT, "prediction", "json_readmes", "")
JSON_README_FOLDER_TRAIN = os.path.join(PROJECT_ROOT, "collection", "%s", "json_readmes_unarchived_labelled", "")

LANGUAGE_FEATURES_NAME_PATH = os.path.join(PROJECT_ROOT, "prediction", "")