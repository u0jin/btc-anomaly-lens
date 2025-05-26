import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("BLOCKCYPHER_TOKEN")
BLOCKCYPHER_BASE = "https://api.blockcypher.com/v1/btc/main"

def fetch_from_blockcypher(address):
    url = f"{BLOCKCYPHER_BASE}/addrs/{address}/full?token={API_TOKEN}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else {"error": f"Status {response.status_code}"}

def fetch_from_tatum(address):
    return {"note": "Premium API not yet implemented."}

def get_transaction_data(address, mode="free"):
    return fetch_from_blockcypher(address) if mode == "free" else fetch_from_tatum(address)
