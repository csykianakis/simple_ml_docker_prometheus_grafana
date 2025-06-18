# --------------------- model.py ---------------------
import joblib
import numpy as np
from config import MODEL_FILENAME

model = joblib.load(MODEL_FILENAME)

def predict(x_val):
    return model.predict(np.array([[x_val]]))[0]
