import numpy as np
import pandas as pd
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import math
import re
from typing import Dict, List, Tuple, Optional
import streamlit as st

class ExchangePatternAnalyzer:
    """거래소 주소 패턴 분석기 - 엔트로피, 규칙성, 특징 추출"""
    
    def __init__(self):
        self.exchange_patterns = {
            'Binance': {
                'entropy_range': (3.2, 3.8),
                'amount_patterns': ['round_numbers', 'high_volume'],
                'time_patterns': ['regular_intervals', 'batch_processing'],
                'address_patterns': ['bc1_prefix', 'multiple_outputs']
            },
            'Upbit': {
                'entropy_range': (3.0, 3.6),
                'amount_patterns': ['korean_market', 'krw_conversion'],
                'time_patterns': ['korean_timezone', 'business_hours'],
                'address_patterns': ['legacy_format', 'single_output']
            },
            'Coinbase': {
                'entropy_range': (3.4, 3.9),
                'amount_patterns': ['usd_conversion', 'institutional'],
                'time_patterns': ['us_timezone', 'regular_schedules'],
                'address_patterns': ['segwit_format', 'multiple_outputs']
            },
            'OKX': {
                'entropy_range': (3.1, 3.7),
                'amount_patterns': ['asian_market', 'high_frequency'],
                'time_patterns': ['asian_timezone', 'continuous_trading'],
                'address_patterns': ['mixed_formats', 'high_volume']
            }
        }
    
    def calculate_address_entropy(self, address: str) -> float:
        """주소의 엔트로피 계산 (정보 이론 기반)"""
        if not address:
            return 0.0
        
        # 문자 빈도 계산
        char_freq = Counter(address)
        total_chars = len(address)
        
        # 엔트로피 계산: H = -Σ(p_i * log2(p_i))
        entropy = 0.0
        for count in char_freq.values():
            probability = count / total_chars
            if probability > 0:
                entropy -= probability * math.log2(probability)
        
        return entropy
    
    def analyze_amount_patterns(self, tx_list: List[Dict]) -> Dict:
        """금액 패턴 분석"""
        amounts = [tx.get('amount', 0) for tx in tx_list if tx.get('amount', 0) > 0]
        if not amounts:
            return {}
        
        analysis = {
            'total_volume': sum(amounts),
            'avg_amount': np.mean(amounts),
            'std_amount': np.std(amounts),
            'min_amount': min(amounts),
            'max_amount': max(amounts),
            'round_numbers': 0,
            'high_volume': 0,
            'krw_conversion': 0,
            'usd_conversion': 0
        }
        
        # 반올림 숫자 패턴 (1000, 10000, 100000 등)
        for amount in amounts:
            if amount % 1000 == 0:
                analysis['round_numbers'] += 1
            if amount > 1000000:  # 1 BTC 이상
                analysis['high_volume'] += 1
            # KRW 환산 패턴 (약 50,000,000원 = 1 BTC 기준)
            if 45000000 <= amount <= 55000000:
                analysis['krw_conversion'] += 1
            # USD 환산 패턴 (약 40,000 USD = 1 BTC 기준)
            if 35000000 <= amount <= 45000000:
                analysis['usd_conversion'] += 1
        
        return analysis
    
    def analyze_time_patterns(self, tx_list: List[Dict]) -> Dict:
        """시간 패턴 분석"""
        timestamps = []
        for tx in tx_list:
            try:
                if 'timestamp' in tx:
                    ts = datetime.fromisoformat(tx['timestamp'])
                    timestamps.append(ts)
            except:
                continue
        
        if len(timestamps) < 2:
            return {}
        
        # 시간대별 분석
        hours = [ts.hour for ts in timestamps]
        hour_distribution = Counter(hours)
        
        # 한국 시간대 (9-18시) vs 미국 시간대 (14-23시 UTC)
        korean_hours = sum(1 for h in hours if 9 <= h <= 18)
        us_hours = sum(1 for h in hours if 14 <= h <= 23)
        
        # 간격 분석
        sorted_times = sorted(timestamps)
        intervals = [(t2 - t1).total_seconds() for t1, t2 in zip(sorted_times[:-1], sorted_times[1:])]
        
        analysis = {
            'total_transactions': len(timestamps),
            'korean_timezone_ratio': korean_hours / len(hours) if hours else 0,
            'us_timezone_ratio': us_hours / len(hours) if hours else 0,
            'avg_interval': np.mean(intervals) if intervals else 0,
            'std_interval': np.std(intervals) if intervals else 0,
            'regular_intervals': 0,
            'batch_processing': 0
        }
        
        # 정규 간격 패턴 (30초-5분 간격)
        regular_count = sum(1 for interval in intervals if 30 <= interval <= 300)
        analysis['regular_intervals'] = regular_count / len(intervals) if intervals else 0
        
        # 배치 처리 패턴 (연속 트랜잭션)
        batch_count = sum(1 for interval in intervals if interval < 60)
        analysis['batch_processing'] = batch_count / len(intervals) if intervals else 0
        
        return analysis
    
    def analyze_address_patterns(self, tx_list: List[Dict]) -> Dict:
        """주소 패턴 분석"""
        addresses = []
        for tx in tx_list:
            if tx.get('to'):
                addresses.append(tx['to'])
            if tx.get('from'):
                addresses.append(tx['from'])
        
        if not addresses:
            return {}
        
        analysis = {
            'total_addresses': len(addresses),
            'unique_addresses': len(set(addresses)),
            'bc1_prefix': 0,
            'legacy_format': 0,
            'multiple_outputs': 0,
            'single_output': 0
        }
        
        for addr in addresses:
            if addr.startswith('bc1'):
                analysis['bc1_prefix'] += 1
            elif addr.startswith('1') or addr.startswith('3'):
                analysis['legacy_format'] += 1
        
        # 출력 개수 패턴
        for tx in tx_list:
            outputs = tx.get('outputs', [])
            if len(outputs) > 1:
                analysis['multiple_outputs'] += 1
            else:
                analysis['single_output'] += 1
        
        return analysis
    
    def calculate_exchange_similarity(self, tx_list: List[Dict], exchange_name: str) -> float:
        """특정 거래소와의 유사도 계산"""
        if not tx_list:
            return 0.0
        
        # 각 패턴 분석
        amount_patterns = self.analyze_amount_patterns(tx_list)
        time_patterns = self.analyze_time_patterns(tx_list)
        address_patterns = self.analyze_address_patterns(tx_list)
        
        # 엔트로피 계산
        addresses = [tx.get('to', '') for tx in tx_list if tx.get('to')]
        if addresses:
            avg_entropy = np.mean([self.calculate_address_entropy(addr) for addr in addresses])
        else:
            avg_entropy = 0.0
        
        # 거래소별 패턴 매칭
        exchange_pattern = self.exchange_patterns.get(exchange_name, {})
        similarity_score = 0.0
        total_checks = 0
        
        # 엔트로피 매칭
        if 'entropy_range' in exchange_pattern:
            min_entropy, max_entropy = exchange_pattern['entropy_range']
            if min_entropy <= avg_entropy <= max_entropy:
                similarity_score += 0.3
            total_checks += 1
        
        # 금액 패턴 매칭
        for pattern in exchange_pattern.get('amount_patterns', []):
            if pattern in amount_patterns:
                if amount_patterns[pattern] > 0:
                    similarity_score += 0.2
            total_checks += 1
        
        # 시간 패턴 매칭
        for pattern in exchange_pattern.get('time_patterns', []):
            if pattern in time_patterns:
                if time_patterns[pattern] > 0.3:  # 30% 이상
                    similarity_score += 0.2
            total_checks += 1
        
        # 주소 패턴 매칭
        for pattern in exchange_pattern.get('address_patterns', []):
            if pattern in address_patterns:
                if address_patterns[pattern] > 0:
                    similarity_score += 0.1
            total_checks += 1
        
        return (similarity_score / total_checks * 100) if total_checks > 0 else 0.0
    
    def identify_exchange_type(self, tx_list: List[Dict]) -> Dict:
        """거래소 유형 식별"""
        if not tx_list:
            return {}
        
        results = {}
        
        # 주요 거래소들과의 유사도 계산
        for exchange_name in self.exchange_patterns.keys():
            similarity = self.calculate_exchange_similarity(tx_list, exchange_name)
            results[exchange_name] = {
                'similarity': similarity,
                'confidence': 'high' if similarity > 70 else 'medium' if similarity > 50 else 'low'
            }
        
        # 가장 유사한 거래소 찾기
        best_match = max(results.items(), key=lambda x: x[1]['similarity'])
        
        return {
            'best_match': {
                'exchange': best_match[0],
                'similarity': best_match[1]['similarity'],
                'confidence': best_match[1]['confidence']
            },
            'all_matches': results,
            'analysis': {
                'amount_patterns': self.analyze_amount_patterns(tx_list),
                'time_patterns': self.analyze_time_patterns(tx_list),
                'address_patterns': self.analyze_address_patterns(tx_list),
                'entropy': self.calculate_address_entropy(tx_list[0].get('to', '')) if tx_list else 0.0
            }
        }
    
    def generate_exchange_report(self, tx_list: List[Dict]) -> str:
        """거래소 분석 리포트 생성"""
        if not tx_list:
            return "분석할 트랜잭션이 없습니다."
        
        identification = self.identify_exchange_type(tx_list)
        best_match = identification['best_match']
        analysis = identification['analysis']
        
        report = f"""
## 🏦 거래소 패턴 분석 리포트

### 📊 주요 발견사항
- **가장 유사한 거래소**: {best_match['exchange']}
- **유사도**: {best_match['similarity']:.1f}%
- **신뢰도**: {best_match['confidence']}

### 🔍 패턴 분석
**금액 패턴:**
- 총 거래량: {analysis['amount_patterns'].get('total_volume', 0):,.0f} satoshi
- 평균 거래량: {analysis['amount_patterns'].get('avg_amount', 0):,.0f} satoshi
- 반올림 숫자 패턴: {analysis['amount_patterns'].get('round_numbers', 0)}건
- 대용량 거래: {analysis['amount_patterns'].get('high_volume', 0)}건

**시간 패턴:**
- 한국 시간대 비율: {analysis['time_patterns'].get('korean_timezone_ratio', 0):.1%}
- 미국 시간대 비율: {analysis['time_patterns'].get('us_timezone_ratio', 0):.1%}
- 정규 간격 패턴: {analysis['time_patterns'].get('regular_intervals', 0):.1%}
- 배치 처리 패턴: {analysis['time_patterns'].get('batch_processing', 0):.1%}

**주소 패턴:**
- bc1 접두사: {analysis['address_patterns'].get('bc1_prefix', 0)}건
- 레거시 형식: {analysis['address_patterns'].get('legacy_format', 0)}건
- 다중 출력: {analysis['address_patterns'].get('multiple_outputs', 0)}건

**엔트로피 분석:**
- 주소 엔트로피: {analysis['entropy']:.2f} bits
"""
        
        return report

def analyze_exchange_patterns(tx_list: List[Dict]) -> Dict:
    """거래소 패턴 분석 메인 함수"""
    analyzer = ExchangePatternAnalyzer()
    return analyzer.identify_exchange_type(tx_list) 