# Farmer Assistance System

A FastAPI-based backend project that helps farmers with:
- Crop recommendation (top 3 crops from soil/weather inputs)
- Soil/fertilizer advice for a selected crop
- History storage and retrieval using Firebase Firestore

## Features
- Machine learning crop recommendation using `RandomForestClassifier`
- Rule-based soil correction and fertilizer suggestions
- REST API built with FastAPI
- Firestore integration to save analyze/suggest records
- Saved model artifacts (`.pkl`) for fast inference

## Project Structure
```text
farmer-assistance/
├── app.py                       # FastAPI application and API routes
├── test_api.py                  # Simple API test script (needs endpoint update)
├── data/
│   └── Crop_recommendation.csv  # Training dataset
├── database/
│   ├── firebase_db.py           # Firebase/Firestore client setup
│   └── cloud_storage.py         # Save/fetch records in Firestore
├── models/
│   ├── crop_model.pkl           # Trained RandomForest model
│   ├── scaler.pkl               # StandardScaler object
│   └── label_encoder.pkl        # LabelEncoder for crop labels
└── src/
    ├── train_model.py           # Model training pipeline
    ├── predict.py               # Top-3 crop prediction
    └── soil_rules.py            # Rule-based soil/fertilizer suggestions
```

## Dataset
- File: `data/Crop_recommendation.csv`
- Shape: `2200 x 8`
- Columns: `N, P, K, temperature, humidity, ph, rainfall, label`
- Number of crop classes: `22`

Classes:
`apple, banana, blackgram, chickpea, coconut, coffee, cotton, grapes, jute, kidneybeans, lentil, maize, mango, mothbeans, mungbean, muskmelon, orange, papaya, pigeonpeas, pomegranate, rice, watermelon`

## How It Works
1. `src/train_model.py` trains a Random Forest model from dataset inputs.
2. Features are standardized with `StandardScaler`.
3. Labels are encoded using `LabelEncoder`.
4. Artifacts are saved in `models/`.
5. `src/predict.py` loads artifacts and returns top 3 crops by class probability.
6. `src/soil_rules.py` generates soil/fertilizer suggestions based on rules.
7. `database/cloud_storage.py` stores API interactions in Firestore.

## Tech Stack
- Python
- FastAPI
- Pydantic
- scikit-learn
- pandas, numpy
- Firebase Admin SDK (Firestore)
- Uvicorn

## Installation and Setup
### 1. Clone repository
```bash
git clone https://github.com/gmsuhas-03/Famer_Assistance_System.git
cd Famer_Assistance_System
```

### 2. Create virtual environment
Windows PowerShell:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

macOS/Linux:
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install fastapi uvicorn pandas numpy scikit-learn joblib firebase-admin requests
```

### 4. Firebase setup (optional but recommended)
1. Create a Firebase project.
2. Enable Firestore.
3. Download service account JSON key.
4. Place the key as:
   - `firebase_key.json` in the project root.

Without valid Firebase credentials:
- `/analyze` and `/suggest` still return responses, but history saving fails silently (logged in console).
- `/history` returns an error message with empty records.

## Run the API
```bash
uvicorn app:app --reload
```

Server runs at:
- `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`

## API Endpoints
### `GET /`
Health check.

Response:
```json
{"status":"API running"}
```

### `POST /analyze`
Predicts top 3 crops for given soil/environment data.

Request body:
```json
{
  "soil_data": {
    "N": 90,
    "P": 42,
    "K": 43,
    "temperature": 20.8,
    "humidity": 82,
    "ph": 6.5,
    "rainfall": 202
  }
}
```

Response:
```json
{
  "top_3_crops": ["rice", "banana", "maize"]
}
```

### `POST /suggest`
Returns crop-specific fertilizer/soil correction guidance.

Request body:
```json
{
  "crop": "rice",
  "soil_data": {
    "N": 50,
    "P": 20,
    "K": 25,
    "temperature": 25.0,
    "humidity": 70,
    "ph": 5.2,
    "rainfall": 80
  }
}
```

Response (example):
```json
{
  "crop": "rice",
  "suggestions": [
    "Nitrogen LOW -> Apply Urea 30 kg/acre for rice",
    "Phosphorus VERY LOW -> Apply DAP 40 kg/acre for rice",
    "Soil highly acidic -> Apply Lime 200 kg/acre",
    "Low rainfall -> Provide supplemental irrigation"
  ]
}
```

### `GET /history?limit=10`
Returns latest analysis/suggestion records from Firestore.

## Train/Re-train the Model
Run:
```bash
python src/train_model.py
```

What it does:
- Splits dataset (`test_size=0.2`, `random_state=42`)
- Trains `RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)`
- Prints model accuracy
- Saves updated model artifacts into `models/`

## Notes and Limitations
- Soil advice rule base has explicit NPK targets for:
  `rice, maize, wheat, banana, cotton, chickpea, jute`
- Other crops still receive generic pH/rainfall advice and suitability fallback.
- `test_api.py` currently posts to `/soil-advice`, but the implemented endpoint is `/suggest`.

## Security Notes
- Do not commit `firebase_key.json` to GitHub.
- Keep service account keys private and rotate if exposed.

## Future Improvements
- Add `requirements.txt`
- Add automated tests with `pytest`
- Add model evaluation report and confusion matrix
- Add environment variable based Firebase key path
- Build frontend dashboard for farmers and admins

## Author
Suhas G Mestha
