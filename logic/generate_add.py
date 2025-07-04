import requests
import time
import pandas as pd
import os

# 파일 경로 설정
input_path = "/Users/yujin/Desktop/BitcoinTrace/lens/btc-anomaly-lens/data/selected_addresses.csv"  # 너가 사용 중인 파일
output_path = "/Users/yujin/Desktop/BitcoinTrace/lens/btc-anomaly-lens/data/100add_blacklist_grouped_txmeta.csv"

# 이미 저장된 결과 불러오기 (중복 방지용)
if os.path.exists(output_path):
    saved_df = pd.read_csv(output_path)
    done_addresses = set(saved_df["address"])
else:
    saved_df = pd.DataFrame()
    done_addresses = set()

df = pd.read_csv(input_path)
results = []

print(f"🔍 총 주소 수: {len(df)}개")

for i, row in df.iterrows():
    addr = row["hacker_address"]
    group = row["report_type"]

    if addr in done_addresses:
        print(f"[{i+1}/{len(df)}] ⏩ Already processed: {addr}")
        continue

    print(f"\n[{i+1}/{len(df)}] 📦 Address: {addr} ｜ Group: {group}")

    try:
        url = f"https://mempool.space/api/address/{addr}/txs"
        res = requests.get(url)
        if res.status_code != 200:
            print(f"❌ Failed to fetch: {res.status_code}")
            continue
        txs = res.json()

        if len(txs) < 2:
            print("⚠️ Not enough transactions (len < 2)")
            continue

        tx_times = sorted([tx['status']['block_time'] for tx in txs if 'status' in tx and 'block_time' in tx])
        intervals = [t2 - t1 for t1, t2 in zip(tx_times, tx_times[1:])]
        avg_interval = sum(intervals) / len(intervals) if intervals else 9999

        recipients = []
        for tx in txs:
            for out in tx.get("vout", []):
                if "scriptpubkey_address" in out:
                    recipients.append(out["scriptpubkey_address"])
        reused_ratio = 1 - len(set(recipients)) / len(recipients) if recipients else 0

        high_fee_flag = any(tx.get("fee", 0) > 500 for tx in txs)

        result = {
            "address": addr,
            "group": group,
            "tx_count": len(txs),
            "avg_interval": round(avg_interval, 2),
            "reused_ratio": round(reused_ratio, 2),
            "high_fee": high_fee_flag
        }

        # 실시간 저장 (append)
        pd.DataFrame([result]).to_csv(output_path, mode='a', header=not os.path.exists(output_path), index=False)

        print(f"   ➤ tx_count = {result['tx_count']} ｜ avg_interval = {result['avg_interval']}s ｜ reused_ratio = {result['reused_ratio']} ｜ high_fee = {result['high_fee']}")

    except Exception as e:
        print(f"Error: {addr} → {e}")

    time.sleep(1.0)  # 요청 간격 (필요시 조정)

print(f"\n✅ 작업 완료. 결과 저장: {output_path}")
