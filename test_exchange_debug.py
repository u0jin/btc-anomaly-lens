#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logic.exchange_identifier import identify_exchange_comprehensive, ExchangeIdentifier
import json

def test_exchange_identification():
    """거래소 주소 인식 테스트"""
    
    # 테스트할 공식 주소들
    test_addresses = [
        "1NDyJtNTjmwk5xPNhjgAMu4HDHigtobu1s",  # Binance
        "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy",  # Binance
        "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",  # Binance
        "3QCzvfL4ZRvmJFiWWBVwxfdaNBT8EtxB5y",  # Coinbase
        "3NukJ6fYZJ5Kk8bPjycAnruZkE5Q7UW7i8",  # Coinbase
        "3Cbq7aT1tY8kMxWLbitaG7yT6bPbKChq64",  # Coinbase
        "37XuVSEpWW4trkfmvWzegTHQt7BdktSKUs",  # OKX
        "1Kr6QSydW9bFQG1mXiPNNu6WpJGmUa9i1g",  # KuCoin
        "3D2oetdNuZUqQHPJmcMDDHYoqkyNVsFk9r",  # Bitfinex
        "1Cdid9KFAaatwczBwBttQcwXYCpvK8h7FK",  # Huobi
    ]
    
    print("🔍 거래소 주소 인식 디버깅 테스트")
    print("=" * 60)
    
    # ExchangeIdentifier 인스턴스 생성
    identifier = ExchangeIdentifier()
    
    for i, address in enumerate(test_addresses, 1):
        print(f"\n{i}. 테스트 주소: {address}")
        print("-" * 40)
        
        # 1. 공식 주소 확인 테스트
        official_result = identifier.check_official_addresses(address)
        print(f"공식 주소 확인: {official_result}")
        
        # 2. 종합 식별 테스트
        comprehensive_result = identify_exchange_comprehensive(address)
        final_result = comprehensive_result.get('final_result', {})
        
        print(f"종합 식별 결과:")
        print(f"  - 거래소: {final_result.get('exchange', 'None')}")
        print(f"  - 신뢰도: {final_result.get('confidence', 'None')}")
        print(f"  - 방법: {final_result.get('method', 'None')}")
        print(f"  - 설명: {final_result.get('description', 'None')}")
        
        # 3. 문제 진단
        if not final_result.get('exchange'):
            print("❌ 문제 발견: 거래소가 식별되지 않음")
            print("  - 공식 주소 확인 결과:", official_result.get('found', False))
            print("  - 실제 거래소 DB 확인:", address in identifier.real_exchange_addresses)
        else:
            print("✅ 정상: 거래소가 식별됨")
        
        print()

if __name__ == "__main__":
    test_exchange_identification() 