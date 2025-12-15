# 🇮🇳 Samvidhan AI – Intelligent Constitutional Assistant

Samvidhan AI is an **AI-powered legal assistant** built to make the **Indian Constitution accessible, understandable, and actionable** for every citizen. It leverages **Retrieval-Augmented Generation (RAG)** to fetch authentic constitutional articles and explain them in **simple, citizen-friendly language** using modern generative AI.

The system ensures **accuracy, transparency, and trust** by grounding every response directly in the Constitution of India and explicitly citing the relevant Articles.

---

## 🎯 Problem Statement

Legal language is often complex and inaccessible to non-lawyers. Citizens frequently struggle to understand:

* Their **fundamental rights**
* Legal protections during arrest or detention
* Constitutional remedies and freedoms

**Samvidhan AI bridges this gap** by transforming dense legal text into clear explanations while preserving constitutional authenticity.

---

## ✨ Key Features

### 🔍 Intelligent Constitutional Search

Ask natural language questions such as:

* *“Can I be arrested without a warrant?”*
* *“What does Article 21 protect?”*
* *“What are my fundamental rights?”*

The system retrieves **precise constitutional provisions** before generating answers.

### 🧠 RAG (Retrieval-Augmented Generation) Architecture

* Retrieves relevant Articles from a **vector database (Pinecone)**
* Uses **Google Gemini Pro** to generate contextual, easy-to-understand explanations
* Eliminates hallucinations by grounding answers in verified legal text

### ⚡ Hybrid AI Engine

* **HuggingFace local embeddings** for fast, cost-effective semantic search
* **Google Gemini** for high-quality reasoning and natural language explanations

### 📚 Source Attribution & Transparency

* Every response includes **explicit Article references** (e.g., Article 14, 19, 21)
* Promotes trust and legal authenticity

### 🎨 Modern & Responsive UI

* Clean, minimal frontend
* Real-time response and “thinking” indicators
* Optimized for desktop and mobile usage

---

## 🏗️ System Architecture

```
User Query
   ↓
Frontend (HTML/CSS/JS)
   ↓
FastAPI Backend
   ↓
Embedding Model (HuggingFace)
   ↓
Pinecone Vector Database (Constitution Articles)
   ↓
Relevant Context Retrieval
   ↓
Google Gemini (Explanation Generation)
   ↓
Answer + Article Citations
```

---

## 🛠️ Tech Stack

### Frontend

* HTML5
* CSS3
* Vanilla JavaScript

### Backend

* Python
* FastAPI
* LangChain

### AI & NLP

* **LLM:** Google Gemini Pro
* **Embeddings:** `sentence-transformers/all-mpnet-base-v2`
* **RAG Framework:** LangChain

### Database

* Pinecone (Vector Database)

---

## ⚙️ Installation & Setup

Follow the steps below to run Samvidhan AI locally.

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/PriyankSolanki9853/samvidhan-ai.git
cd samvidhan-ai
```

---

### 2️⃣ Backend Setup

```bash
cd backend
python -m venv venv
```

Activate the virtual environment:

**Windows**

```bash
venv\Scripts\activate
```

**Mac / Linux**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install fastapi uvicorn pinecone-client langchain-google-genai langchain-community python-dotenv sentence-transformers langchain-huggingface
```

---

### 3️⃣ Environment Variables

Create a `.env` file inside the `backend` folder:

```ini
GOOGLE_API_KEY=your_google_gemini_key
PINECONE_API_KEY=your_pinecone_api_key
```

---

### 4️⃣ Load the Knowledge Base

Upload the Indian Constitution data into Pinecone:

```bash
python upload_all.py
```

---

### 5️⃣ Run the Backend Server

```bash
uvicorn main:app --reload
```

Server will be available at:

```
http://127.0.0.1:8000
```

---

## 🖥️ Usage Guide

1. Ensure the **backend server is running**
2. Navigate to the `frontend` folder
3. Open `index.html` in a browser (or use VS Code Live Server)
4. Ask constitutional questions like:

   * *“What are my fundamental rights?”*
   * *“Explain Article 19 in simple terms”*
   * *“Can police arrest me without a warrant?”*

---

## 📁 Project Structure

```
samvidhan-ai/
├── backend/
│   ├── data/                # Constitution JSON files
│   ├── main.py              # FastAPI app & RAG logic
│   ├── upload_all.py        # Pinecone ingestion script
│   ├── .env                 # API keys (not committed)
│   └── requirements.txt     # Python dependencies
│
├── frontend/
│   ├── index.html           # User Interface
│   ├── style.css            # Styling
│   └── script.js            # API communication
│
└── README.md
```

---

## 🚀 Future Enhancements

* Multilingual support (Hindi & regional languages)
* Voice-based constitutional queries
* Legal scenario simulations
* Offline embedding fallback
* Public API for legal-tech integration

---

## 👥 Team

* **Backend Architect & AI Integration**
* **Frontend Developer & UI/UX Designer**

---

## ⚠️ Disclaimer

Samvidhan AI is an **educational and informational tool**. It does **not replace professional legal advice**.

---

## ❤️ Acknowledgements

Built with a vision to empower citizens and strengthen constitutional awareness.

**Made with ❤️ for India 🇮🇳**
