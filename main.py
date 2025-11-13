from fastapi import FastAPI, HTTPException, Query
import requests
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# ------------------------------
# Load environment variables
# ------------------------------
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError("Missing OPENROUTER_API_KEY. Please set it in your .env file.")

# ------------------------------
# FastAPI initialization
# ------------------------------
app = FastAPI(title="Aurora QA API", version="0.3.0")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    default_headers={
        "HTTP-Referer": "https://myapp.com",
        "X-Title": "Aurora QA API"
    }
)



@app.get("/")
def root():
    return {"status": "ok", "message": "Aurora QA API running."}