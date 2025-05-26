from datetime import datetime

def parse_blockcypher_transactions(raw_json):
    tx_list = []
    for tx in raw_json.get("txs", []):
        timestamp = tx.get("confirmed")
        if not timestamp:
            continue
        try:
            dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except:
            continue
        total_btc = sum(out.get("value", 0) for out in tx.get("outputs", [])) / 1e8
        tx_list.append({"timestamp": dt.isoformat(), "amount": round(total_btc, 8)})
    return tx_list
