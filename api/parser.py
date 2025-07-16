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
        
        # 입력 주소들 (from)
        inputs = tx.get("vin", [])
        from_addresses = []
        for inp in inputs:
            if "prevout" in inp and "scriptpubkey_address" in inp["prevout"]:
                from_addresses.append(inp["prevout"]["scriptpubkey_address"])
        
        # 출력 주소들 (to)
        outputs = tx.get("vout", [])
        for out in outputs:
            address_list = out.get("scriptpubkey_address")
            if not address_list:
                continue
            total_btc = out.get("value", 0) / 1e8
            
            # 각 from 주소에 대해 트랜잭션 생성
            for from_addr in from_addresses:
                tx_list.append({
                    "timestamp": dt.isoformat(),
                    "amount": round(total_btc, 8),
                    "from": from_addr,
                    "to": address_list,
                    "tx_hash": tx.get("txid", ""),
                    "fee": tx.get("fee", 0) / 1e8 if tx.get("fee") else 0
                })
            
            # from 주소가 없으면 기본값 사용
            if not from_addresses:
                tx_list.append({
                    "timestamp": dt.isoformat(),
                    "amount": round(total_btc, 8),
                    "from": "unknown",
                    "to": address_list,
                    "tx_hash": tx.get("txid", ""),
                    "fee": tx.get("fee", 0) / 1e8 if tx.get("fee") else 0
                })
    
    log(f"✅ Parsed {len(tx_list)} transactions")
    return tx_list
