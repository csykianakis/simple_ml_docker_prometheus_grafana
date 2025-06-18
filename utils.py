# --------------------- utils.py ---------------------
def load_training_stats(path):
    try:
        with open(path) as f:
            lines = f.readlines()
            mean = float(lines[0].split("=")[1])
            std = float(lines[1].split("=")[1])
        return mean, std
    except Exception:
        return 0, 1

def calculate_alert(x, mean, std, threshold_multiplier):
    deviation = abs(x - mean)
    threshold = threshold_multiplier * std
    return deviation > threshold, deviation, threshold