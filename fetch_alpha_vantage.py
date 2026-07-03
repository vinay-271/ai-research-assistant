import os
import sys
import time
import json
import requests
from dotenv import load_dotenv

# Ensure workspace root is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
TICKERS = ["AAPL", "MSFT", "GOOG", "TSLA", "NVDA"]
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alpha_vantage_data")

def download_data():
    if not API_KEY:
        print("Error: ALPHA_VANTAGE_API_KEY not found in environment. Please check your .env file.")
        sys.exit(1)
        
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"Saving files to: {DATA_DIR}")
    print(f"Fetching data for tickers: {TICKERS}")
    
    # 5 requests per minute limit = ~12-13 seconds sleep between requests
    delay = 13
    
    for idx, ticker in enumerate(TICKERS):
        print(f"\n[{idx+1}/{len(TICKERS)}] Fetching data for {ticker}...")
        
        # 1. Fetch Income Statement
        income_file = os.path.join(DATA_DIR, f"{ticker}_income.json")
        if not os.path.exists(income_file):
            print(f"Calling INCOME_STATEMENT for {ticker}...")
            url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker}&apikey={API_KEY}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if "symbol" in data:
                    with open(income_file, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=4)
                    print(f"Saved income statement to {ticker}_income.json")
                else:
                    print(f"Warning: Unexpected API response structure for {ticker} income statement: {list(data.keys())[:3]}")
            else:
                print(f"Error fetching income statement: HTTP {response.status_code}")
            time.sleep(delay)
        else:
            print(f"Income statement file already exists for {ticker}. Skipping.")
            
        # 2. Fetch Earnings
        earnings_file = os.path.join(DATA_DIR, f"{ticker}_earnings.json")
        if not os.path.exists(earnings_file):
            print(f"Calling EARNINGS for {ticker}...")
            url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey={API_KEY}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if "symbol" in data:
                    with open(earnings_file, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=4)
                    print(f"Saved earnings to {ticker}_earnings.json")
                else:
                    print(f"Warning: Unexpected API response structure for {ticker} earnings: {list(data.keys())[:3]}")
            else:
                print(f"Error fetching earnings: HTTP {response.status_code}")
            time.sleep(delay)
        else:
            print(f"Earnings file already exists for {ticker}. Skipping.")
            
        # 3. Fetch News Sentiment
        news_file = os.path.join(DATA_DIR, f"{ticker}_news.json")
        if not os.path.exists(news_file):
            print(f"Calling NEWS_SENTIMENT for {ticker}...")
            url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={API_KEY}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if "feed" in data:
                    with open(news_file, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=4)
                    print(f"Saved news sentiment to {ticker}_news.json")
                else:
                    print(f"Warning: Unexpected API response structure for {ticker} news: {list(data.keys())[:3]}")
            else:
                print(f"Error fetching news sentiment: HTTP {response.status_code}")
            time.sleep(delay)
        else:
            print(f"News sentiment file already exists for {ticker}. Skipping.")

    print("\nData download workflow completed.")

if __name__ == "__main__":
    download_data()
