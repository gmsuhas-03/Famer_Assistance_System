from datetime import datetime
from database.firebase_db import get_firestore_client


# ---------------------------
# Save analyze data
# ---------------------------
def save_analysis_to_cloud(soil_data: dict, crops: list):
    db = get_firestore_client()

    record = {
        "type": "analyze",
        "timestamp": datetime.utcnow().isoformat(),
        "soil_data": soil_data,
        "top_3_crops": crops
    }

    db.collection("farmer_records").add(record)


# ---------------------------
# Save suggestion data
# ---------------------------
def save_suggestion_to_cloud(soil_data: dict, crop: str, suggestions: list):
    db = get_firestore_client()

    record = {
        "type": "suggest",
        "timestamp": datetime.utcnow().isoformat(),
        "soil_data": soil_data,
        "crop": crop,
        "suggestions": suggestions
    }

    db.collection("farmer_records").add(record)


# ---------------------------
# Fetch history
# ---------------------------
def fetch_history(limit: int = 10):
    db = get_firestore_client()

    docs = (
        db.collection("farmer_records")
        .order_by("timestamp", direction="DESCENDING")
        .limit(limit)
        .stream()
    )

    history = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        history.append(data)

    return history
