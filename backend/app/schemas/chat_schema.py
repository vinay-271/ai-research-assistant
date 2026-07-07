from pydantic import BaseModel
from typing import Optional


class Question(BaseModel):
    question: str
    symbol: Optional[str] = None