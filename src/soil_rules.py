def get_soil_advice(crop: str, soil_data: dict):
    """
    Crop-specific soil & fertilizer recommendations (kg/acre)
    """

    suggestions = []

    N = soil_data["N"]
    P = soil_data["P"]
    K = soil_data["K"]
    ph = soil_data["ph"]
    rainfall = soil_data["rainfall"]

    crop = crop.lower()

    # --------------------------------
    # Base fertilizer requirements (kg/acre)
    # --------------------------------
    crop_requirements = {
        "rice":      {"N": 100, "P": 50, "K": 50},
        "maize":     {"N": 80,  "P": 40, "K": 40},
        "wheat":     {"N": 90,  "P": 45, "K": 45},
        "banana":    {"N": 120, "P": 60, "K": 80},
        "cotton":    {"N": 75,  "P": 35, "K": 35},
        "chickpea":  {"N": 30,  "P": 50, "K": 20},
        "jute":      {"N": 60,  "P": 30, "K": 30}
    }

    req = crop_requirements.get(crop)

    # --------------------------------
    # Nitrogen
    # --------------------------------
    if req:
        if N < req["N"] * 0.4:
            suggestions.append(f"Nitrogen VERY LOW → Apply Urea 45 kg/acre for {crop}")
        elif N < req["N"] * 0.6:
            suggestions.append(f"Nitrogen LOW → Apply Urea 30 kg/acre for {crop}")

    # --------------------------------
    # Phosphorus
    # --------------------------------
    if req:
        if P < req["P"] * 0.4:
            suggestions.append(f"Phosphorus VERY LOW → Apply DAP 40 kg/acre for {crop}")
        elif P < req["P"] * 0.6:
            suggestions.append(f"Phosphorus LOW → Apply DAP 25 kg/acre for {crop}")

    # --------------------------------
    # Potassium
    # --------------------------------
    if req:
        if K < req["K"] * 0.4:
            suggestions.append(f"Potassium VERY LOW → Apply MOP 35 kg/acre for {crop}")
        elif K < req["K"] * 0.6:
            suggestions.append(f"Potassium LOW → Apply MOP 20 kg/acre for {crop}")

    # --------------------------------
    # pH correction (common)
    # --------------------------------
    if ph < 5.5:
        suggestions.append("Soil highly acidic → Apply Lime 200 kg/acre")
    elif ph < 6.0:
        suggestions.append("Soil acidic → Apply Lime 100 kg/acre")
    elif ph > 7.5:
        suggestions.append("Soil alkaline → Apply Gypsum 100 kg/acre")

    # --------------------------------
    # Rainfall / irrigation
    # --------------------------------
    if rainfall < 100:
        suggestions.append("Low rainfall → Provide supplemental irrigation")

    # --------------------------------
    # Fallback
    # --------------------------------
    if not suggestions:
        suggestions.append(f"Soil conditions are suitable for cultivating {crop}")

    return {
        "crop": crop,
        "suggestions": suggestions
    }
