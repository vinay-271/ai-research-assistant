from fastapi import APIRouter
from app.config.database import db
from app.schemas.stock_schema import Stock

router = APIRouter()


@router.post("/stocks")
async def create_stock(stock: Stock):
    result = await db.stocks.insert_one(stock.dict())

    return {
        "id": str(result.inserted_id),
        "message": "Stock added successfully"
    }

@router.get("/stocks")
async def get_stocks():
    stocks = []

    async for stock in db.stocks.find():
        stock["_id"] = str(stock["_id"])
        stocks.append(stock)

    return stocks

@router.get("/stocks/{symbol}")
async def get_stock(symbol: str):
    stock = await db.stocks.find_one(
        {"symbol": symbol.upper()}
    )

    if not stock:
        return {"message": "Stock not found"}

    stock["_id"] = str(stock["_id"])

    return stock