from pydash import get, flatten #type: ignore
import math

def flatten_filing(filing):
  transactions = []

  try:
    base_data = {
        "periodOfReport": filing["periodOfReport"], 
        "issuerCik": filing["issuer"]["cik"],
        "issuerTicker": filing["issuer"]["tradingSymbol"],
        "reportingPersonName": get(filing, "reportingOwner.name", ""),
        "reportingPersonCik": get(filing, "reportingOwner.cik", ""),
        "relationship": get(filing, "reportingOwner.relationship", {})
    }
  except Exception as e:
    print(f'{filing["id"]}, caught {type(e)}: {e}')
    return transactions

  if "derivativeTable" in filing and "transactions" in filing["derivativeTable"]:
    for transaction in filing["derivativeTable"]["transactions"]:
      shares = get(transaction, "amounts.shares", 0)
      sharePrice = get(transaction, "amounts.pricePerShare", 0)
      sharesOwnedFollowingTransaction = get(transaction, "postTransactionAmounts.sharesOwnedFollowingTransaction", 0)
      codingCode = get(transaction, "coding.code", "")
      underlyingSecurity = get(transaction, "underlyingSecurity.title", "")

      entry = {
          "type": "derivative",
          "securityTitle": transaction["securityTitle"],
          "underlyingSecurity": underlyingSecurity,
          "codingCode": codingCode,
          "acquiredDisposed": transaction["amounts"]["acquiredDisposedCode"],
          "shares": shares,
          "sharePrice": sharePrice,
          "total": math.ceil(shares * sharePrice),
          "sharesOwnedFollowingTransaction": sharesOwnedFollowingTransaction
      }

      transactions.append({**base_data, **entry})

  if "nonDerivativeTable" in filing and "transactions" in filing["nonDerivativeTable"]:
    for transaction in filing["nonDerivativeTable"]["transactions"]:
      sharePrice = get(transaction, "amounts.pricePerShare", 0)
      sharesOwnedFollowingTransaction = get(transaction, "postTransactionAmounts.sharesOwnedFollowingTransaction", 0)

      entry = {
          "type": "nonDerivative",
          "securityTitle": transaction["securityTitle"],
          "codingCode": transaction["coding"]["code"],
          "acquiredDisposed": transaction["amounts"]["acquiredDisposedCode"],
          "shares": transaction["amounts"]["shares"],
          "sharePrice": sharePrice,
          "total": math.ceil(transaction["amounts"]["shares"] * sharePrice),
          "sharesOwnedFollowingTransaction": sharesOwnedFollowingTransaction
      }

      # merge base_data and entry into a new dict and append to transactions
      transactions.append({**base_data, **entry})

  return transactions


def flatten_filings(filings):
  unflattened_list = list(map(flatten_filing, filings))
  return [item for sublist in unflattened_list for item in sublist]
