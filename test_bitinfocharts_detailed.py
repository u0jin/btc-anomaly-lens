#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time

def analyze_bitinfocharts_page(address):
    """BitInfoCharts 페이지 상세 분석"""
    
    url = f"https://bitinfocharts.com/bitcoin/address/{address}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        print(f"🔍 {address} 분석 중...")
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            print(f"✅ 페이지 로드 성공")
            
            # 페이지 제목 확인
            title = soup.find('title')
            if title:
                print(f"📄 페이지 제목: {title.get_text()}")
            
            # 메타 태그 확인
            meta_tags = soup.find_all('meta')
            for meta in meta_tags:
                if meta.get('name') and 'description' in meta.get('name').lower():
                    print(f"📝 메타 설명: {meta.get('content', '')}")
            
            # 거래소 관련 키워드 검색
            page_text = soup.get_text().lower()
            exchange_keywords = [
                'binance', 'coinbase', 'upbit', 'okx', 'bitfinex', 
                'kraken', 'huobi', 'kucoin', 'gate.io', 'exchange',
                'hot wallet', 'cold wallet', 'deposit', 'withdrawal'
            ]
            
            found_keywords = []
            for keyword in exchange_keywords:
                if keyword in page_text:
                    found_keywords.append(keyword)
            
            if found_keywords:
                print(f"✅ 발견된 키워드: {found_keywords}")
            else:
                print(f"❌ 거래소 관련 키워드를 찾을 수 없음")
            
            # 주소 정보 섹션 찾기
            address_info = soup.find_all(['div', 'span', 'p'], class_=lambda x: x and any(word in x.lower() for word in ['address', 'info', 'details']))
            print(f"📊 주소 정보 섹션 수: {len(address_info)}")
            
            # 첫 번째 주소 정보 섹션의 텍스트 출력
            if address_info:
                first_section = address_info[0]
                section_text = first_section.get_text()[:200]  # 처음 200자만
                print(f"📋 첫 번째 섹션 텍스트: {section_text}...")
            
            return True
            
        else:
            print(f"❌ HTTP 오류: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False

def main():
    """메인 테스트 함수"""
    
    test_addresses = [
        "1NDyJtNTjmwk5xPNhjgAMu4HDHigtobu1s",  # Binance
        "3QCzvfL4ZRvmJFiWWBVwxfdaNBT8EtxB5y",  # Coinbase
    ]
    
    print("🔍 BitInfoCharts 상세 분석")
    print("=" * 50)
    
    for i, address in enumerate(test_addresses, 1):
        print(f"\n{i}. 주소: {address}")
        print("-" * 40)
        
        analyze_bitinfocharts_page(address)
        
        # 요청 간격 조절
        time.sleep(2)
        print()

if __name__ == "__main__":
    main() 