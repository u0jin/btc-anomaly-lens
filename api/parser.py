from datetime import datetime
from dateutil.parser import parse  # 유연한 문자열 → datetime 변환
import logging

# 로그 출력 함수
def log(msg):
    print(f"[PARSER] {msg}")

# ✅ 무료 모드: BlockCypher API 파서
def parse_blockcypher_transactions(raw_json):
    tx_list = []
    txs = raw_json.get("txs", [])
    log(f"Fetched {len(txs)} transactions from BlockCypher")

    for tx in txs:
        timestamp = tx.get("confirmed") or tx.get("received")
        if not timestamp:
            log("⛔ Skipped tx with no timestamp")
            continue
        try:
            dt = parse(timestamp)
        except Exception as e:
            log(f"❌ Timestamp parse failed: {timestamp} → {e}")
            continue

        outputs = tx.get("outputs", [])
        if not outputs:
            log("⛔ Skipped tx with no outputs")
            continue
        for out in outputs:
            address_list = out.get("addresses") or []
            if not address_list:
                log("⛔ Skipped output with no addresses")
                continue
            total_btc = out.get("value", 0) / 1e8
            for addr in address_list:
                tx_list.append({
                    "timestamp": dt.isoformat(),
                    "amount": round(total_btc, 8),
                    "to": addr
                })

    log(f"✅ Parsed {len(tx_list)} transactions")
    return tx_list

# ✅ 프리미엄 모드: mempool.space API 파서
def parse_mempool_transactions(raw_json):
    tx_list = []
    log(f"Fetched {len(raw_json)} transactions from Mempool.space")

    for tx in raw_json:
        status = tx.get("status", {})
        timestamp = status.get("block_time") or status.get("received_at")
        if not timestamp:
            log("⛔ Skipped tx with no timestamp")
            continue
        try:
            dt = (
                datetime.fromtimestamp(timestamp)
                if isinstance(timestamp, int)
                else parse(timestamp)
            )
        except Exception as e:
            log(f"❌ Timestamp parse failed: {timestamp} → {e}")
            continue

        outputs = tx.get("vout", [])
        if not outputs:
            log("⛔ Skipped tx with no outputs")
            continue
        for out in outputs:
            address = out.get("scriptpubkey_address")
            if not address:
                log("⛔ Skipped output with no scriptpubkey_address")
                continue
            value_btc = out.get("value", 0) / 1e8
            tx_list.append({
                "timestamp": dt.isoformat(),
                "amount": round(value_btc, 8),
                "to": address
            })

    log(f"✅ Parsed {len(tx_list)} transactions")
    return tx_list
