from fastapi import FastAPI, Query
from pydantic import BaseModel

from src.predict import recommend_top3_crops
from src.soil_rules import get_soil_advice

from database.cloud_storage import (
    save_analysis_to_cloud,
    save_suggestion_to_cloud,
    fetch_history
)

app = FastAPI(title="Farmer Assistance System")


# -----------------------------
# Input models
# -----------------------------
class SoilData(BaseModel):
    N: int
    P: int
    K: int
    temperature: float
    humidity: int
    ph: float
    rainfall: int


class AnalyzeRequest(BaseModel):
    soil_data: SoilData


class SuggestRequest(BaseModel):
    crop: str
    soil_data: SoilData


# -----------------------------
# Health check
# -----------------------------
@app.get("/")
def root():
    return {"status": "API running"}


# -----------------------------
# ANALYZE
# -----------------------------
@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    soil_dict = request.soil_data.dict()
    crops = recommend_top3_crops(soil_dict)

    try:
        save_analysis_to_cloud(soil_dict, crops)
    except Exception as e:
        print("⚠️ Firebase error (analyze):", e)

    return {"top_3_crops": crops}


# -----------------------------
# SUGGEST
# -----------------------------
@app.post("/suggest")
def suggest(request: SuggestRequest):
    soil_dict = request.soil_data.dict()
    result = get_soil_advice(request.crop, soil_dict)

    try:
        save_suggestion_to_cloud(
            soil_dict,
            request.crop,
            result["suggestions"]
        )
    except Exception as e:
        print("⚠️ Firebase error (suggest):", e)

    return result


# -----------------------------
# HISTORY
# -----------------------------
@app.get("/history")
def history(limit: int = Query(10, ge=1, le=50)):
    try:
        records = fetch_history(limit)
        return {
            "count": len(records),
            "records": records
        }
    except Exception as e:
        print("❌ Firebase error (history):", e)
        return {
            "count": 0,
            "records": [],
            "error": "Unable to fetch history"
        }
