from sec_api import QueryApi #type: ignore
import pandas as pd #type: ignore

queryApi = QueryApi(api_key="your_api_key")

query = {
    "query": { "query_string": { "query": "formType:\"4\"" } },
    "from": "0",
    "size": "10",
    "sort": [{ "filedAt": { "order": "desc" } }]
}

filings = queryApi.get_filings(query)

df = pd.json_normalize(filings['filings'])

print(df[['reportingOwnerName', 'transactionDate', 'transactionShares']])
