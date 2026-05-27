from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types
import os, json
import numpy as np
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# Conexao atualizada sem a trava da api_version="v1"
client = genai.Client(api_key=GOOGLE_API_KEY)
DB_FILE = "vector_db.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def get_embedding(text, task_type="RETRIEVAL_DOCUMENT"):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config=types.EmbedContentConfig(task_type=task_type)
    )
    return response.embeddings[0].values

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def search(query_embedding, db, top_k=3):
    if not db:
        return []
    scored = [(cosine_similarity(query_embedding, doc["embedding"]), doc) for doc in db]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]

@app.route("/health", methods=["GET"])
def health():
    db = load_db()
    return jsonify({"status": "ok", "docs_count": len(db)})

@app.route("/ingest", methods=["POST"])
def ingest():
    data = request.get_json()
    documents = data.get("documents", [])
    if not documents:
        return jsonify({"error": "Nenhum documento enviado"}), 400
    db = load_db()
    added = 0
    for doc in documents:
        doc_id = doc.get("id", f"doc_{len(db)}")
        text = doc.get("text", "")
        metadata = doc.get("metadata", {})
        if not text:
            continue
        embedding = get_embedding(text, "RETRIEVAL_DOCUMENT")
        db = [d for d in db if d["id"] != doc_id]
        db.append({"id": doc_id, "text": text, "metadata": metadata, "embedding": embedding})
        added += 1
    save_db(db)
    return jsonify({"message": f"{added} documentos inseridos com sucesso."})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"error": "Pergunta vazia"}), 400
    db = load_db()
    if not db:
        return jsonify({"answer": "Base vazia. Execute seed_data.py primeiro.", "sources": [], "context_used": []})
    
    query_emb = get_embedding(question, "RETRIEVAL_QUERY")
    top_docs = search(query_emb, db, top_k=3)
    
    context = "\n\n".join(f"[{d['metadata'].get('source', f'Doc {i+1}')}]: {d['text']}" for i, d in enumerate(top_docs))
    prompt = f"""Voce e um assistente inteligente. Use APENAS os documentos abaixo para responder.

Documentos:
{context}

Pergunta: {question}

Responda em portugues brasileiro."""
    
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return jsonify({"answer": response.text, "sources": [d["metadata"].get("source", "N/A") for d in top_docs], "context_used": [d["text"] for d in top_docs]})

@app.route("/collection/clear", methods=["DELETE"])
def clear_collection():
    save_db([])
    return jsonify({"message": "Base limpa com sucesso."})

if __name__ == "__main__":
    app.run(debug=True, port=5000)