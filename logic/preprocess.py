# logic/preprocess.py

import pandas as pd
from dateutil.parser import parse  # 🔥 이걸로 바꿔줌

def preprocess(tx_list):
    """
    Convert transaction list to pandas DataFrame, clean and sort timestamps.
    """
    df = pd.DataFrame(tx_list)
    print(f"📦 Before timestamp parse: {len(df)} rows")

    # ✅ 날짜 파싱 함수
    def safe_parse(ts):
        try:
            return parse(ts)
        except:
            return pd.NaT

    # ✅ datetime 변환 (수동 적용)
    df['timestamp'] = df['timestamp'].apply(safe_parse)
    df = df[df['timestamp'].notna()]
    print(f"✅ After timestamp parse: {len(df)} rows")

    df = df.sort_values(by='timestamp').reset_index(drop=True)
    return df.to_dict(orient='records')  # 분석 함수가 dict list를 받는 경우
