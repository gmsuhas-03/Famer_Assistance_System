import pandas as pd
import numpy as np
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# ---------------------------
# Paths
# ---------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "Crop_recommendation.csv"
MODEL_DIR = BASE_DIR / "models"

MODEL_DIR.mkdir(exist_ok=True)


# ---------------------------
# Load dataset
# ---------------------------
df = pd.read_csv(DATA_PATH)

print("Dataset loaded:", df.shape)


# ---------------------------
# Split features and target
# ---------------------------
X = df.drop("label", axis=1)
y = df["label"]


# ---------------------------
# Encode target labels
# ---------------------------
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)


# ---------------------------
# Train-test split
# ---------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)


# ---------------------------
# Feature scaling
# ---------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# ---------------------------
# Train Random Forest model
# ---------------------------
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train_scaled, y_train)


# ---------------------------
# Evaluate model
# ---------------------------
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)

print(f"Model accuracy: {accuracy:.4f}")


# ---------------------------
# Save model artifacts
# ---------------------------
joblib.dump(model, MODEL_DIR / "crop_model.pkl")
joblib.dump(scaler, MODEL_DIR / "scaler.pkl")
joblib.dump(encoder, MODEL_DIR / "label_encoder.pkl")

print("Model files saved in /models folder")
