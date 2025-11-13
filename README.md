# 🧠 Aurora QA API

A **question-answering microservice** built with **FastAPI** and **OpenRouter** that can infer answers to natural-language questions based on member messages fetched from a public dataset.

🌐 **Live Demo:** [https://aurora-assessment.onrender.com](https://aurora-assessment.onrender.com)  
📘 **API Docs:** [https://aurora-assessment.onrender.com/docs](https://aurora-assessment.onrender.com/docs)


For example:
> - “When is Layla planning her trip to London?”  
> - “How many cars does Vikram Desai have?”  
> - “What are Amira’s favorite restaurants?”

---

## 🚀 Overview

This service fetches member messages from a provided public API and uses a **Large Language Model (LLM)** (via OpenRouter’s API) to infer answers from those messages.  

It exposes a single endpoint `/ask` that accepts a question and responds with a concise, factual answer based only on the messages.

---

## 🧩 Example Usage

### Endpoint
GET /ask?question=When%20is%20Layla%20planning%20her%20trip%20to%20London%3F


### Example Response
```json
{
  "answer": "Layla is planning her trip to London in December."
}
If the information is not available:
{
  "answer": "I don't know."
}
```

## Setup Instructions

1️⃣ Clone the repository
```
git clone https://github.com/<your-username>/aurora-qa-api.git
cd aurora-qa-api
```
2️⃣ Create and activate a virtual environment
```
python3 -m venv venv
source venv/bin/activate
```
3️⃣ Install dependencies
```
pip install -r requirements.txt
```
4️⃣ Create .env file
```
OPENROUTER_API_KEY=your_api_key_here
```
5️⃣ Run the service locally
```
uvicorn main:app --reload
```
The API will be available at:
👉 http://127.0.0.1:8000

Deployed version (Render):
👉 https://aurora-assessment.onrender.com


##🧠 How It Works
1️⃣ Fetching Data

The app retrieves member messages from:
```
https://november7-730026606190.europe-west1.run.app/messages
```
It paginates through results and caches them locally in messages_cache.json for faster subsequent queries.

2️⃣ Building Context

All messages are combined into a contextual text block:
```
<user_name>: <message>
<user_name>: <message>
```

3️⃣ Question Processing

When a question is received at /ask, the system sends both:

- the question, and
- the concatenated message context
to OpenRouter’s LLM (Llama 3.3-70B-Instruct) model.

4️⃣ Response Filtering

The LLM is prompted to:

- Only use information explicitly present in the messages
- Return “I don’t know.” if uncertain


## 🔍 API Documentation

| Endpoint | Method | Description |
|-----------|--------|-------------|
| `/` | GET | Health check |
| `/ask` | GET | Ask a question about the member messages |

### Parameters

| Name | Type | Required | Description |
|------|------|-----------|-------------|
| `question` | string | ✅ | Natural language question to be answered |

---

## 🧪 Example Queries

| Question | Example Answer |
|-----------|----------------|
| When is Layla planning her trip to London? | “Layla is planning her trip to London in December.” |
| How many cars does Vikram Desai have? | “Vikram Desai has 2 cars.” |
| What are Amira’s favorite restaurants? | “Amira’s favorite restaurants are Nobu and Dishoom.” |
| Who is going to Japan next month? | “I don't know.” |

## 🧩 Bonus 1: Design Notes

### 🏗️ Approach 1 — LLM-based Retrieval (✅ Chosen)

- Fetch all messages and use an LLM (via OpenRouter) to interpret the answer.  
- Simple to implement, flexible, and leverages model reasoning.  
- **Drawback:** Context window limits when message history grows very large.  

---

### 🧮 Approach 2 — Embedding Search + LLM

- Pre-compute embeddings for all messages (e.g., using OpenAI embeddings).  
- On query, find top-N relevant messages and send only those to the model.  
- More scalable but more complex to implement.  

---

### 📊 Approach 3 — Rule-based Extraction

- Use regex / keyword matching to infer structured facts.  
- Efficient but brittle and less adaptable to natural language.  

---

### ✅ Final Decision

> **Approach 1** — chosen because the dataset is small enough and prioritizing correctness & simplicity fits the assessment goals.

---

## 🔎 Bonus 2: Data Insights

After analyzing the dataset returned by the `/messages` API:

- Some users have incomplete or inconsistent message patterns (e.g., missing user names or truncated messages).  
- Certain members appear multiple times under slightly different spellings (e.g., “Layla M.” vs “Layla Malik”).  
- Occasional duplicate or contradictory entries (e.g., two different trip dates for the same person).  
- Some messages include non-standard formatting (extra emojis, multiple question marks, etc.), which can affect LLM parsing.  

🧩 These inconsistencies suggest the data likely originated from conversational logs, not structured forms.

---

## 🧰 Tech Stack

| Component | Description |
|------------|-------------|
| **Language** | Python 3.10+ |
| **Framework** | FastAPI |
| **LLM Provider** | OpenRouter (Llama 3.3-70B-Instruct) |
| **Env Management** | python-dotenv |
| **HTTP Requests** | requests |
| **Server** | uvicorn |

---

## 📦 Project Structure

```text
aurora-qa-api/
│
├── main.py                # FastAPI app entry point
├── requirements.txt       # Dependencies
├── .env                   # Environment variables (excluded from git)
├── .gitignore             # Ignore rules
├── messages_cache.json    # Cached dataset (excluded)
└── README.md              # Documentation
```


---

## 🧪 Testing Locally

Run the development server:

```bash
uvicorn main:app --reload
```
Then open:

API Docs: http://127.0.0.1:8000/docs

Example Query:
http://127.0.0.1:8000/ask?question=When%20is%20Layla%20planning%20her%20trip%20to%20London%3F



