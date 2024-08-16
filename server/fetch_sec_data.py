import os
from sec_api import QueryApi
import pandas as pd
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

queryApi = QueryApi(api_key=os.getenv("SEC_API_KEY"))

query = {
    "query": { "query_string": { "query": "formType:\"4\"" } },
    "from": "0",
    "size": "10",
    "sort": [{ "filedAt": { "order": "desc" } }]
}

filings = queryApi.get_filings(query)

df = pd.json_normalize(filings['filings'])

print("Available columns:", df.columns)
print(df.head())

if all(col in df.columns for col in ['companyName', 'formType', 'filedAt']):
    print("\nRelevant filing data:")
    print(df[['companyName', 'formType', 'filedAt']])
else:
    print("Expected columns not found in DataFrame.")

entities_df = pd.json_normalize(
    filings['filings'], 
    'entities', 
    ['companyName', 'formType', 'filedAt'], 
    record_prefix='entity_',
    meta_prefix='parent_'
)

print("\nEntities details:")
print(entities_df.head())
