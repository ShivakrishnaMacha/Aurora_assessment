from fastapi import FastAPI, HTTPException
from openai import OpenAI
from dotenv import load_dotenv
import requests
import os
import json

# Load env
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError("Missing OPENROUTER_API_KEY. Please set it in your .env file.")

app = FastAPI(title="Aurora QA API", version="0.2.1")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

MESSAGES_API_URL = "https://november7-730026606190.europe-west1.run.app/messages"
CACHE_FILE = "messages_cache.json"

def fetch_messages(skip=0, limit=100):
    try:
        res = requests.get(MESSAGES_API_URL, params={"skip": skip, "limit": limit}, timeout=10)
        res.raise_for_status()
        return res.json().get("items", [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching messages: {e}")

def fetch_all_messages():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                cached = json.load(f)
            return cached
        except Exception:
            pass

    all_msgs = []
    skip = 0
    while True:
        batch = fetch_messages(skip=skip, limit=100)
        if not batch:
            break
        all_msgs.extend(batch)
        skip += 100

    with open(CACHE_FILE, "w") as f:
        json.dump(all_msgs, f)
    return all_msgs

@app.get("/")
def root():
    return {"status": "ok"}
