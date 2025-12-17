# ⚖️ NYAYA.ai: Legal Intelligence for The Next Generation

![Status](https://img.shields.io/badge/status-active-success.svg) ![Python](https://img.shields.io/badge/python-3.11-blue.svg) ![FastAPI](https://img.shields.io/badge/FastAPI-v0.100+-005571.svg) ![LLM](https://img.shields.io/badge/LLM-Llama--3.3--70B-orange) ![Pinecone](https://img.shields.io/badge/Vector%20DB-Pinecone-blueviolet)

**NYAYA.ai** is a revolutionary, full-stack legal companion designed to democratize justice. By leveraging **Retrieval-Augmented Generation (RAG)**, it simplifies complex legal procedures, providing citizens and professionals with instant, accurate insights into the Indian Constitution and the new **Bhartiya Nyaya Sanhita (BNS)**.

> **"Justice Democratized."**

---

## 📸 Interface Preview

### 🏠 Landing Dashboard
The gateway to legal intelligence, featuring real-time updates and core legal metrics.
![NYAYA.ai Home]<img width="1832" height="1042" alt="Screenshot 2025-12-17 222043" src="https://github.com/user-attachments/assets/463acd4d-27d3-40c8-9871-1ecc07dc2ffc" /> 
*Current Scale: 395+ Articles | 15,000+ Precedents | 98% Accuracy*

### 💬 BNS Code Conversational AI
An advanced chat interface for deep legal querying, document analysis, and simplified explanations.
![BNS Code Chat]<img width="1881" height="1038" alt="Screenshot 2025-12-17 222133" src="https://github.com/user-attachments/assets/1867695a-84fd-4f60-a58b-2863fc2f2960" /> 
*Example: Real-time analysis of Article 21 (Protection of Life and Personal Liberty).*

---

## 🚀 Key Features

### 🧑‍⚖️ Virtual Intelligence
* **AI Judge (Verdict Predictor):** Analyzes case scenarios to identify applicable sections under the new **BNS (2023)** and predicts likely legal outcomes and bail eligibility.
* **Semantic Legal Search:** Navigate 395+ constitutional articles using natural language queries—no exact legal citations required.
* **BNS Code Assistant:** A dedicated module specifically designed to handle the transition from the IPC to the new Bhartiya Nyaya Sanhita framework.
* **Jargon Simplifier:** Converts dense, "legalese" court judgments into plain, actionable language.

### 📝 Legal Drafting & Analysis
* **Automated Document Drafter:** Instantly generates professional legal templates (Agreements, Affidavits, Petitions) with dynamic AI guidance.
* **PDF Analysis (OCR):** Upload legal notices, FIRs, or contracts directly via the attachment tool (📎). The AI extracts text, evaluates risks, and highlights critical deadlines.
* **Instant PDF Export:** Export AI-generated drafts directly to professional PDF format with a single click.

### 🎨 UI/UX & Accessibility
* **SaaS Style Dashboard:** Sleek, dark-themed interface with a live ticker for Supreme Court updates and e-filing news.
* **Multilingual Voice Search:** Integrated **Speech-to-Text** (🎤) supporting Hinglish and Hindi for enhanced accessibility.
* **Quick-Action Chips:** One-tap buttons for trending legal topics like "Murder Punishment," "Cyber Crime," and "Self Defense."

---

## 🏗️ Technical Architecture (RAG Pipeline)

NYAYA.ai ensures legal precision by eliminating AI hallucinations through a verified Retrieval-Augmented Generation pipeline:

1.  **Vectorization:** Legal datasets (Constitution, BNS Acts, 15,000+ Precedents) are converted into high-dimensional vectors using `all-mpnet-base-v2`.
2.  **Storage:** Vectors are indexed in a **Pinecone Vector Database** for sub-second similarity retrieval.
3.  **Retrieval:** When a query is made, the system fetches the most mathematically relevant legal context.
4.  **Augmentation & Generation:** The retrieved context is processed by **Llama 3.3 (via Groq)** to generate a verified, professional, and cited response.

---

## 📂 Project Structure

samvidhan-ai/
├── backend/            # FastAPI Server
│   ├── main.py         # Primary API endpoints
│   ├── venv/           # Virtual Environment
│   ├── .env            # API Keys (Protected)
│   └── requirements.txt
├── frontend/           # UI Workspace
│   ├── index.html      # Main Dashboard
│   ├── style.css       # Glassmorphism UI logic
│   └── script.js       # Frontend API handlers
├── data/               # Legal PDF Datasets
└── README.md           # Project Documentation
## 🛠️ Tech Stack

---

| Layer | Technology |
| :--- | :--- |
| **Frontend** | HTML5, CSS3 (Advanced Gradients & Glassmorphism), JS (ES6+) |
| **Backend** | Python 3.11, FastAPI, Uvicorn |
| **AI Brain** | Llama 3.3 70B (Groq Cloud API) |
| **Vector DB** | Pinecone (Serverless Vector Search) |
| **Embeddings** | HuggingFace Sentence Transformers |
| **Processing** | PyPDF (Server-side OCR) & HTML2PDF.js (Client-side Export) |

---

## ⚙️ Installation & Setup

### Prerequisites
* Python 3.11+
* Groq API Key
* Pinecone API Key

### Steps
1.  **Clone the Repo:** ```bash
    git clone [https://github.com/your-username/samvidhan-ai.git](https://github.com/your-username/samvidhan-ai.git)
    cd samvidhan-ai
    ```
2.  **Install Backend Environment:** ```bash
    cd backend
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    # source venv/bin/activate # Mac/Linux
    pip install -r requirements.txt
    ```
3.  **Environment Variables:** Create a `.env` file in `backend/` and add:
    ```env
    GROQ_API_KEY=your_key_here
    PINECONE_API_KEY=your_key_here
    ```
4.  **Launch:** ```bash
    # Start Backend
    python -m uvicorn main:app --reload
    ```
    Open `frontend/index.html` in your browser to begin.

---

Roadmap & Future Vision
[x] Phase 1: Core RAG pipeline and BNS/IPC mapping.

[x] Phase 2: Automated Document Drafting.

[ ] Phase 3: Support for 12+ regional Indian languages via Whisper API.

[ ] Phase 4: Fine-tuning on 50,000+ landmark Supreme Court judgments.

[ ] Phase 5: Mobile App (iOS/Android) using Flutter.

---

## 📜 Disclaimer
*NYAYA.ai is an experimental tool provided for educational and informational purposes only. It does not constitute formal legal advice. Always consult a certified legal professional for official matters. Predictions made by the AI Judge are based on data patterns and do not guarantee actual court outcomes.*

---
**Developed by Priyank Solanki with ❤️ for Legal Literacy in India** 🇮🇳
