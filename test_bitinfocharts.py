#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logic.exchange_identifier import ExchangeIdentifier

def test_bitinfocharts():
    """BitInfoCharts 웹 스크래핑 테스트"""
    
    print("🔍 BitInfoCharts 웹 스크래핑 테스트")
    print("=" * 50)
    
    identifier = ExchangeIdentifier()
    
    # 테스트할 주소들
    test_addresses = [
        "1NDyJtNTjmwk5xPNhjgAMu4HDHigtobu1s",  # Binance
        "3QCzvfL4ZRvmJFiWWBVwxfdaNBT8EtxB5y",  # Coinbase
        "37XuVSEpWW4trkfmvWzegTHQt7BdktSKUs",  # OKX
        "1Kr6QSydW9bFQG1mXiPNNu6WpJGmUa9i1g",  # KuCoin
    ]
    
    for i, address in enumerate(test_addresses, 1):
        print(f"\n{i}. 테스트 주소: {address}")
        print("-" * 40)
        
        # BitInfoCharts 검사
        result = identifier._check_bitinfocharts_pattern(address)
        print(f"BitInfoCharts 결과: {result}")
        
        # 전체 공개 DB 검사
        public_db_result = identifier.check_public_databases(address)
        print(f"전체 공개 DB 결과: {public_db_result}")
        
        print()

if __name__ == "__main__":
    test_bitinfocharts() 