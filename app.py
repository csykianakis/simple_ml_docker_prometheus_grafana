# --------------------- app.py ---------------------
from flask import Flask, request, jsonify, render_template_string
from model import predict
import mlflow
import mlflow.sklearn
import logging
from config import *
from utils import load_training_stats, calculate_alert
from pydantic import BaseModel, ValidationError
from prometheus_flask_exporter import PrometheusMetrics

# Set MLflow tracking URI from config
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
metrics = PrometheusMetrics(app, path="/metrics")  # This registers /metrics


# Load training stats for alert calculation
TRAIN_MEAN, TRAIN_STD = load_training_stats(TRAIN_STATS_FILENAME)
logging.info(f"Loaded training stats: mean={TRAIN_MEAN}, std={TRAIN_STD}")

# Define Pydantic model for input validation
class InputData(BaseModel):
    x: float

# HTML template for form input and displaying results
HTML_TEMPLATE = """
<!doctype html>
<title>Model Prediction</title>
<h2>Enter a value for x:</h2>
<form method=post action="/predict-form">
  <input type=number step="any" name=x>
  <input type=submit value=Predict>
</form>
{% if prediction is not none %}
  <h3>Prediction: {{ prediction }}</h3>
{% endif %}
{% if alert %}
  <p style="color: red">⚠️ Warning: Input distribution deviates significantly from training data!</p>
{% endif %}
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, prediction=None, alert=False)

@app.route('/predict-form', methods=['POST'])
def predict_form():
    x = float(request.form['x'])
    pred = predict(x)
    alert, deviation, threshold = calculate_alert(x, TRAIN_MEAN, TRAIN_STD, ALERT_THRESHOLD)
    logging.info(f"Input: {x}, Deviation: {deviation:.2f}, Threshold: {threshold:.2f}, Alert: {alert}")

    with mlflow.start_run(nested=True):
        mlflow.log_param("input", x)
        mlflow.log_metric("prediction", pred)
        mlflow.log_metric("alert_triggered", int(alert))

    return render_template_string(HTML_TEMPLATE, prediction=pred, alert=alert)

@app.route('/predict', methods=['POST'])
def make_prediction():
    try:
        input_data = InputData(**request.get_json())
        x = input_data.x
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    pred = predict(x)
    alert, deviation, threshold = calculate_alert(x, TRAIN_MEAN, TRAIN_STD, ALERT_THRESHOLD)
    logging.info(f"Input: {x}, Deviation: {deviation:.2f}, Threshold: {threshold:.2f}, Alert: {alert}")

    with mlflow.start_run(nested=True):
        mlflow.log_param("input", x)
        mlflow.log_metric("prediction", pred)
        mlflow.log_metric("alert_triggered", int(alert))

    return jsonify({"prediction": pred, "alert": alert})

# if __name__ == '__main__':
#     print("\nRegistered Routes:")
#     for rule in app.url_map.iter_rules():
#         print(f"{rule.endpoint:25s} -> {rule.rule}")
#     app.run(host='0.0.0.0', port=2000, debug=True)

if __name__ == '__main__':
    print("\nRegistered Routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint:25s} -> {rule.rule}")
    app.run(host='0.0.0.0', port=2001, debug=False) # Change debug to False