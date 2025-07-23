import faiss
import pickle
from sentence_transformers import SentenceTransformer
from groq import Groq

# Load once at startup
model = SentenceTransformer("BAAI/bge-m3")
index = faiss.read_index("chat/vector_index.faiss")
with open("chat/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

# Groq client - replace with your API key
client = Groq(api_key="GROQ API KEY HERE")

def retrieve_top_k_chunks(query, k=3):
    query_embedding = model.encode([f"Query: {query}"], convert_to_numpy=True)
    D, I = index.search(query_embedding, k)
    return [chunks[i] for i in I[0]]

def generate_groq_answer(query, context_chunks):
    context = "\n".join(context_chunks)
    prompt = f"""
প্রসঙ্গ (Context):
{context}

প্রশ্ন (Question):
{query}

উত্তরটি বাংলায় সংক্ষিপ্তভাবে এবং প্রসঙ্গ অনুযায়ী দাও:
"""
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=100,
        top_p=1,
    )
    return response.choices[0].message.content.strip()
