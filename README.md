# AI-Powered Q&A API Project

---

## Description
This project is a **Python FastAPI API** designed to answer user questions using a **Large Language Model (LLM)**, augmented by a custom **knowledge base** from `knowledge_base.txt`.

---

## Technologies Used
* **Python**
* **FastAPI**
* **OpenAI API**
* **Git & GitHub**

---

## How to Run Locally

1.  **Clone:** `git clone https://github.com/WaleedBarmo/AI-Powered-QnA-API.git && cd AI-Powered-QnA-API`
2.  **Virtual Environment:** `python -m venv venv` then `.\venv\Scripts\activate` (Windows) or `source venv/bin/activate` (macOS/Linux).
3.  **Install Dependencies:** `pip install "fastapi[all]" openai`
4.  **Set OpenAI Key:** `$env:OPENAI_API_KEY="YOUR_API_KEY"` (Windows) or `export OPENAI_API_KEY='YOUR_API_KEY'` (macOS/Linux).
5.  **Run API:** `uvicorn main:app --reload` (API runs at `http://127.0.0.1:8000`)

---

## How to Test
Access Swagger UI at `http://127.0.0.1:8000/docs`, use `POST /ask` with a JSON request body like `{"message": "Your question here"}`.

---

## Author
**Waleed Barmo**
Email: mohamad.mwb.90@gmail.com
GitHub: [https://github.com/WaleedBarmo](https://github.com/WaleedBarmo)