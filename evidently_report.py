# --------------------- evidently_report.py ---------------------
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
import pandas as pd

def generate_drift_report(reference, current, filename="drift_report.html"):
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference, current_data=current)
    report.save_html(filename)