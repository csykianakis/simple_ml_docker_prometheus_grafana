# --------------------- train.py ---------------------
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import mlflow
import json
import mlflow.sklearn
from config import MLFLOW_TRACKING_URI, MODEL_FILENAME, TRAIN_STATS_FILENAME

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.sklearn.autolog()

data = pd.DataFrame({
    'x': range(100),
    'y': [2 * i + 3 for i in range(100)]
})

X = data[['x']]
y = data['y']

x_mean = X['x'].mean()
x_std = X['x'].std()
with open(TRAIN_STATS_FILENAME, "w") as f:
    json.dump({"mean": x_mean, "std": x_std}, f)

with mlflow.start_run():
    model = LinearRegression()
    model.fit(X, y)
    joblib.dump(model, MODEL_FILENAME)
    mlflow.log_artifact(MODEL_FILENAME)
    mlflow.log_artifact(TRAIN_STATS_FILENAME)

print("Model trained and saved with MLflow tracking.")