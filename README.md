# Money Logix — AI Financial Assistant 📈

Money Logix is a premium, end-to-end AI-powered financial research assistant. It features a RAG (Retrieval-Augmented Generation) pipeline backend built in Python (FastAPI) and an interactive, highly polished, three-column analytical dashboard built in React (Vite).

---

## 🚀 Key Features

1. **Intelligent Financial RAG**: Scrapes, parses, and indexes raw company filings and news reports locally.
2. **Hybrid Storage**: Uses **MongoDB** for document metadata storage and **ChromaDB** for vector embeddings.
3. **Local Embedding Computation**: Computes text embeddings locally using the HuggingFace `sentence-transformers/all-MiniLM-L6-v2` model (no API key required).
4. **Streaming Answers**: Queries Groq API (`llama-3.3-70b-versatile` or custom) to stream synthesis answers to the client in real-time.
5. **Interactive UI Spec**: Implements a floating, fixed-viewport dashboard featuring:
   - Dynamic sidebar navigation.
   - Dual-mode light/dark theme.
   - 20-company context selector.
   - Context-aware quick actions (business segments, performance, moats, risks).
   - Rich message formatting with inline data tables, success/risk pills, and bullet layouts.
   - Client-side fallback system when backend is offline, allowing full-fidelity prototype demonstrations.

---

## 🛠️ Project Structure

```
.
├── app/                      # FastAPI Backend Code
│   ├── config/               # Database & client connections
│   ├── models/               # MongoDB models & schemas
│   ├── routes/               # API endpoints (Chat, Stocks, News, Filings)
│   ├── services/             # Core services (Embedding, RAG query, etc.)
│   └── main.py               # API Entry Point
├── reports/                  # Raw markdown report directories for 20 companies
├── frontend/                 # React + Vite Frontend App
│   ├── src/
│   │   ├── companyData.js    # Local company financial mock data matching filings
│   │   ├── App.jsx           # Main interactive UI component
│   │   ├── App.css           # UI dashboard styles
│   │   ├── index.css         # Reset & global design tokens
│   │   └── main.jsx
│   ├── index.html            # Entry HTML page (with SEO configuration)
│   └── package.json
├── requirements.txt          # Python dependencies
├── seed_reports.py           # Script to parse and index raw report documents
├── seed_alpha_vantage.py     # Script to pull data from Alpha Vantage
└── README.md
```

---

## 💻 Installation & Setup

### 1. Prerequisites
- **Python**: v3.10 or higher.
- **Node.js**: v18 or higher with `npm`.
- **MongoDB**: A running instance (local or Atlas cluster).

### 2. Backend Setup
1. Initialize the virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory:
   ```env
   MONGODB_URL=mongodb://localhost:27017
   DATABASE_NAME=financial_assistant
   GROQ_API_KEY=your_groq_api_key_here
   GROQ_LLM_MODEL=llama-3.3-70b-versatile
   ```
4. Seed the database with the pre-existing company reports in the `reports/` folder:
   ```bash
   python seed_reports.py
   ```
5. Start the FastAPI backend server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   *Your backend API will now be running on [http://localhost:8000](http://localhost:8000)*.

---

### 3. Frontend Setup
1. Navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   *Your frontend dashboard will now be live on [http://localhost:5173](http://localhost:5173)*.

---

## 🎨 UI Specifications Implemented

- **Color Tokens**: Dark Navy sidebar (`#0F1024`), white chat space (`#FFFFFF`), light gray backdrop (`#EEF0F5`), violet accents (`#6D5EF0`).
- **Sidebar**: Logo with gradient icon, active navigation highlighting, bottom promotional card, and copyright details.
- **Header**: Avatar identifier, greeting, and a dynamic Sun/Moon light-dark mode toggle.
- **Right Panel**: Stacked info cards featuring Company profile, Market cap & financial ratios, related files, and disclaimer tags.
- **Chat Workspace**: High-fidelity messaging system with user message bubbles, assistant streaming answers, data tables with success-green (`+YoY`) and danger-red (`-YoY`) change indicators, and quick action chips.

---
