import os
import sys
import asyncio
from dotenv import load_dotenv

# Ensure workspace root is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.config.database import db
from app.services.rag_service import store_document, collection

def split_markdown_by_headings(content: str):
    sections = []
    current_header = "Overview"
    current_content = []
    
    for line in content.splitlines():
        if line.startswith("## ") or line.startswith("# ") or line.startswith("### "):
            if current_content:
                text_block = "\n".join(current_content).strip()
                if text_block:
                    sections.append((current_header, text_block))
            current_header = line.strip("# ")
            current_content = [line]
        else:
            current_content.append(line)
            
    if current_content:
        text_block = "\n".join(current_content).strip()
        if text_block:
            sections.append((current_header, text_block))
            
    return sections

async def main():
    load_dotenv()
    
    print("Cleaning up existing data to prevent duplicates...")
    
    # 1. Clear MongoDB embeddings collection
    mongo_result = await db.embeddings.delete_many({})
    print(f"Cleared {mongo_result.deleted_count} documents from MongoDB embeddings collection.")
    
    # 2. Clear ChromaDB collection entries
    try:
        existing_data = collection.get()
        if existing_data and "ids" in existing_data and existing_data["ids"]:
            collection.delete(ids=existing_data["ids"])
            print(f"Cleared {len(existing_data['ids'])} vectors from ChromaDB collection.")
        else:
            print("ChromaDB collection was already empty.")
    except Exception as e:
        print(f"Notice: ChromaDB clear skipped or failed ({str(e)}).")
        
    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
    if not os.path.exists(reports_dir):
        print(f"Error: Reports directory not found at {reports_dir}")
        return
        
    company_dirs = [d for d in os.listdir(reports_dir) if os.path.isdir(os.path.join(reports_dir, d))]
    print(f"Found {len(company_dirs)} company folders to process.")
    
    total_chunks = 0
    
    for company_symbol in sorted(company_dirs):
        company_path = os.path.join(reports_dir, company_symbol)
        print(f"\nProcessing {company_symbol}...")
        
        # Look for standard 3 reports files
        files_to_process = ["company_knowledge.md", "quarterly_results.md", "recent_news.md"]
        for filename in files_to_process:
            filepath = os.path.join(company_path, filename)
            if not os.path.exists(filepath):
                continue
                
            source_type = filename.replace(".md", "")
            
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                
            if not content.strip():
                continue
                
            sections = split_markdown_by_headings(content)
            for topic, text in sections:
                # Format chunk with contextual headers for optimized vector search
                chunk_text = f"Company: {company_symbol.upper()} | Source: {source_type} | Topic: {topic}\n\n{text}"
                
                await store_document(
                    symbol=company_symbol.upper(),
                    source=source_type,
                    text=chunk_text
                )
                total_chunks += 1
                
        print(f"Completed processing for {company_symbol}")
        
    print(f"\nSeeding complete! Indexed {total_chunks} sections into the RAG database.")

if __name__ == "__main__":
    asyncio.run(main())
