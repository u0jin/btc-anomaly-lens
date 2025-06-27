from datetime import datetime

# ✅ 무료 모드용 BlockCypher API 파서
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
            address_list = out.get("addresses") or []  # ← 여기만 수정!
            total_btc = out.get("value", 0) / 1e8
            for addr in address_list:
                tx_list.append({
                    "timestamp": dt.isoformat(),
                    "amount": round(total_btc, 8),
                    "to": addr
                })

    return tx_list


# ✅ 프리미엄 모드용 mempool.space API 파서
def parse_mempool_transactions(raw_json):
    tx_list = []

    for tx in raw_json:
        status = tx.get("status", {})
        timestamp = status.get("block_time") or status.get("received_at")
        if not timestamp:
            continue
        try:
            dt = (
                datetime.fromtimestamp(timestamp)
                if isinstance(timestamp, int)
                else datetime.fromisoformat(timestamp)
            )
        except:
            continue

        outputs = tx.get("vout", [])
        for out in outputs:
            scriptpubkey_address = out.get("scriptpubkey_address")
            value_btc = out.get("value", 0) / 1e8
            if scriptpubkey_address:
                tx_list.append({
                    "timestamp": dt.isoformat(),
                    "amount": round(value_btc, 8),
                    "to": scriptpubkey_address
                })

    return tx_list
