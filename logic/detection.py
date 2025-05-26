from datetime import datetime
import numpy as np

def interval_anomaly_score(tx_list):
    '''
    Calculate risk score based on transaction time intervals.
    tx_list: list of dicts with a 'timestamp' key (ISO format)
    '''
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
