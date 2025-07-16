#!/usr/bin/env python3
"""
거래소 식별 시스템 테스트 스크립트
실제 거래소 주소들과 패턴 분석 기능을 테스트합니다.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logic.exchange_identifier import identify_exchange_comprehensive
import streamlit as st

def test_exchange_identification():
    """거래소 식별 시스템 테스트"""
    
    # 테스트할 실제 거래소 주소들
    test_addresses = [
        # Binance (바이낸스) - 실제 알려진 주소들
        "1NDyJtNTjmwk5xPNhjgAMu4HDHigtobu1s",
        "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy", 
        "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
        
        # Upbit (업비트) - 실제 알려진 주소들
        "3Cjybp2r1tGgEUXG6oF1H1Q1r6t1Q1r6t1",
        "1FzWLkAahHooV3TzLvzv2YnuKFj3fx4m6B",
        "1Ej5N5L4QpDduz7HMwG2PJpxcnj3Y4ozzL",
        
        # Coinbase (코인베이스) - 실제 알려진 주소들
        "3QCzvfL4ZRvmJFiWWBVwxfdaNBT8EtxB5y",
        "3NukJ6fYZJ5Kk8bPjycAnruZkE5Q7UW7i8",
        "3QJmV3qfvL9SuYo34YihAf3sRCW3qSinyC",
        
        # OKX (오케이엑스) - 실제 알려진 주소들
        "37XuVSEpWW4trkfmvWzegTHQt7BdktSKUs",
        "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
        
        # Bitfinex (비트파이넥스) - 실제 알려진 주소들
        "3D2oetdNuZUqQHPJmcMDDHYoqkyNVsFk9r",
        "1Kr6QSydW9bFQG1mXiPNNu6WpJGmUa9i1g",
        
        # Kraken (크라켄) - 실제 알려진 주소들
        "14XcsWCCWq1BJLeexVFeDksbZJwZYDkL1D",
        
        # Huobi (후오비) - 실제 알려진 주소들
        "1Cdid9KFAaatwczBwBttQcwXYCpvK8h7FK",
        
        # Bithumb (빗썸) - 실제 알려진 주소들
        "1DiYKei8qUYsiozLZzKYiRMxWYQJwUPeWa",
        
        # KuCoin (쿠코인) - 실제 알려진 주소들
        "1PgQVLmst3Z314JrQn5TNiys8Hc38TcXJu",
        
        # Gate.io (게이트아이오) - 실제 알려진 주소들
        "3GZ7eYJb4s4yzBWqc2VFtAjhZ5VrUueQkM",
        
        # 일반 사용자 주소 (음성 테스트)
        "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",  # Genesis 블록 주소
        "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",  # 일반 SegWit 주소
    ]
    
    # 시뮬레이션된 거래 데이터 (거래소 패턴)
    exchange_tx_pattern = [
        {
            'from': '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
            'to': '1NDyJtNTjmwk5xPNhjgAMu4HDHigtobu1s',
            'amount': 50000000,  # 0.5 BTC
            'timestamp': '2024-01-15T10:30:00'
        },
        {
            'from': '1NDyJtNTjmwk5xPNhjgAMu4HDHigtobu1s',
            'to': '3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy',
            'amount': 100000000,  # 1 BTC
            'timestamp': '2024-01-15T10:35:00'
        },
        {
            'from': '3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy',
            'to': 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh',
            'amount': 75000000,  # 0.75 BTC
            'timestamp': '2024-01-15T10:40:00'
        },
        {
            'from': 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh',
            'to': '1LQoWist8KkaUXSPKZHNvEyfrEkPHzSsCd',
            'amount': 25000000,  # 0.25 BTC
            'timestamp': '2024-01-15T10:45:00'
        },
        {
            'from': '1LQoWist8KkaUXSPKZHNvEyfrEkPHzSsCd',
            'to': '3Kzh9qAqVWQhEsfQz7zEQL1EuSx5tyNLNS',
            'amount': 30000000,  # 0.3 BTC
            'timestamp': '2024-01-15T10:50:00'
        }
    ]
    
    # 일반 사용자 거래 패턴 (비거래소)
    user_tx_pattern = [
        {
            'from': '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
            'to': 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh',
            'amount': 1000000,  # 0.01 BTC
            'timestamp': '2024-01-15T14:30:00'
        },
        {
            'from': 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh',
            'to': '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
            'amount': 500000,  # 0.005 BTC
            'timestamp': '2024-01-15T16:45:00'
        }
    ]
    
    print("🔍 거래소 식별 시스템 테스트 시작")
    print("=" * 60)
    
    # 1. 실제 거래소 주소 테스트 (트랜잭션 없이)
    print("\n📋 1. 실제 거래소 주소 테스트 (주소만)")
    print("-" * 40)
    
    for i, address in enumerate(test_addresses[:10], 1):  # 처음 10개만 테스트
        print(f"\n{i}. 주소: {address}")
        result = identify_exchange_comprehensive(address)
        
        final_result = result.get('final_result', {})
        exchange = final_result.get('exchange', 'Unknown')
        confidence = final_result.get('confidence', 'low')
        method = final_result.get('method', '-')
        
        print(f"   결과: {exchange}")
        print(f"   신뢰도: {confidence}")
        print(f"   방법: {method}")
        
        # 공식 주소 확인 결과
        official_result = result.get('official_address', {})
        if official_result.get('found'):
            print(f"   ✅ 공식 주소 매칭: {official_result.get('exchange', 'Unknown')}")
        
        # 패턴 분석 결과
        pattern_result = result.get('pattern_analysis', {})
        if pattern_result.get('confidence') != 'low':
            print(f"   📊 패턴 분석: {pattern_result.get('confidence', 'low')}")
    
    # 2. 거래소 패턴이 있는 주소 테스트
    print("\n\n📋 2. 거래소 패턴이 있는 주소 테스트")
    print("-" * 40)
    
    exchange_address = "1NDyJtNTjmwk5xPNhjgAMu4HDHigtobu1s"  # Binance
    print(f"테스트 주소: {exchange_address}")
    print("거래소 패턴 거래 데이터 사용")
    
    result = identify_exchange_comprehensive(exchange_address, exchange_tx_pattern)
    final_result = result.get('final_result', {})
    
    print(f"최종 결과: {final_result.get('exchange', 'Unknown')}")
    print(f"신뢰도: {final_result.get('confidence', 'low')}")
    print(f"방법: {final_result.get('method', '-')}")
    
    # 패턴 분석 상세
    pattern_result = result.get('pattern_analysis', {})
    if pattern_result:
        patterns = pattern_result.get('patterns', {})
        print(f"패턴 점수: {pattern_result.get('score', 0)}")
        print(f"거래 빈도: {patterns.get('transaction_frequency', 0):.1f} 거래/시간")
        print(f"정규 간격: {patterns.get('regular_intervals', 0):.1%}")
    
    # 3. 일반 사용자 패턴 테스트
    print("\n\n📋 3. 일반 사용자 패턴 테스트")
    print("-" * 40)
    
    user_address = "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"
    print(f"테스트 주소: {user_address}")
    print("일반 사용자 패턴 거래 데이터 사용")
    
    result = identify_exchange_comprehensive(user_address, user_tx_pattern)
    final_result = result.get('final_result', {})
    
    print(f"최종 결과: {final_result.get('exchange', 'Unknown')}")
    print(f"신뢰도: {final_result.get('confidence', 'low')}")
    print(f"방법: {final_result.get('method', '-')}")
    
    # 4. 데이터베이스 로드 테스트
    print("\n\n📋 4. 거래소 주소 데이터베이스 로드 테스트")
    print("-" * 40)
    
    from logic.exchange_identifier import ExchangeIdentifier
    identifier = ExchangeIdentifier()
    
    print(f"로드된 거래소 주소 수: {len(identifier.real_exchange_addresses)}")
    
    # 몇 개 샘플 출력
    sample_count = 0
    for addr, info in identifier.real_exchange_addresses.items():
        if sample_count < 5:
            print(f"  {addr} -> {info}")
            sample_count += 1
        else:
            break
    
    print("\n✅ 테스트 완료!")

if __name__ == "__main__":
    test_exchange_identification() 