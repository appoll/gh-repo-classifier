import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "")
STOPWORDS_PATH = os.path.join(PROJECT_ROOT, "config", "stopwords", "")
FEATURE_TRAIN_PATH = os.path.join(PROJECT_ROOT, "exploration", "labelled", "features", "")
FEATURE_PREDICT_PATH = os.path.join(PROJECT_ROOT, "prediction", "features", "")
