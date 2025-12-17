import os
import json
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings

# 1. Load Secrets
load_dotenv()
PINECONE_KEY = os.getenv("PINECONE_API_KEY")

if not PINECONE_KEY:
    print("❌ Error: PINECONE_API_KEY missing in .env")
    exit()

# 2. Setup Pinecone
pc = Pinecone(api_key=PINECONE_KEY)
index_name = "samvidhan-index"
index = pc.Index(index_name)

# 3. Setup Embeddings
print("📥 Loading Local Embedding Model...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# 4. Load Data (With Backup)
filename = "data/constitution_of_india.json"
data = []

# Try loading file
if os.path.exists(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"✅ Found file: {filename}")
    except Exception as e:
        print(f"⚠️ Error reading file: {e}")

# If file is missing or empty, USE THIS BACKUP DATA so it always answers
if not data:
    print("⚠️ File not found. Using EMERGENCY BACKUP DATA (Articles 12-35)...")
    data = [
        {"article": "Article 14", "title": "Equality before law", "description": "The State shall not deny to any person equality before the law or the equal protection of the laws within the territory of India."},
        {"article": "Article 15", "title": "Prohibition of discrimination", "description": "The State shall not discriminate against any citizen on grounds only of religion, race, caste, sex, place of birth or any of them."},
        {"article": "Article 16", "title": "Equality of opportunity in public employment", "description": "There shall be equality of opportunity for all citizens in matters relating to employment or appointment to any office under the State."},
        {"article": "Article 17", "title": "Abolition of Untouchability", "description": "Untouchability is abolished and its practice in any form is forbidden. The enforcement of any disability arising out of Untouchability shall be an offence punishable in accordance with law."},
        {"article": "Article 19", "title": "Protection of certain rights regarding freedom of speech", "description": "All citizens shall have the right (a) to freedom of speech and expression; (b) to assemble peaceably and without arms; (c) to form associations or unions."},
        {"article": "Article 21", "title": "Protection of life and personal liberty", "description": "No person shall be deprived of his life or personal liberty except according to procedure established by law."},
        {"article": "Article 23", "title": "Prohibition of traffic in human beings and forced labour", "description": "Traffic in human beings and begar and other similar forms of forced labour are prohibited."},
        {"article": "Article 24", "title": "Prohibition of employment of children", "description": "No child below the age of fourteen years shall be employed to work in any factory or mine or engaged in any other hazardous employment."},
        {"article": "Article 25", "title": "Freedom of conscience and religion", "description": "Subject to public order, morality and health, all persons are equally entitled to freedom of conscience and the right freely to profess, practise and propagate religion."},
        {"article": "Article 32", "title": "Remedies for enforcement of rights", "description": "The right to move the Supreme Court by appropriate proceedings for the enforcement of the rights conferred by this Part is guaranteed."}
    ]

print(f"🚀 Starting Upload of {len(data)} items...")

vectors = []
for i, item in enumerate(data):
    # Standardize keys
    doc_id = str(item.get('article', item.get('id', f'doc_{i}')))
    title = item.get('title', '')
    desc = item.get('description', item.get('text', ''))
    
    text = f"{title}: {desc}"
    
    try:
        vector = embeddings.embed_query(text)
        
        vectors.append({
            "id": doc_id,
            "values": vector,
            "metadata": {"text": text}
        })
        print(f"   Generated: {doc_id}")

        # Batch upload
        if len(vectors) >= 50:
            index.upsert(vectors=vectors)
            vectors = []
            print(f"   💾 Saved batch.")

    except Exception as e:
        print(f"   ❌ Error on {doc_id}: {e}")

if vectors:
    index.upsert(vectors=vectors)

print("\n✅ Upload Complete! Now start the server.")