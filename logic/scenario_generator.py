import requests
import time
import pandas as pd
import os

df = pd.read_csv("/Users/yujin/Desktop/BitcoinTrace/lens/btc-anomaly-lens/data/10_blacklist_grouped_txmeta.csv")
grouped = df.groupby("group").agg({
    "tx_count": "mean",
    "avg_interval": "mean",
    "reused_ratio": "mean",
    "high_fee": lambda x: x.mean() > 0.5
}).reset_index()

patterns = []
for _, row in grouped.iterrows():
    patterns.append({
        "id": f"{row['group'].replace(' ', '_').upper()}-AUTO",
        "actor": row['group'],
        "description": f"Auto-generated from blacklist data for {row['group']}",
        "pattern": {
            "tx_count_min": int(round(row['tx_count'])),
            "avg_interval_max": int(round(row['avg_interval'])),
            "reused_address_ratio_min": round(row['reused_ratio'], 2),
            "high_fee_flag": bool(row['high_fee'])
        }
    })

import json
with open("10_scenario_db_from_blacklist.json", "w") as f:
    json.dump(patterns, f, indent=2)

print("✅ 시나리오 패턴 생성 완료 → 10_scenario_db_from_blacklist.json 저장됨")
