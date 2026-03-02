import joblib
import pandas as pd
import numpy as np
from pathlib import Path

# ---------------------------
# Load model artifacts
# ---------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"

model = joblib.load(MODEL_DIR / "crop_model.pkl")
scaler = joblib.load(MODEL_DIR / "scaler.pkl")
encoder = joblib.load(MODEL_DIR / "label_encoder.pkl")

# Feature order must match training
FEATURES = [
    "N",
    "P",
    "K",
    "temperature",
    "humidity",
    "ph",
    "rainfall"
]

def recommend_top3_crops(soil_data: dict):
    df = pd.DataFrame(
        [[soil_data[f] for f in FEATURES]],
        columns=FEATURES
    )

    scaled = scaler.transform(df)
    probs = model.predict_proba(scaled)[0]

    top3_idx = np.argsort(probs)[-3:][::-1]

    # ✅ ONLY crop names
    crops = []
    for idx in top3_idx:
        crops.append(
            encoder.inverse_transform([idx])[0]
        )

    return crops
