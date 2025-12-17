import os
import io
import json
import random
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from pypdf import PdfReader 

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Setup Pinecone & Embeddings
try:
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index("samvidhan-index")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    DB_STATUS = True
except:
    print("⚠️ Database offline. Switching to Pure AI Mode.")
    DB_STATUS = False

# 2. THE PROFESSIONAL BRAIN
llm = ChatGroq(
    temperature=0.6, # Slightly higher for creative glossary terms
    model_name="llama-3.3-70b-versatile", 
    groq_api_key=GROQ_API_KEY
)

# 3. BNS Reference Data
BNS_DATA = [
    {"topic": "Murder", "ipc": "Section 302", "bns": "Section 103", "desc": "Punishment for murder. New clause added for Mob Lynching (Death Penalty)."},
    {"topic": "Cheating", "ipc": "Section 420", "bns": "Section 318", "desc": "Cheating and dishonesty. Covers online scams now."},
    {"topic": "Rape", "ipc": "Section 375/376", "bns": "Section 63/64", "desc": "Stricter punishment. Identity of victim protected."},
    {"topic": "Theft", "ipc": "Section 378", "bns": "Section 303", "desc": "Theft of property. Community service added for petty theft."},
    {"topic": "Sedition", "ipc": "Section 124A", "bns": "Section 152", "desc": "Sedition repealed. Replaced by 'Acts endangering sovereignty'."},
    {"topic": "Defamation", "ipc": "Section 499", "bns": "Section 356", "desc": "Community service introduced as punishment."},
    {"topic": "Mob Lynching", "ipc": "None", "bns": "Section 103(2)", "desc": "First time specific law for Mob Lynching. Punishable by death."},
    {"topic": "Hit and Run", "ipc": "Section 304A", "bns": "Section 106(2)", "desc": "10 Years jail if driver escapes without reporting to police."}
]

# --- NEW: AI GLOSSARY ENDPOINT ---
@app.get("/glossary")
async def get_glossary():
    # Randomly pick a category to ensure variety
    categories = ["Constitutional Writs", "Latin Legal Maxims", "Criminal Law Terms", "Civil Procedure", "Corporate Law", "Human Rights"]
    selected_cat = random.choice(categories)

    prompt = f"""
    Generate 3 unique, random, and slightly complex legal terms related to '{selected_cat}' in Indian Law.
    Return ONLY a valid JSON array of objects. Do not write anything else.
    Format:
    [
        {{"term": "Term Name", "desc": "A simple 1-sentence definition for a layperson."}},
        {{"term": "Term Name", "desc": "Definition..."}},
        {{"term": "Term Name", "desc": "Definition..."}}
    ]
    """
    try:
        response = await llm.ainvoke(prompt)
        content = response.content.strip()
        # Clean JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        return json.loads(content)
    except Exception as e:
        # Fallback
        return [
            {"term": "Amicus Curiae", "desc": "A 'friend of the court' who assists the court by offering information or advice."},
            {"term": "Suo Moto", "desc": "An action taken by a court on its own authority without a formal request."},
            {"term": "Res Judicata", "desc": "A matter that has been adjudicated by a competent court and may not be pursued further."}
        ]

# --- DAILY QUIZ ENDPOINT ---
@app.get("/daily_quiz")
async def get_daily_quiz():
    topics = [
        "Fundamental Rights (Article 12-35)", 
        "Directive Principles of State Policy", 
        "The President of India's Powers",
        "New Bharatiya Nyaya Sanhita (BNS) changes", 
        "Cyber Law and IT Act 2000", 
        "Consumer Protection Rights", 
        "Right to Information (RTI)", 
        "Famous Supreme Court Judgments",
        "Arrest and Bail Procedures",
        "Women's Rights in India"
    ]
    selected_topic = random.choice(topics)

    prompt = f"""
    Generate 1 unique, challenging multiple-choice question about Indian Law.
    Topic Focus: {selected_topic}
    
    Return ONLY valid JSON in this format:
    {{
        "question": "The question text here?",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correct_index": 0,
        "explanation": "Short explanation of why."
    }}
    """
    try:
        response = await llm.ainvoke(prompt)
        content = response.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        return json.loads(content)
    except Exception as e:
        return {
            "question": "Which Article of the Indian Constitution abolishes Untouchability?",
            "options": ["Article 16", "Article 17", "Article 18", "Article 23"],
            "correct_index": 1,
            "explanation": "Article 17 explicitly abolishes untouchability."
        }

# --- PDF ANALYSIS ENDPOINT ---
@app.post("/analyze_pdf")
async def analyze_pdf(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        pdf_file = io.BytesIO(contents)
        reader = PdfReader(pdf_file)
        
        text = ""
        for page in reader.pages[:5]:
            text += page.extract_text()
            
        if not text.strip():
            return {"result": "⚠️ I couldn't read any text from this PDF. It might be an image scan.", "source": "System"}

        prompt = f"""
        You are an expert Legal Analyst.
        TASK: Analyze this uploaded legal document text.
        DOCUMENT CONTENT: {text[:6000]} 
        OUTPUT FORMAT:
        1. **Document Type:** (e.g., Rent Agreement, Court Notice)
        2. **Core Summary:** What is this document about?
        3. **Key Dates/Deadlines:** Any important dates?
        4. **Risk Analysis:** Are there any dangerous clauses?
        """
        response = await llm.ainvoke(prompt)
        return {"result": response.content, "source": f"📄 Document Analysis: {file.filename}"}

    except Exception as e:
        return {"result": f"Error analyzing PDF: {str(e)}", "source": "System Error"}


# --- SEARCH ENDPOINT ---
@app.get("/search")
async def search_law(query: str, mode: str = "constitution", lang: str = "en"):
    print(f"\n🔎 User asked: {query} [Mode: {mode}, Lang: {lang}]")

    lang_instruction = "Answer in Hindi (Devanagari script) mixed with English legal terms (Hinglish) where appropriate." if lang == "hi" else "Answer in professional English."

    # 1. DRAFTING
    draft_keywords = ["draft", "write", "create", "make", "format"]
    is_drafting = any(word in query.lower() for word in draft_keywords) and ("agreement" in query.lower() or "affidavit" in query.lower() or "application" in query.lower())

    if is_drafting:
        prompt = f"""
        You are an expert Legal Drafter.
        Task: Create a formal Indian Legal Document based on: "{query}"
        Language: {lang_instruction}
        Guidelines: Use proper legal placeholders [NAME], [DATE]. Format clearly.
        """
        response = await llm.ainvoke(prompt)
        return {"result": response.content, "source": "✨ AI Legal Drafter"}

    # 2. AI JUDGE
    if mode == "judge":
        prompt = f"""
        You are a Senior Indian Judge.
        SCENARIO: "{query}"
        TASK: Analyze under BNS/BNSS.
        LANGUAGE: {lang_instruction}
        OUTPUT: Offense Identification, Verdict Prediction, Bail Status, Next Steps.
        """
        response = await llm.ainvoke(prompt)
        return {"result": response.content, "source": "🧑‍⚖️ Virtual Judge AI"}

    # 3. SUMMARIZER
    if mode == "summarizer":
        prompt = f"""
        You are a Legal Summarizer.
        TEXT: "{query}"
        TASK: Summarize this legal text/judgment into 5 bullet points.
        LANGUAGE: {lang_instruction}
        """
        response = await llm.ainvoke(prompt)
        return {"result": response.content, "source": "📄 Case Summarizer"}

    # 4. SIMPLIFIER
    if mode == "simplify":
        prompt = f"""
        You are a Legal Translator.
        TASK: Simplify this legal text into plain language.
        TEXT: "{query}"
        LANGUAGE: {lang_instruction}
        """
        response = await llm.ainvoke(prompt)
        return {"result": response.content, "source": "📄 Legal Simplifier"}

    # 5. STANDARD SEARCH (RAG)
    context_text = ""
    sources = []

    if mode == "constitution" and DB_STATUS:
        try:
            query_vector = embeddings.embed_query(query)
            search_results = index.query(vector=query_vector, top_k=3, include_metadata=True)
            for match in search_results['matches']:
                if match['score'] > 0.30: 
                    context_text += match['metadata']['text'] + "\n\n"
                    sources.append(match['id'])
        except Exception as e:
            print(f"DB Error: {e}")

    elif mode == "bns":
        for item in BNS_DATA:
            if item['topic'].lower() in query.lower():
                context_text += f"BNS Rule: Old IPC {item['ipc']} -> BNS {item['bns']}. {item['desc']}\n"
                sources.append("BNS Database")

    if not sources: sources.append("Legal AI Knowledge Base")
    
    prompt = f"""
    You are Samvidhan AI, an Indian Legal Advisor.
    QUERY: {query}
    CONTEXT: {context_text}
    LANGUAGE: {lang_instruction}
    INSTRUCTIONS: Use the context if relevant. Otherwise use general legal knowledge. Be professional.
    """

    try:
        response = await llm.ainvoke(prompt)
        return {"result": response.content, "source": f"Source: {', '.join(sources)}"}
    except Exception as e:
        return {"result": f"System Error: {str(e)}", "source": "System"}