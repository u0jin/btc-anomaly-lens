from datetime import datetime
from dateutil.parser import parse  # 유연한 문자열 → datetime 변환
import logging

# 로그 출력 함수
def log(msg):
    print(f"[PARSER] {msg}")

# mempool.space 파서만 남김
def parse_mempool_transactions(raw_json):
    tx_list = []
    txs = raw_json if isinstance(raw_json, list) else raw_json.get("txs", [])
    for tx in txs:
        timestamp = tx.get("status", {}).get("block_time")
        if not timestamp:
            continue
        from datetime import datetime
        dt = datetime.utcfromtimestamp(timestamp)
        outputs = tx.get("vout", [])
        for out in outputs:
            address_list = out.get("scriptpubkey_address")
            if not address_list:
                continue
            total_btc = out.get("value", 0) / 1e8
            tx_list.append({
                "timestamp": dt.isoformat(),
                "amount": round(total_btc, 8),
                "to": address_list
            })
    return tx_list
