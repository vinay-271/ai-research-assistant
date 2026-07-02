from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.schemas.chat_schema import Question
from app.services.rag_service import (
    search_documents
)
from groq import AsyncGroq
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_LLM_MODEL = os.getenv("GROQ_LLM_MODEL", "llama-3.3-70b-versatile")

# Initialize Async Groq client
groq_client = AsyncGroq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """You are a strict financial research assistant. Answer the following question based ONLY on the provided context. 

If the provided context does not contain the specific answer to the user's question, you MUST reply with exactly: "I don't have enough information to answer this." 

Do not make up or infer information not present in the context. Do not provide a general summary of the company.
Retrieved Context:
{context}
"""


async def event_generator(question_text: str, symbol: str = None):
    # Search documents using the refactored RAG service
    docs = await search_documents(question_text, symbol=symbol)

    # Format the retrieved documents as context
    context_str = ""
    if docs:
        for idx, doc in enumerate(docs, start=1):
            context_str += f"Source {idx} | Stock: {doc['symbol']} | Source: {doc['source']}\nContent: {doc['text']}\n\n"
    else:
        context_str = "No retrieved context found."

    formatted_system = SYSTEM_PROMPT.format(context=context_str)

    try:
        chat_completion = await groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": formatted_system},
                {"role": "user", "content": question_text}
            ],
            model=GROQ_LLM_MODEL,
            stream=True
        )

        async for chunk in chat_completion:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    except Exception as e:
        yield f"\n[Error generating response: {str(e)}]"


@router.post("/ask")
async def ask_question(
    question: Question
):
    return StreamingResponse(
        event_generator(question.question, symbol=question.symbol),
        media_type="text/plain; charset=utf-8"
    )