import streamlit as st
import chromadb
import ollama
from sentence_transformers import SentenceTransformer

# --- CONFIGURATION ---
DB_PATH = "./chroma_db"
COLLECTION_NAME = "labor_code"
MODEL_NAME = "mistral" # Ensure you ran 'ollama pull mistral'

# --- INITIALIZATION ---
@st.cache_resource
def load_resources():
    # Load DB Client
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_collection(name=COLLECTION_NAME)
    # Load Embedding Model
    embed_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    return collection, embed_model

collection, embed_model = load_resources()

# --- RAG LOGIC ---
def retrieve_context(query, k=3):
    """Retrieve the top K most relevant legal articles."""
    query_embedding = embed_model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k
    )
    return results['documents'][0]

def generate_response(query, context_list):
    """Generate answer using LLM with strict legal context."""
    context_text = "\n\n".join(context_list)
    
    # Strict System Prompt defined in Phase 3
    system_prompt = f"""
    Rôle : Vous êtes un assistant juridique expert en Droit du Travail Marocain.
    Instruction : Répondez à la question de l'utilisateur en vous basant UNIQUEMENT sur le CONTEXTE JURIDIQUE fourni ci-dessous.
    
    CONTEXTE JURIDIQUE (Code du Travail) :
    {context_text}
    
    Si la réponse n'est pas dans le contexte, dites simplement "Je ne trouve pas cette information dans le code fourni."
    Répondez dans la même langue que la question (Arabe ou Français).
    """
    
    response = ollama.chat(model=MODEL_NAME, messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': query}
    ])
    return response['message']['content']

# --- INTERFACE (Phase 4) ---
st.set_page_config(page_title="Legal-RAG Maroc", page_icon="⚖️")
st.title("⚖️ Legal-RAG : Code du Travail Marocain")
st.markdown("Posez vos questions juridiques. L'IA répondra **uniquement** sur la base du code officiel.")

# User Input
query = st.text_input("Votre question :", placeholder="Ex: Quelles sont les indemnités de licenciement abusif ?")

if query:
    with st.spinner("🔍 Recherche des articles de loi..."):
        # 1. Retrieval
        retrieved_docs = retrieve_context(query)
        
    # Display Context (Transparency)
    with st.expander("Voir les articles de loi utilisés (Sources)"):
        for doc in retrieved_docs:
            st.info(doc)
            
    with st.spinner("📝 Rédaction de la réponse..."):
        # 2. Generation
        answer = generate_response(query, retrieved_docs)
        st.success("Réponse :")
        st.write(answer)