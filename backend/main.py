import os
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Setup Services
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("samvidhan-index")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# --- CHANGE IS HERE: Use 'gemini-1.5-flash' (Higher limits, Faster) ---
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", google_api_key=GOOGLE_API_KEY)

# 2. Load BNS Data
bns_path = "data/bns_mapping.json"
if os.path.exists(bns_path):
    with open(bns_path, "r") as f:
        BNS_DATA = json.load(f)
else:
    BNS_DATA = [] # Fallback if file missing

@app.get("/search")
def search_law(query: str, mode: str = "constitution"):
    print(f"\n🔎 User asked: {query} [Mode: {mode}]")
    
    # --- MODE A: CONSTITUTION (RAG) ---
    if mode == "constitution":
        print(f"\n🔎 User asked: {query}")
    
        try:
            # STEP 1: Search using Local Embeddings
            query_vector = embeddings.embed_query(query)
            search_results = index.query(vector=query_vector, top_k=3, include_metadata=True)
            
            context_text = ""
            sources = []
            for match in search_results['matches']:
                if match['score'] > 0.30: # Slightly lower threshold for this model
                    context_text += match['metadata']['text'] + "\n\n"
                    sources.append(match['id'])

            if not context_text:
                return {"result": "I couldn't find a specific law for that. Try asking about 'Rights' or 'Arrest'.", "source": "No Match"}

            # STEP 2: Answer using Gemini
            print(f"   📚 Found context: {sources}")
            prompt = f"""
            You are a legal expert. Answer the user based ONLY on this context from the Indian Constitution:
            {context_text}
            
            Question: {query}
            3. Keep it simple and mention the Article number.
            """
            
            response = llm.invoke(prompt)
            
            return {
                "result": response.content,
                "source": f"Sources: Article {', '.join(sources)}"
            }
        
        except Exception as e:
            print(f"❌ Error: {e}")
            return {"result": "System Error. Please check backend logs.", "source": "Error"}   

    # --- MODE B: IPC vs BNS (New Laws) ---
    elif mode == "bns":
        query = query.lower()
        found_law = None
        
        for law in BNS_DATA:
            for keyword in law["keywords"]:
                if keyword in query:
                    found_law = law
                    break
            if found_law: break
        
        if found_law:
            return {
                "result": f"""
                **Topic:** {found_law['topic']}
                
                🔴 **Old Law (IPC):** {found_law['ipc']}
                🟢 **New Law (BNS):** {found_law['bns']}
                
                **Change:** {found_law['desc']}
                """,
                "source": "Bhartiya Nyaya Sanhita (2023)"
            }
        else:
            return {
                "result": "I have data for Murder (302), Cheating (420), Sedition, and Rape. Ask me about one of those.",
                "source": "BNS Database"
            }