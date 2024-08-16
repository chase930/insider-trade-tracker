import os
from sec_api import QueryApi  # type: ignore
import pandas as pd  # type: ignore
from dotenv import load_dotenv
import json

load_dotenv()

queryApi = QueryApi(api_key=os.getenv("SEC_API_KEY"))

query = {
    "query": {"query_string": {"query": "formType:\"4\""}},
    "from": "0",
    "size": "20",
    "sort": [{"filedAt": {"order": "desc"}}]
}

filings = queryApi.get_filings(query)

print(json.dumps(filings['filings'][0], indent=4))

def get_reporting_owner_data(filing):
    company_name = None
    insider_name = None

    for entity in filing['entities']:
        if '(Issuer)' in entity['companyName']:
            company_name = entity['companyName'].replace(' (Issuer)', '').strip()
        if '(Reporting)' in entity['companyName']:
            insider_name = entity['companyName'].replace(' (Reporting)', '').strip()

    return {
        'companyName': company_name,
        'insider_reportingOwnerName': insider_name,
        'filedAt': filing['filedAt']
    }

data = [get_reporting_owner_data(filing) for filing in filings['filings']]

df = pd.DataFrame(data)

print("\nRelevant filing data:")
print(df)

entities_df = pd.json_normalize(
    filings['filings'],
    'entities',
    ['companyName', 'formType', 'filedAt'],
    record_prefix='entity_',
    meta_prefix='parent_'
)

print("\nEntities details:")
print(entities_df.head())
