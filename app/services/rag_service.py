import chromadb
import uuid
import os
from app.config.database import db
from app.services.embedding_service import (
    create_embedding
)

# Initialize ChromaDB persistent client in the workspace root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHROMA_DB_PATH = os.path.join(BASE_DIR, "chroma_db")
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

# Get or create the collection
collection = chroma_client.get_or_create_collection(name="financial_docs")


async def store_document(
    symbol: str,
    source: str,
    text: str
):
    embedding = create_embedding(text)

    # Store in MongoDB (original behavior)
    document = {
        "symbol": symbol.upper(),
        "source": source,
        "text": text,
        "embedding": embedding
    }
    await db.embeddings.insert_one(document)

    # Store in ChromaDB
    doc_id = str(uuid.uuid4())
    collection.add(
        embeddings=[embedding],
        documents=[text],
        metadatas=[{"symbol": symbol.upper(), "source": source}],
        ids=[doc_id]
    )


async def search_documents(query: str, symbol: str = None):
    query_embedding = create_embedding(query)

    # Build filter if symbol is provided
    where_filter = None
    if symbol:
        where_filter = {"symbol": symbol.upper()}

    # Query ChromaDB for top 10 candidates
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=10,
        where=where_filter
    )

    documents = []
    if results and "documents" in results and results["documents"] and len(results["documents"]) > 0:
        doc_texts = results["documents"][0]
        metadatas = results["metadatas"][0]

        for text, meta in zip(doc_texts, metadatas):
            documents.append({
                "symbol": meta.get("symbol"),
                "source": meta.get("source"),
                "text": text
            })
    #temporary adding to check
    print("\n========== SEARCH DEBUG ==========")
    print("Question:", query)
    print("Symbol filter:", where_filter)
    print("Results count:", len(documents))
    print("Documents:", documents)
    print("=================================\n")
    #temporary adding over

    return documents