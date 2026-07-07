from fastapi import APIRouter
from app.config.database import db
from app.schemas.news_schema import News
from app.services.rag_service import store_document

router = APIRouter()


@router.post("/news")
async def create_news(news: News):
    news_data = news.model_dump()

    result = await db.news.insert_one(
        news_data
    )

    await store_document(
        symbol=news.symbol,
        source="news",
        text=news.content
    )

    return {
        "id": str(result.inserted_id),
        "message": "News added successfully"
    }

@router.get("/news")
async def get_news():

    news_list = []

    async for news in db.news.find():
        news["_id"] = str(news["_id"])
        news_list.append(news)

    return news_list

@router.get("/news/{symbol}")
async def get_news_by_symbol(symbol: str):

    news_list = []

    async for news in db.news.find(
        {"symbol": symbol.upper()}
    ):
        news["_id"] = str(news["_id"])
        news_list.append(news)

    return news_list