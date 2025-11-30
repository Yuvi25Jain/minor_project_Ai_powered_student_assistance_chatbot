import json
from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions

# ---------------------- Config ----------------------
# Local folder where Chroma will store its data
BASE_DIR = Path(__file__).parent
CHROMA_DB_PATH = BASE_DIR / "chroma_db"
COLLECTION_NAME = "student_faqs"
EMBED_MODEL_NAME = "all-mpnet-base-v2"


def get_client():
    """Return a local persistent Chroma client (no HTTP server needed)."""
    return chromadb.PersistentClient(path=str(CHROMA_DB_PATH))


def get_collection(client):
    """Return (or create) the FAQ collection with the correct embedding function."""
    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBED_MODEL_NAME
    )
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embed_fn,
    )


def load_faqs():
    """Load FAQs from faqs.json (in the same folder as this file)."""
    faqs_path = BASE_DIR / "faqs.json"

    try:
        with open(faqs_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: faqs.json not found at {faqs_path}")
        raise
    except json.JSONDecodeError:
        print("❌ Error: faqs.json contains invalid JSON")
        raise


def ingest_faqs():
    """Embed and store FAQs in ChromaDB, skipping ones already present."""
    client = get_client()
    collection = get_collection(client)

    try:
        faqs = load_faqs()
    except Exception:
        # Errors already logged in load_faqs()
        return

    # Check existing IDs to avoid duplicates
    existing_ids = set()
    try:
        existing = collection.get()
        existing_ids = set(existing.get("ids", []))
    except Exception:
        # Collection may be empty or not yet created
        pass

    # Only add FAQs not already in the DB
    new_faqs = [faq for faq in faqs if faq.get("id") not in existing_ids]

    if not new_faqs:
        print("✅ No new FAQs to add. ChromaDB is already up to date.")
        return

    for faq in new_faqs:
        q = faq.get("question", "")
        a = faq.get("answer", "")
        faq_id = faq.get("id")
        category = faq.get("category")

        if not faq_id or not q or not a:
            # Skip incomplete records
            continue

        collection.add(
            documents=[q],
            metadatas=[{"answer": a, "category": category}],
            ids=[faq_id],
        )

    print(f"✅ {len(new_faqs)} new FAQs embedded and stored in ChromaDB")


if __name__ == "__main__":
    # Run this once (or when faqs.json changes) to load data into ChromaDB
    ingest_faqs()