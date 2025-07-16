#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from logic.exchange_identifier import ExchangeIdentifier
import time

def test_walletexplorer_integration():
    """WalletExplorer.com API가 통합된 거래소 식별 시스템 테스트"""
    
    # 테스트할 거래소 주소들
    test_addresses = [
        "1NDyJtNTjmwk5xPNhjgAMu4HDHigtobu1s",  # Binance
        "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy",  # Binance
        "3QCzvfL4ZRvmJFiWWBVwxfdaNBT8EtxB5y",  # Coinbase
        "3NukJ6fYZJ5Kk8bPjycAnruZkE5Q7UW7i8",  # Coinbase
        "1FzWLkAahHooV3TzLvzv2YnuKFj3fx4m6B",  # Upbit
        "3Cjybp2r1tGgEUXG6oF1H1Q1r6t1Q1r6t1",  # Upbit
    ]
    
    print("🔍 WalletExplorer.com API 통합 테스트 시작")
    print("=" * 60)
    
    identifier = ExchangeIdentifier()
    
    for i, address in enumerate(test_addresses, 1):
        print(f"\n{i}. 주소 테스트: {address}")
        print("-" * 40)
        
        try:
            # 거래소 식별 실행
            result = identifier.identify_exchange(address)
            
            print(f"결과: {result['is_exchange']}")
            print(f"거래소: {result.get('exchange_name', 'N/A')}")
            print(f"신뢰도: {result.get('confidence', 'N/A')}")
            print(f"분석 근거: {result.get('analysis_basis', 'N/A')}")
            print(f"설명: {result.get('explanation', 'N/A')}")
            
            # 공개 DB 검색 결과
            if 'public_db_results' in result:
                public_db = result['public_db_results']
                if public_db.get('found'):
                    print(f"✅ 공개 DB 발견: {public_db.get('exchanges', [])}")
                    print(f"   소스: {public_db.get('sources', [])}")
                    print(f"   신뢰도: {public_db.get('confidence', 'N/A')}")
                else:
                    print("❌ 공개 DB에서 발견되지 않음")
            
        except Exception as e:
            print(f"❌ 오류: {e}")
        
        # 요청 간격 조절
        time.sleep(3)
    
    print("\n" + "=" * 60)
    print("✅ WalletExplorer.com API 통합 테스트 완료")

if __name__ == "__main__":
    test_walletexplorer_integration() 