#temporary making old code comment
"""
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

SYSTEM_PROMPT = """ """You are a strict financial research assistant. Answer the following question based ONLY on the provided context. 

If the provided context does not contain the specific answer to the user's question, you MUST reply with exactly: "I don't have enough information to answer this." 

Do not make up or infer information not present in the context. Do not provide a general summary of the company.
Retrieved Context:
{context}"""
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

"""

#new code here
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.schemas.chat_schema import Question
from app.services.rag_service import search_documents
from groq import AsyncGroq
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_LLM_MODEL = os.getenv("GROQ_LLM_MODEL", "llama-3.3-70b-versatile")

# Initialize Groq client
groq_client = AsyncGroq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
You are an intelligent financial research assistant.

Use ONLY the information provided in the retrieved context.

Rules:
1. Summarize and explain information found in the context.
2. You may combine facts from multiple retrieved documents.
3. Do NOT make up information that is not present in the context.
4. If only partial information is available, provide whatever information is available and mention what is missing.
5. Reply with:
"I don't have enough information to answer this."
ONLY when no relevant context is retrieved.

Retrieved Context:
{context}
"""


async def event_generator(question_text: str, symbol: str = None):
    # Retrieve relevant documents
    docs = await search_documents(question_text, symbol=symbol)

    print("\n========== SEARCH DEBUG ==========")
    print("Question:", question_text)
    print("Symbol:", symbol)
    print("Documents Retrieved:", len(docs))
    print("=================================\n")

    # No documents found
    if not docs:
        yield "I don't have enough information to answer this."
        return

    # Use top 5 documents to avoid overwhelming the model
    docs = docs[:5]

    # Build context
    context_parts = []

    for idx, doc in enumerate(docs, start=1):
        context_parts.append(
            f"""
Source {idx}
Stock: {doc['symbol']}
Type: {doc['source']}

{doc['text']}
"""
        )

    context_str = "\n\n".join(context_parts)

    formatted_system = SYSTEM_PROMPT.format(
        context=context_str
    )

    try:
        chat_completion = await groq_client.chat.completions.create(
            model=GROQ_LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": formatted_system
                },
                {
                    "role": "user",
                    "content": question_text
                }
            ],
            temperature=0.2,
            stream=True
        )

        async for chunk in chat_completion:
            if (
                chunk.choices
                and chunk.choices[0].delta.content
            ):
                yield chunk.choices[0].delta.content

    except Exception as e:
        yield f"Error generating response: {str(e)}"


@router.post("/ask")
async def ask_question(question: Question):
    return StreamingResponse(
        event_generator(
            question.question,
            symbol=question.symbol
        ),
        media_type="text/plain"
    )