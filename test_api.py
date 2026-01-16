
import requests
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GEMINI_API_KEY")

def test_model(name):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{name}:generateContent?key={key}"
    try:
        r = requests.post(url, json={"contents": [{"parts": [{"text": "Hello"}]}]})
        print(f"{name}: {r.status_code}")
        if r.status_code == 200:
            print("Response:", r.json())
        else:
            print("Error:", r.text)
    except Exception as e:
        print(f"Exception: {e}")

test_model("gemini-1.5-flash")
test_model("gemini-pro")
