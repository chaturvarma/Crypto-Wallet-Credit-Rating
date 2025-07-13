import json

def extract_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    result = []

    transaction_types = {
        "deposits": 0,
        "withdraws": 1,
        "borrows": 2,
        "repays": 3,
    }

    for transaction_type, transaction_code in transaction_types.items():
        transactions = data.get(transaction_type, [])
        for transaction in transactions:
            transaction_info = {
                "account_id": transaction["account"]["id"],
                "amount_usd": float(transaction["amountUSD"] or 0),
                "asset_symbol": transaction["asset"]["symbol"],
                "timestamp": transaction["timestamp"],
                "transaction_type": transaction_code
            }
            result.append(transaction_info)


    liquidates = data.get("liquidates", [])

    for liquidate in liquidates:
        liquidate_info = {
            "account_id": liquidate["liquidator"]["id"],
            "amount_usd": float(liquidate["amountUSD"] or 0),
            "asset_symbol": liquidate["asset"]["symbol"],
            "timestamp": liquidate["timestamp"],
            "transaction_type": 4
        }
        result.append(liquidate_info)

    return result