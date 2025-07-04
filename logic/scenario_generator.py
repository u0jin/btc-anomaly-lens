import pandas as pd
import json

df = pd.read_csv("/Users/yujin/Desktop/BitcoinTrace/lens/btc-anomaly-lens/data/100_blacklist_grouped_txmeta.csv")

# 숫자형 컬럼 변환
for col in ["tx_count", "avg_interval", "reused_ratio"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# high_fee 컬럼을 bool로 변환
df["high_fee"] = df["high_fee"].astype(str).str.strip().str.lower().map({
    "true": True,
    "false": False
})

# NaN 제거
df.dropna(subset=["tx_count", "avg_interval", "reused_ratio", "high_fee"], inplace=True)

# 그룹화 및 집계
grouped = df.groupby("group").agg({
    "tx_count": "mean",
    "avg_interval": "mean",
    "reused_ratio": "mean",
    "high_fee": lambda x: x.mean() > 0.5
}).reset_index()

# 시나리오 구성
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

with open("10_scenario_db_from_blacklist.json", "w") as f:
    json.dump(patterns, f, indent=2)

print("✅ 시나리오 패턴 생성 완료 → 100_scenario_db_from_blacklist.json 저장됨")
