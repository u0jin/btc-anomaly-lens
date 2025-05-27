import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("BLOCKCYPHER_TOKEN")
BLOCKCYPHER_BASE = "https://api.blockcypher.com/v1/btc/main"
MEMPOOL_BASE = "https://mempool.space/api"

# ✅ BlockCypher API (무료)
def fetch_from_blockcypher(address):
    url = f"{BLOCKCYPHER_BASE}/addrs/{address}/full?token={API_TOKEN}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else {"error": f"Status {response.status_code}"}

# ✅ Mempool.space API (프리미엄)
def fetch_from_mempool(address):
    try:
        url = f"{MEMPOOL_BASE}/address/{address}/txs"
        response = requests.get(url)
        return response.json() if response.status_code == 200 else {"error": f"Status {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

# ✅ 전체 mempool 요약
def fetch_mempool_summary():
    """
    Fetch global mempool summary from mempool.space
    Returns dict with 'count', 'vsize', 'total_fee'
    """
    try:
        r = requests.get(f"{MEMPOOL_BASE}/mempool")
        if r.status_code == 200:
            return r.json()
        return {}
    except Exception:
        return {}
# ✅ 수수료 히스토그램
def fetch_fee_histogram():
    """
    Fetch mempool fee histogram (used to estimate block composition by fee rate)
    Returns a list of dicts with blockSize, feeRange, count
    """
    try:
        r = requests.get(f"{MEMPOOL_BASE}/v1/fees/mempool-blocks")
        if r.status_code == 200:
            return r.json()
        return []
    except Exception:
        return []

# ✅ 외부에서 호출하는 통합 함수
def get_transaction_data(address, mode="free"):
    return fetch_from_blockcypher(address) if mode == "free" else fetch_from_mempool(address)
