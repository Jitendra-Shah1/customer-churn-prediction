import os
import pickle
import pandas as pd
import sys
from .FeatureEngineering import engineering_features   # same-folder import

# Base directory of this file
BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, 'model.pkl')

# Ensure compatibility for pickles that expect engineering_features in __main__
if '__main__' in sys.modules:
    try:
        setattr(sys.modules['__main__'], 'engineering_features', engineering_features)
    except Exception:
        pass

# Load the trained model
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f, encoding='latin1')

THRESHOLD = 0.67   #  chosen threshold using precision_recall_curve

def predict_data(data: dict):
    df = pd.DataFrame([data])
    
    # Get probability of churn (class 1)
    prob = float(model.predict_proba(df)[0][1])
    
    # Applying threshold
    prediction = 1 if prob >= THRESHOLD else 0
    
    return {"prediction": prediction, "probability": prob}
