import os
import json
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone

load_dotenv()

# 1. Connect to Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("samvidhan-index")

# 2. Setup Embeddings (Turning text into numbers)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# 3. Load Data (Adjust filename as needed)
with open("data/constitution.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 4. Upload Loop (Simplified)
print("Starting upload...")
vectors = []
for i, article in enumerate(data):
    text = f"Article {article.get('id')}: {article.get('text')}"
    
    # Turn text into numbers
    vector = embeddings.embed_query(text)
    
    # Prepare for upload
    vectors.append({
        "id": str(i),
        "values": vector,
        "metadata": {"text": text}
    })
    
    # Upload in batches of 50
    if len(vectors) >= 50:
        index.upsert(vectors)
        vectors = []
        print(f"Uploaded batch {i}")

print("Upload Complete!")