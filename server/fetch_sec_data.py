import os
from sec_api import QueryApi
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

queryApi = QueryApi(api_key=os.getenv("SEC_API_KEY"))

query = {
    "query": { "query_string": { "query": "formType:\"4\"" } },
    "from": "0",
    "size": "10",
    "sort": [{ "filedAt": { "order": "desc" } }]
}

filings = queryApi.get_filings(query)

print(filings)

if filings and 'filings' in filings:
    df = pd.json_normalize(filings['filings'])
    print(df.columns)  
    print(df.head())   
    
    if all(col in df.columns for col in ['reportingOwnerName', 'transactionDate', 'transactionShares']):
        print(df[['reportingOwnerName', 'transactionDate', 'transactionShares']])
    else:
        print("Columns not found in DataFrame.")
else:
    print("No filings returned from the API.")
