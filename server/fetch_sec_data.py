import os
from sec_api import InsiderTradingApi #type: ignore
import pandas as pd  # type: ignore
from dotenv import load_dotenv
import json

load_dotenv()

insiderTradingApi = InsiderTradingApi(api_key=os.getenv("SEC_API_KEY"))


query_string = "issuer.tradingSymbol:TSLA"

insider_trades_sample = insiderTradingApi.get_data({
  "query": {"query_string": {"query": query_string}},
  "from": "0",
  "size": "2",
  "sort": [{ "filedAt": { "order": "desc" } }]
})

print(json.dumps(insider_trades_sample, indent=4))

