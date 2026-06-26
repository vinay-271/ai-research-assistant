from fastapi import APIRouter
from app.config.database import db
from app.schemas.filing_schema import Filing
from app.services.rag_service import store_document

router = APIRouter()


@router.post("/filings")
async def create_filing(filing: Filing):
    result = await db.filings.insert_one(
        filing.model_dump()
    )
    await store_document(
        symbol=filing.symbol,
        source="filing",
        text=filing.content
    )

    return {
        "id": str(result.inserted_id),
        "message": "Filing added successfully"
    }


@router.get("/filings")
async def get_filings():
    filings = []

    async for filing in db.filings.find():
        filing["_id"] = str(filing["_id"])
        filings.append(filing)

    return filings


@router.get("/filings/{symbol}")
async def get_filings_by_symbol(symbol: str):
    filings = []

    async for filing in db.filings.find(
        {"symbol": symbol.upper()}
    ):
        filing["_id"] = str(filing["_id"])
        filings.append(filing)

    return filings