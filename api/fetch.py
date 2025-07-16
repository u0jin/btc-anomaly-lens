import requests
import os
from dotenv import load_dotenv

load_dotenv()
MEMPOOL_BASE = "https://mempool.space/api"

# ✅ mempool.space API (프리미엄)
def fetch_from_mempool(address):
    url = f"{MEMPOOL_BASE}/address/{address}/txs"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else {"error": f"Status {response.status_code}"}

# ✅ 외부에서 호출하는 통합 함수
def get_transaction_data(address, mode="premium"):
    return fetch_from_mempool(address)
