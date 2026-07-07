from pydantic import BaseModel


class Stock(BaseModel):
    symbol: str
    name: str
    sector: str
    market_cap: float