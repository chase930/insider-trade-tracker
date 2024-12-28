import os
from sec_api import InsiderTradingApi 
import pandas as pd 
from dotenv import load_dotenv 
import psycopg2 
from psycopg2.extras import execute_values 
from pydash import get, flatten 
from flatten import flatten_filings
import json

load_dotenv()

insiderTradingApi = InsiderTradingApi(api_key=os.getenv("SEC_API_KEY"))

stock_list = ["TSLA", "AAPL", "AMZN", "NVDA", "META"]


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


def insert_into_db(trades_data):
    try:
        connection = psycopg2.connect(
            user=os.getenv("DB_USER"),       
            password=os.getenv("DB_PASSWORD"),  
            host=os.getenv("DB_HOST"),         
            port=os.getenv("DB_PORT"),       
            database=os.getenv("DB_DATABASE")    
        )
        cursor = connection.cursor()
        
        insert_query = """
        INSERT INTO insider_trades (
            stock_name, period_of_report, issuer_cik, issuer_ticker, 
            reporting_person_name, reporting_person_cik, relationship, type, 
            security_title, underlying_security, coding_code, acquired_disposed, 
            shares, share_price, total, shares_owned_following_transaction,
            transaction_date
        ) VALUES %s
        """
        
        for stock, trades in trades_data.items():
            records = trades.to_dict('records')
            values = [
                (
                stock,
                record["periodOfReport"],
                record["issuerCik"],
                record["issuerTicker"],
                record["reportingPersonName"],
                record["reportingPersonCik"],
                json.dumps(record["relationship"]),  
                record["type"],
                record["securityTitle"],
                record.get("underlyingSecurity", ""),
                record["codingCode"],
                record["acquiredDisposed"],
                record["shares"],
                record["sharePrice"],
                record["total"],
                record["sharesOwnedFollowingTransaction"],
                record.get("transactionDate", None)
                ) for record in records
            ]
            
            # Execute batch insertion
            execute_values(cursor, insert_query, values)
            connection.commit()
            print("DB insertion complete.")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


if __name__ == "__main__":
    stock_list = ["TSLA", "AAPL", "AMZN", "NVDA", "META"]
    trades_data = fetch_multiple_stocks(stock_list)
    insert_into_db(trades_data)
    print("Data inserted successfully!")
    

