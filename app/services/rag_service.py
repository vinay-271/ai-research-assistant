from app.config.database import db
from app.services.embedding_service import (
    create_embedding
)

#store the doc

async def store_document(
    symbol: str,
    source: str,
    text: str
):
    embedding = create_embedding(text)

    document = {
        "symbol": symbol,
        "source": source,
        "text": text,
        "embedding": embedding
    }

    await db.embeddings.insert_one(document)

#search the stored doc

async def search_documents(query: str):

    query_embedding = create_embedding(query)

    pipeline = [
        {
            "$vectorSearch": {
                "index": "autoembed_index",
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": 10,
                "limit": 3
            }
        }
    ]

    documents = []

    async for doc in db.embeddings.aggregate(
        pipeline
    ):
        doc["_id"] = str(doc["_id"])
        documents.append(
        {
            "symbol": doc["symbol"],
            "source": doc["source"],
            "text": doc["text"]
        }
    )

    return documents