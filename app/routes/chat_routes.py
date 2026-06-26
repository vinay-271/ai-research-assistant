from fastapi import APIRouter
from app.schemas.chat_schema import Question
from app.services.rag_service import (
    search_documents
)

router = APIRouter()


@router.post("/ask")
async def ask_question(
    question: Question
):

    docs = await search_documents(
        question.question
    )

    return {
        "question": question.question,
        "context": docs
    }