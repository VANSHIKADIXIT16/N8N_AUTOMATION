import requests
import os
from dotenv import load_dotenv

load_dotenv()

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

def trigger_n8n_workflow(data: dict):
    if not N8N_WEBHOOK_URL:
        print("⚠ N8N_WEBHOOK_URL not set. Skipping workflow trigger.")
        return None
    
    try:
        response = requests.post(N8N_WEBHOOK_URL, json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error triggering n8n workflow: {str(e)}")
        return None
