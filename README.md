# LLM Test Generator

Automatically generate structured API test cases from an OpenAPI spec using Claude.

---

## Overview

LLM Test Generator ingests an OpenAPI specification, parses each endpoint, and uses Anthropic Claude to generate structured test cases covering happy path scenarios, edge cases, and error conditions. Results are returned via a FastAPI backend and displayed in a React UI grouped by endpoint.

## Tech Stack

- **Backend:** Python, FastAPI, Anthropic Claude (via `anthropic` SDK)
- **Frontend:** React, Vite
- **Config:** `python-dotenv` for environment management

## Project Structure

```
llm-test-generator/
├── backend/
│   ├── main.py          # FastAPI app — /health and /generate endpoints
│   ├── parser.py        # Loads and parses OpenAPI spec, extracts endpoints
│   ├── generator.py     # Sends each endpoint to Claude, returns test cases
│   └── requirements.txt
├── frontend/
│   └── src/
│       └── App.jsx      # React UI — spec path input, results display
├── data/
│   └── sample_api_spec.json  # Sample OpenAPI spec for the RAG QE Knowledge Base API
└── .env                 # ANTHROPIC_API_KEY
```

## How It Works

```
OpenAPI spec file
      │
      ▼
parser.py — load_spec() + extract_endpoints()
      │
      ▼
generator.py — generate_tests() sends each endpoint to Claude
      │
      ▼
main.py — POST /generate returns { "endpoints": [...] }
      │
      ▼
React UI — displays test cases grouped by endpoint
```

Each test case includes a name, description, expected HTTP status, and expected behavior.

## Getting Started

### Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Add your Anthropic API key to .env
echo "ANTHROPIC_API_KEY=your_key_here" > ../.env

uvicorn main:app --port 8001 --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The UI runs at `http://localhost:5173` and connects to the backend at `http://3.21.168.210:8001` by default (the deployed EC2 endpoint).

## Deployment

The backend is deployed on AWS EC2 (Ubuntu 24.04, t2.micro). The FastAPI server runs on port 8001 and is accessible at `http://3.21.168.210:8001`.

To start the server on EC2:

```bash
ssh -i llm-test-generator-key.pem ubuntu@3.21.168.210
cd llm-test-generator/backend
source ../venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8001
```

## Example

A sample OpenAPI spec for the **RAG QE Knowledge Base API** is included at `data/sample_api_spec.json`. Use it as a starting point to see the full pipeline in action — enter the path in the UI and click **Generate Tests**.
