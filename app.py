from pathlib import Path

from flask import Flask, request, jsonify
from flask_cors import CORS
import chromadb
from chromadb.utils import embedding_functions

# ---------------------- Config ----------------------
BASE_DIR = Path(__file__).parent
CHROMA_DB_PATH = BASE_DIR / "chroma_db"
COLLECTION_NAME = "student_faqs"
EMBED_MODEL_NAME = "all-mpnet-base-v2"

# ---------------------- Flask app setup ----------------------
app = Flask(__name__)
CORS(app)  # allow Streamlit (different port) to call this API


def get_client():
    """Return the same local persistent Chroma client used by db.py."""
    return chromadb.PersistentClient(path=str(CHROMA_DB_PATH))


def get_collection():
    """Return (or create) the FAQ collection with the correct embedding function."""
    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBED_MODEL_NAME
    )
    client = get_client()
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embed_fn,
    )


# Create collection once at startup
collection = get_collection()


@app.route("/health", methods=["GET"])
def health():
    """Simple health check endpoint."""
    return jsonify({"status": "ok"}), 200


@app.route("/search", methods=["POST"])
def search():
    """
    Accepts JSON: { "query": "<user question>" }
    Returns:      { "answer": "<best answer from FAQ VectorDB>" }
    """
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or "query" not in data:
        return jsonify({"answer": "❌ Invalid request. Expected JSON with 'query' field."}), 400

    query = str(data.get("query", "")).strip()
    print(f"Received query: {query}")

    if not query:
        return jsonify({"answer": "❌ Query cannot be empty."}), 400

    try:
        results = collection.query(query_texts=[query], n_results=1)

        metadatas = results.get("metadatas") or []
        if not metadatas or not metadatas[0]:
            print("No results found or empty metadata.")
            return jsonify({"answer": "❌ No matching answer found."})

        top_meta = metadatas[0][0] or {}
        answer = top_meta.get("answer", "❌ No matching answer found.")

        return jsonify({"answer": answer})

    except Exception as e:
        print(f"Error during query: {e}")
        return jsonify({"answer": f"❌ Backend error: {str(e)}"}), 500


if __name__ == "__main__":
    # Run: python app.py
    # Then backend is available at http://127.0.0.1:5000/search
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)