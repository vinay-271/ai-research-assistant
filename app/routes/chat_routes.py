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

SYSTEM_PROMPT = """You are an AI Research Assistant for stocks.
You answer user questions about stocks based ONLY on the retrieved fundamentals, filings, and news provided below.

INSTRUCTIONS:
1. Grounding: Answer the question using ONLY the provided text segments. If the information is not present, clearly state that you do not have sufficient data in the retrieved context to answer.
2. Source Citations: Every statement or claim must be cited. When you make a point supported by a retrieved source, cite the source in brackets immediately after the statement (e.g., "... revenue increased by 12% [Source: TCS news]" or "... operating margins expanded [Source: TCS filing]").
3. Guardrails against Financial Advice: Do NOT give recommendations to buy, sell, or hold any stock. Do NOT provide stock price predictions, investment advice, or tell the user what to do with their money. If a user asks for advice or recommendations, explicitly state: "I am an AI Research Assistant. I provide data and information from fundamentals, filings, and news, but I cannot provide investment recommendations or financial advice. Please consult a certified financial advisor."

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