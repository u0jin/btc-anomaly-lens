# logic/preprocess.py

import pandas as pd

def preprocess(tx_list):
    """
    Convert transaction list to pandas DataFrame, clean and sort timestamps.
    """
    df = pd.DataFrame(tx_list)

    # ✅ 'timestamp' 컬럼을 datetime으로 안전하게 변환
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True, errors='coerce')

    # ✅ 변환 실패한 값(NaT) 제거
    df = df[df['timestamp'].notna()]

    # ✅ 정렬
    df = df.sort_values(by='timestamp').reset_index(drop=True)

    return df
