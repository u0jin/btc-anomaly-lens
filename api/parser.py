from datetime import datetime

def parse_blockcypher_transactions(raw_json):
    tx_list = []

    for tx in raw_json.get("txs", []):
        timestamp = tx.get("confirmed") or tx.get("received")
        if not timestamp:
            continue
        try:
            dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except:
            continue

        outputs = tx.get("outputs", [])
        for out in outputs:
            address_list = out.get("addresses", [])
            total_btc = out.get("value", 0) / 1e8  # value는 Satoshi 단위
            for addr in address_list:
                tx_list.append({
                    "timestamp": dt.isoformat(),
                    "amount": round(total_btc, 8),
                    "to": addr  # 여기서 수신 주소 직접 저장
                })

    return tx_list
