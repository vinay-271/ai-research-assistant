import os
import sys
import json
import uuid
import asyncio
from dotenv import load_dotenv

# Ensure workspace root is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.config.database import db
from app.services.rag_service import store_document, collection

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alpha_vantage_data")

def clean_value(val):
    if not val or val.lower() == "none" or val.lower() == "null":
        return 0.0
    try:
        return float(val)
    except ValueError:
        return 0.0

async def parse_and_seed():
    load_dotenv()
    
    if not os.path.exists(DATA_DIR):
        print(f"Error: Data directory not found at {DATA_DIR}. Run fetch_alpha_vantage.py first.")
        return
        
    print("Cleaning up existing database records to prevent duplicates...")
    
    # 1. Clear MongoDB embeddings
    mongo_result = await db.embeddings.delete_many({})
    print(f"Cleared {mongo_result.deleted_count} documents from MongoDB embeddings.")
    
    # 2. Clear ChromaDB
    try:
        existing = collection.get()
        if existing and "ids" in existing and existing["ids"]:
            collection.delete(ids=existing["ids"])
            print(f"Cleared {len(existing['ids'])} vectors from ChromaDB.")
        else:
            print("ChromaDB was already empty.")
    except Exception as e:
        print(f"Notice: ChromaDB clear skipped or failed ({str(e)}).")
        
    total_chunks = 0
    files = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]
    
    for filename in sorted(files):
        filepath = os.path.join(DATA_DIR, filename)
        symbol = filename.split("_")[0].upper()
        source_type = filename.split("_")[1].replace(".json", "")
        
        print(f"\nProcessing {filename} for ticker {symbol}...")
        
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                continue
                
        if source_type == "income":
            reports = data.get("quarterlyReports", [])
            print(f"Found {len(reports)} quarterly income reports. Processing last 8 quarters...")
            # Process last 8 quarters
            for entry in reports[:8]:
                fiscal_date = entry.get("fiscalDateEnding", "N/A")
                currency = entry.get("reportedCurrency", "USD")
                
                rev_raw = entry.get("totalRevenue", "0")
                gp_raw = entry.get("grossProfit", "0")
                op_raw = entry.get("operatingIncome", "0")
                ni_raw = entry.get("netIncome", "0")
                
                rev = clean_value(rev_raw)
                gp = clean_value(gp_raw)
                op = clean_value(op_raw)
                ni = clean_value(ni_raw)
                
                gross_margin = (gp / rev * 100.0) if rev > 0 else 0.0
                operating_margin = (op / rev * 100.0) if rev > 0 else 0.0
                net_margin = (ni / rev * 100.0) if rev > 0 else 0.0
                
                chunk_text = (
                    f"Company: {symbol} | Source: AlphaVantage Income Statement | Topic: Quarterly Financials for Quarter ending {fiscal_date}\n\n"
                    f"For the quarter ending {fiscal_date}, {symbol} reported total revenue of {rev:,.0f} {currency}, "
                    f"gross profit of {gp:,.0f} {currency}, operating income of {op:,.0f} {currency}, and net income of {ni:,.0f} {currency}.\n"
                    f"Calculated Margin Metrics:\n"
                    f"- Gross Margin: {gross_margin:.2f}%\n"
                    f"- Operating Margin: {operating_margin:.2f}%\n"
                    f"- Net Margin: {net_margin:.2f}%"
                )
                
                await store_document(
                    symbol=symbol,
                    source="AlphaVantage Income Statement",
                    text=chunk_text
                )
                total_chunks += 1
                
        elif source_type == "earnings":
            reports = data.get("quarterlyEarnings", [])
            print(f"Found {len(reports)} quarterly earnings reports. Processing last 8 quarters...")
            for entry in reports[:8]:
                fiscal_date = entry.get("fiscalDateEnding", "N/A")
                reported_date = entry.get("reportedDate", "N/A")
                rep_eps = entry.get("reportedEPS", "0")
                est_eps = entry.get("estimatedEPS", "0")
                surprise = entry.get("surprise", "0")
                surprise_pct = entry.get("surprisePercentage", "0")
                
                chunk_text = (
                    f"Company: {symbol} | Source: AlphaVantage Earnings | Topic: EPS Performance for Quarter ending {fiscal_date}\n\n"
                    f"For the quarter ended {fiscal_date} (reported on {reported_date}), {symbol} recorded a reported EPS of {rep_eps} "
                    f"compared to an estimated analyst EPS of {est_eps}.\n"
                    f"Surprise figures:\n"
                    f"- EPS Surprise Value: {surprise}\n"
                    f"- EPS Surprise Percentage: {surprise_pct}%"
                )
                
                await store_document(
                    symbol=symbol,
                    source="AlphaVantage Earnings",
                    text=chunk_text
                )
                total_chunks += 1
                
        elif source_type == "news":
            feed = data.get("feed", [])
            print(f"Found {len(feed)} news articles. Processing up to 10 relevant items...")
            for entry in feed[:10]:
                title = entry.get("title", "N/A")
                summary = entry.get("summary", "N/A")
                pub_time = entry.get("time_published", "N/A")
                ov_sent_lbl = entry.get("overall_sentiment_label", "Neutral")
                ov_sent_scr = entry.get("overall_sentiment_score", 0.0)
                
                # Format pub_time into readable format
                try:
                    formatted_time = f"{pub_time[:4]}-{pub_time[4:6]}-{pub_time[6:8]} {pub_time[9:11]}:{pub_time[11:13]}"
                except Exception:
                    formatted_time = pub_time
                    
                # Find ticker specific sentiment
                ticker_sent = None
                for tick_info in entry.get("ticker_sentiment", []):
                    if tick_info.get("ticker") == symbol:
                        ticker_sent = tick_info
                        break
                        
                ticker_sentiment_text = ""
                if ticker_sent:
                    tick_lbl = ticker_sent.get("ticker_sentiment_label", "Neutral")
                    tick_scr = ticker_sent.get("ticker_sentiment_score", 0.0)
                    tick_rel = ticker_sent.get("relevance_score", 0.0)
                    ticker_sentiment_text = (
                        f"Sentiment specifically for ticker {symbol}:\n"
                        f"- Sentiment Label: {tick_lbl}\n"
                        f"- Sentiment Score: {tick_scr}\n"
                        f"- Relevance Score: {tick_rel}"
                    )
                else:
                    ticker_sentiment_text = f"Sentiment specifically for ticker {symbol}: Neutral"
                    
                chunk_text = (
                    f"Company: {symbol} | Source: AlphaVantage News | Topic: Sentiment Analysis - Published {formatted_time}\n\n"
                    f"Article Title: {title}\n"
                    f"Summary: {summary}\n"
                    f"Overall Article Sentiment: {ov_sent_lbl} (Score: {ov_sent_scr})\n"
                    f"{ticker_sentiment_text}"
                )
                
                await store_document(
                    symbol=symbol,
                    source="AlphaVantage News",
                    text=chunk_text
                )
                total_chunks += 1
                
    print(f"\nParsing complete! Indexed {total_chunks} Alpha Vantage records into MongoDB and ChromaDB.")

if __name__ == "__main__":
    asyncio.run(parse_and_seed())
