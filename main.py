import requests
from datetime import datetime
import os

GENDER = "male"
WEIGHT_KG = 91
HEIGHT_CM = 185
AGE = 35

APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]
TOKEN = os.environ["TOKEN"]

endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = os.environ["SHEET_ENDPOINT"]

headers_auth = {"Authorization": f"Bearer {os.environ['TOKEN']}"}

exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

request_body = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}



response = requests.post(endpoint, json=request_body, headers=headers)
result = response.json()
print(result['exercises'])

current_day = datetime.now().strftime('%d/%m/%Y')
current_time = datetime.now().strftime("%X")

for exercise in result['exercises']:
    body = {
        "workout": {
            "date": current_day,
            "time": current_time,
            "exercise": exercise['name'],
            "duration": exercise['duration_min'],
            "calories": exercise['nf_calories']
        }
    }

    sheet_response = requests.post(sheet_endpoint, json=body, headers=headers_auth)
    print(sheet_response.text)
