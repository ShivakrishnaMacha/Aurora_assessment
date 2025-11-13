from fastapi import FastAPI, HTTPException, Query
import requests
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError("Missing OPENROUTER_API_KEY. Please set it in your .env file.")

app = FastAPI(title="Aurora QA API", version="0.3.0")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    default_headers={
        "HTTP-Referer": "https://myapp.com",
        "X-Title": "Aurora QA API"
    }
)

MESSAGES_API_URL = "https://november7-730026606190.europe-west1.run.app/messages"
CACHE_FILE = "messages_cache.json"

def fetch_messages(skip=0, limit=100):
    try:
        response = requests.get(
            MESSAGES_API_URL,
            params={"skip": skip, "limit": limit},
            timeout=10
        )
        response.raise_for_status()
        return response.json().get("items", [])
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

    all_messages = []
    skip = 0
    while True:
        batch = fetch_messages(skip=skip, limit=100)
        if not batch:
            break
        all_messages.extend(batch)
        skip += 100

    with open(CACHE_FILE, "w") as f:
        json.dump(all_messages, f)
    return all_messages

def extract_answer(question, messages):
    if not messages:
        return "I don't know."

    context = "\n".join([f"{m['user_name']}: {m['message']}" for m in messages])
    prompt = f"""
You are a helpful assistant. Answer the question based only on the messages below.
If the answer is not explicitly stated, reply exactly with "I don't know."

Messages:
{context}

Question: {question}

Answer concisely:
"""

    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3.3-70b-instruct:free",
            messages=[
                {"role": "system", "content": "You are a factual assistant that only answers using the provided messages."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answer: {e}")

@app.get("/ask")
def ask(question: str = Query(..., description="Ask a question about the messages")):
    messages = fetch_all_messages()
    answer = extract_answer(question, messages)
    return {"answer": answer}

@app.get("/")
def root():
    return {"status": "ok", "message": "Aurora QA API running."}
