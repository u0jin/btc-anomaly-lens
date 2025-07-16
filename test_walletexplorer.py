#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
from logic.exchange_identifier import ExchangeIdentifier

def test_walletexplorer_api():
    """WalletExplorer.com API 테스트"""
    
    # 테스트할 거래소 주소들
    test_addresses = [
        "1NDyJtNTjmwk5xPNhjgAMu4HDHigtobu1s",  # Binance
        "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy",  # Binance
        "3QCzvfL4ZRvmJFiWWBVwxfdaNBT8EtxB5y",  # Coinbase
        "3NukJ6fYZJ5Kk8bPjycAnruZkE5Q7UW7i8",  # Coinbase
        "1FzWLkAahHooV3TzLvzv2YnuKFj3fx4m6B",  # Upbit
        "3Cjybp2r1tGgEUXG6oF1H1Q1r6t1Q1r6t1",  # Upbit
    ]
    
    print("🔍 WalletExplorer.com API 테스트 시작")
    print("=" * 50)
    
    for i, address in enumerate(test_addresses, 1):
        print(f"\n{i}. 주소 테스트: {address}")
        
        try:
            # WalletExplorer.com API 호출
            url = f"https://www.walletexplorer.com/address/{address}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            print(f"   상태 코드: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text.lower()
                print(f"   응답 길이: {len(content)} 문자")
                
                # 거래소 키워드 검색
                exchange_keywords = [
                    'exchange', 'binance', 'coinbase', 'upbit', 'okx', 'bitfinex', 
                    'kraken', 'huobi', 'kucoin', 'gate.io', 'bybit', 'ftx', 'gemini'
                ]
                
                found_keywords = []
                for keyword in exchange_keywords:
                    if keyword in content:
                        found_keywords.append(keyword)
                
                if found_keywords:
                    print(f"   ✅ 발견된 거래소 키워드: {', '.join(found_keywords)}")
                else:
                    print(f"   ❌ 거래소 키워드 없음")
                
                # 페이지 제목 확인
                if '<title>' in content:
                    title_start = content.find('<title>') + 7
                    title_end = content.find('</title>')
                    if title_end > title_start:
                        title = content[title_start:title_end].strip()
                        print(f"   페이지 제목: {title}")
                
            else:
                print(f"   ❌ API 호출 실패")
                
        except Exception as e:
            print(f"   ❌ 오류: {e}")
        
        # 요청 간격 조절
        time.sleep(2)
    
    print("\n" + "=" * 50)
    print("✅ WalletExplorer.com API 테스트 완료")

if __name__ == "__main__":
    test_walletexplorer_api() 