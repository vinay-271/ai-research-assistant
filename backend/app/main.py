from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.database import db
from app.routes.news_routes import router as news_router
from app.routes.stock_routes import router as stock_router
from app.routes.filing_routes import router as filing_router
from app.routes.chat_routes import (
    router as chat_router
)
from app.services.rag_service import collection
#create_embedding is temp
from app.services.embedding_service import (
    create_embedding
)
#store_document is temp
from app.services.rag_service import (
    store_document
)
#search_documents is temp
from app.services.rag_service import (
    search_documents
)

app = FastAPI(
    title="Financial Assistant API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stock_router)
app.include_router(news_router)
app.include_router(filing_router)
app.include_router(chat_router)

@app.get("/")
def home():
    return {
        "message": "Backend Running 🚀"
    }


@app.get("/test-db")
async def test_db():
    collections = await db.list_collection_names()

    return {
        "database": "financial_assistant",
        "collections": collections
    }

#temp test-embeddings

@app.get("/test-embedding")
def test_embedding():

    embedding = create_embedding(
        "TCS reported strong quarterly earnings."
    )

    return {
        "dimensions": len(embedding),
        "sample": embedding[:5]
    } 

#test_store is temp

@app.get("/test-store")
async def test_store():

    await store_document(
        symbol="TCS",
        source="filing",
        text="Revenue grew by 12 percent and operating margin expanded to 24 percent."
    )

    return {
        "message": "Stored successfully"
    }

#search_document is also temp added
@app.get("/test-search")
async def test_search():

    docs = await search_documents(
        "How did TCS perform this quarter?"
    )

    return docs

#temporary chroma testing
@app.get("/test-chroma")
async def test_chroma():
    return {
        "count": collection.count()
    }

#temporary adding the meta-data-test
@app.get("/test-meta")
async def test_meta():
    data = collection.get(limit=5)
    return data

#another api endpoint and I'm crying at this point
@app.get("/test-symbol/{symbol}")
async def test_symbol(symbol: str):
    data = collection.get(
        where={"symbol": symbol.upper()}
    )
    return {
        "count": len(data["ids"])
    }