from datetime import datetime
from collections import Counter
import numpy as np
import os
import streamlit as st  # 경고 메시지 출력용

# 1. 거래 간격 이상 탐지 (60초 미만)
def interval_anomaly_score(tx_list):
    if len(tx_list) < 2:
        return 0, []
    try:
        timestamps = [datetime.fromisoformat(tx['timestamp']) for tx in tx_list]
    except Exception:
        return 0, []
    intervals = [
        (t2 - t1).total_seconds()
        for t1, t2 in zip(timestamps[:-1], timestamps[1:])
    ]
    short_intervals = [i for i in intervals if i < 60]
    score = min(25, len(short_intervals) * 5)
    return score, short_intervals

# 2. 이상 금액 탐지 (IQR 이상)
def amount_anomaly_score(tx_list):
    values = [tx['amount'] for tx in tx_list if 'amount' in tx]
    if len(values) < 2:
        return 0, []
    q1, q3 = np.percentile(values, [25, 75])
    iqr = q3 - q1
    threshold = q3 + 1.5 * iqr
    outliers = [v for v in values if v > threshold]
    score = min(25, len(outliers) * 5)
    return score, outliers

# 3. 동일 수신 주소 반복 탐지
def repeated_address_score(tx_list):
    targets = [tx.get('to') for tx in tx_list if tx.get('to')]
    counter = Counter(targets)
    flagged = [addr for addr, count in counter.items() if count >= 3]
    score = min(25, len(flagged) * 5)
    return score, flagged

# 4. 시계열 상 이상 간격 탐지
def time_gap_anomaly_score(tx_list):
    if len(tx_list) < 2:
        return 0, []
    try:
        timestamps = [datetime.fromisoformat(tx['timestamp']) for tx in tx_list]
    except Exception:
        return 0, []
    gaps = [
        (t2 - t1).total_seconds()
        for t1, t2 in zip(timestamps[:-1], timestamps[1:])
    ]
    abnormal = [g for g in gaps if g < 10 or g > 3600]
    score = min(15, len(abnormal) * 5)
    return score, abnormal

# 5. 블랙리스트 로딩 및 탐지
def load_blacklist():
    try:
        current_dir = os.path.dirname(__file__)
        blacklist_path = os.path.join(current_dir, "..", "data", "blacklist.txt")

        if not os.path.exists(blacklist_path):
            st.error(f"❌ blacklist.txt not found at: {blacklist_path}")
            return set()

        with open(blacklist_path, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    except Exception as e:
        st.warning(f"⚠️ 블랙리스트 파일 오류: {e}")
        return set()

def blacklist_score(tx_list):
    blacklist = load_blacklist()
    involved = [tx.get('to') for tx in tx_list if tx.get('to') in blacklist]
    if involved:
        return True, 100  # 블랙리스트 주소가 포함되면 100점
    return False, 0
