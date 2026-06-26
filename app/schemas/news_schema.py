from pydantic import BaseModel


class News(BaseModel):
    symbol: str
    title: str
    content: str
    source: str
    published_at: str