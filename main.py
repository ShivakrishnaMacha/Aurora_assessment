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





@app.get("/")
def root():
    return {"status": "ok", "message": "Aurora QA API running."}