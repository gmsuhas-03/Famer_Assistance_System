# test_api.py
import requests

url = "http://127.0.0.1:8000/soil-advice"

payload = {
    "crop": "rice",
    "soil_data": {
        "N": 60,
        "P": 30,
        "K": 35,
        "ph": 5.0,
        "rainfall": 120
    }
}

response = requests.post(url, json=payload)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())
