from datetime import datetime

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
