#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logic.graph import generate_transaction_network

# 테스트용 트랜잭션 데이터 (여러 단계로 이어지는 구조)
test_tx_list = [
    {'from': 'A', 'to': 'B', 'amount': 1, 'tx_hash': 'tx1', 'timestamp': '2024-01-01'},
    {'from': 'B', 'to': 'C', 'amount': 2, 'tx_hash': 'tx2', 'timestamp': '2024-01-02'},
    {'from': 'C', 'to': 'D', 'amount': 3, 'tx_hash': 'tx3', 'timestamp': '2024-01-03'},
    {'from': 'D', 'to': 'E', 'amount': 4, 'tx_hash': 'tx4', 'timestamp': '2024-01-04'},
    {'from': 'E', 'to': 'F', 'amount': 5, 'tx_hash': 'tx5', 'timestamp': '2024-01-05'},
    {'from': 'F', 'to': 'G', 'amount': 6, 'tx_hash': 'tx6', 'timestamp': '2024-01-06'},
]

print("🧪 Testing hop expansion...")
print("=" * 50)

# hop=1 테스트
print("\n🔍 Testing hop=1:")
result1 = generate_transaction_network(test_tx_list, max_hops=1, top_n=10, source_address='A')

# hop=2 테스트  
print("\n🔍 Testing hop=2:")
result2 = generate_transaction_network(test_tx_list, max_hops=2, top_n=10, source_address='A')

# hop=3 테스트
print("\n🔍 Testing hop=3:")
result3 = generate_transaction_network(test_tx_list, max_hops=3, top_n=10, source_address='A')

print("\n✅ Test completed!") 