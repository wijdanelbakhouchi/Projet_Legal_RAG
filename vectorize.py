import json
import chromadb
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

def main():
    print("⚙️ Loading Clean Data...")
    with open("data_clean.json", "r", encoding="utf-8") as f:
        documents = json.load(f)

    # 1. Initialize Embedding Model
    # Using the specific multilingual model requested for Arabic/French support
    print("🧠 Loading Embedding Model (MiniLM)...")
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    # 2. Initialize ChromaDB (Vector Database)
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name="labor_code")

    # 3. Batch Process (Embedding + Indexing)
    batch_size = 100
    total_docs = len(documents)
    
    print(f"💾 Indexing {total_docs} articles into ChromaDB...")
    for i in tqdm(range(0, total_docs, batch_size)):
        batch_docs = documents[i : i + batch_size]
        batch_ids = [f"id_{j}" for j in range(i, i + len(batch_docs))]
        
        # Create Embeddings
        embeddings = model.encode(batch_docs).tolist()
        
        # Add to DB
        collection.add(
            documents=batch_docs,
            embeddings=embeddings,
            ids=batch_ids
        )
        
    print("✅ Indexing Complete. Database saved to './chroma_db'")

if __name__ == "__main__":
    main()