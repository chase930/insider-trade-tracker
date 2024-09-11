import os
from sec_api import InsiderTradingApi #type: ignore
import pandas as pd  # type: ignore
from dotenv import load_dotenv
import psycopg2 #type: ignore
from pydash import get, flatten #type: ignore
from flatten import flatten_filings

load_dotenv()

insiderTradingApi = InsiderTradingApi(api_key=os.getenv("SEC_API_KEY"))

stock_list = ["TSLA", "AAPL", "AMZN", "NVDA", "META"]

db_insert = psycopg2.connect("dbname=server user=postgres")

cursor = db_insert.cursor()

def fetch_insider_trades(stock_name):
    insider_trades_sample = insiderTradingApi.get_data({
      "query": {"query_string": {"query": f"issuer.tradingSymbol:{stock_name}"}},
      "from": "0",
      "size": "2",
      "sort": [{ "filedAt": { "order": "desc" } }]
    })

    transactions = flatten_filings(insider_trades_sample["transactions"])
    trades = pd.DataFrame(transactions)
    
    return trades


def fetch_multiple_stocks(stock_list):
    all_trades = {}
    for stock in stock_list:
        trades = fetch_insider_trades(stock)
        all_trades[stock] = trades
        #Purely for test purposes: will remove later
        print(f"Testing in script: Insider trades for {stock}:")
        print(trades.head(5))
        print("--------------------------------------------------")
    
    return all_trades

if __name__ == "__main__":
    trades_data = fetch_multiple_stocks(stock_list)

    for stock, trades in trades_data.items():
        trades.to_csv(f'{stock}_insider_trades.csv', index=False)

