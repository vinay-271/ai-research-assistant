from pydantic import BaseModel


class Filing(BaseModel):
    symbol: str
    title: str
    content: str
    report_type: str
    published_at: str