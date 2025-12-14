from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# --- CORS SETTINGS ---
# This allows Member 2's frontend (running on localhost) to talk to your backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins (simplest for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "active", "message": "Samvidhan-AI Backend is running!"}

@app.get("/search")
def search_law(query: str):
    # This is where the AI logic will go later.
    # For now, we return a dummy response to test the connection.
    print(f"User asked: {query}")
    
    return {
        "result": f"Answer for '{query}': According to Article 21 of the Constitution, every citizen has the right to life and personal liberty.",
        "source": "Constitution of India, Part III, Article 21"
    }