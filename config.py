MLFLOW_TRACKING_URI = "http://mlflow:5001"
MODEL_FILENAME = "model.pkl"
TRAIN_STATS_FILENAME = "train_stats.json"
ALERT_THRESHOLD = 2.0

import os

if os.getenv("DOCKER_ENV") == "true":
    MLFLOW_TRACKING_URI = "http://mlflow:5001"  # for docker-compose environment
else:
    MLFLOW_TRACKING_URI = "http://localhost:5001"  # for local scripts like train.py
