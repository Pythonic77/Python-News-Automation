
import requests
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("OPENROUTER_API_KEY")

def list_models():
    url = "https://openrouter.ai/api/v1/models"
    headers = {"Authorization": f"Bearer {key}"}
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            models = r.json()['data']
            print(f"Found {len(models)} models.")
            # Print first 10 free ones
            free_models = [m['id'] for m in models if ':free' in m['id']]
            print("Free models:", free_models[:10])
            
            # Print google ones
            google_models = [m['id'] for m in models if 'google/' in m['id']]
            print("Google models:", google_models[:5])
        else:
            print(f"Error listing models: {r.status_code} {r.text}")
    except Exception as e:
        print(f"Exception: {e}")

list_models()
