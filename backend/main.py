import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Import AI Libraries
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Load the keys from .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# 2. Setup the App
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Initialize the Brain (Gemini Model)
# "gemini-pro" is the text model.
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

@app.get("/")
def read_root():
    return {"status": "AI Ready"}

@app.get("/search")
def ask_ai(query: str):
    print(f"User asked: {query}")
    
    # 4. Ask Gemini the question directly
    # (Note: It doesn't know specific Indian laws perfectly yet, but it will try)
    response = llm.invoke(query)
    
    return {
        "result": response.content,
        "source": "AI General Knowledge (No RAG yet)"
    }