# 💰 Money Logix – AI Financial Research Assistant

An AI-powered financial research assistant that enables users to ask natural language questions about companies and receive context-aware answers using Retrieval-Augmented Generation (RAG).

---

## 🚀 Features

- 🤖 AI-powered financial question answering
- 📈 Company-specific analysis
- 📰 Recent news retrieval
- 📊 Quarterly results summarization
- 📚 Company knowledge base
- 🔍 Semantic search using vector embeddings
- ⚡ Streaming AI responses
- 💬 Modern React chat interface
- 🔗 FastAPI backend with REST APIs

---

# 🏗️ Architecture

```
                +----------------------+
                |     React (Vite)     |
                +----------+-----------+
                           |
                           |
                     REST API
                           |
                           ▼
                +----------------------+
                |      FastAPI         |
                +----------+-----------+
                           |
          +----------------+----------------+
          |                                 |
          ▼                                 ▼
  Sentence Transformer             MongoDB
      Embeddings
          |
          ▼
      ChromaDB
(Vector Database)
          |
          ▼
    Relevant Context
          |
          ▼
      Groq LLM
          |
          ▼
    AI Generated Answer
```

---

# 🛠 Tech Stack

### Frontend

- React
- Vite
- CSS
- Fetch API

### Backend

- FastAPI
- Python

### AI

- Groq LLM
- Sentence Transformers
- ChromaDB
- Retrieval-Augmented Generation (RAG)

### Database

- MongoDB

---

# 📂 Project Structure

```
Money Logix
│
├── backend
│   ├── app
│   │   ├── routes
│   │   ├── services
│   │   ├── config
│   │   └── schemas
│   │
│   ├── reports
│   ├── chroma_db
│   ├── requirements.txt
│   └── seed_reports.py
│
├── frontend
│   ├── src
│   ├── public
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

# ⚙️ Installation

## 1. Clone repository

```bash
git clone https://github.com/vinay-271/ai-research-assistant.git

cd ai-research-assistant
```

---

## 2. Backend Setup

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

---

## 3. Configure Environment Variables

Create a `.env` file inside the backend folder.

Example:

```env
GROQ_API_KEY=your_groq_api_key
MONGODB_URI=your_mongodb_connection_string
DATABASE_NAME=financial_db
```

---

## 4. Seed Company Reports

```bash
python seed_reports.py
```

---

## 5. Run Backend

```bash
uvicorn app.main:app --reload
```

Runs at

```
http://localhost:8000
```

Swagger Documentation

```
http://localhost:8000/docs
```

---

## 6. Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Runs at

```
http://localhost:5173
```

---

# 📚 Knowledge Base

The assistant currently supports company analysis using:

- Company Overview
- Quarterly Results
- Recent News
- Financial Metrics
- Competitive Advantages

Supported companies include:

- Asian Paints
- TCS
- Reliance
- Infosys
- HDFC Bank
- ICICI Bank
- ITC
- Kotak Bank
- SBI
- NTPC
- Sun Pharma
- Tata Motors
- UltraTech Cement
- Axis Bank
- Bajaj Finance
- Larsen & Toubro
- Mahindra & Mahindra
- Maruti Suzuki

---

# 💡 Example Questions

```
Tell me about Asian Paints

What happened in October?

Summarize TCS quarterly results.

What are the competitive advantages of ITC?

Should I invest in Reliance?
```

---

# 📸 Screenshots

> <img width="1342" height="590" alt="image" src="https://github.com/user-attachments/assets/2d5864df-6c7d-4aea-ba61-5d10e9eec6f6" />
> <img width="1366" height="606" alt="image" src="https://github.com/user-attachments/assets/3c7af3f3-d83e-4c6a-b345-a9960e0970ed" />
> <img width="428" height="159" alt="image" src="https://github.com/user-attachments/assets/51ab0498-3d90-4531-ab40-d2828ace8abf" />
> <img width="1265" height="634" alt="image" src="https://github.com/user-attachments/assets/c8f605d7-e194-4517-a685-b438e20c527b" />





---

# 👨‍💻 Contributors

- Panshul (@crazyluhsnap) — Backend Development and debugging
- Vertika  — AI+LLM and integration with backend
- Vinay & Ishant — Frontend & integration with backend

---

# 📜 License

This project was developed as part of a Placement Hackathon.

For educational purposes only.
