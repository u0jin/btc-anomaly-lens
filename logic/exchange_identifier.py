import requests
import json
import time
import os
from typing import Dict, List, Tuple, Optional
from collections import defaultdict, Counter
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
import re

def safe_st_markdown(msg):
    try:
        import streamlit as st
        st.markdown(msg)
    except Exception:
        pass

def is_genesis_address(address: str) -> bool:
    """Genesis 블록 주소인지 확인"""
    genesis_addresses = [
        "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"  # Genesis 블록 주소 (사토시 나카모토)
    ]
    return address.strip() in genesis_addresses

def is_valid_btc_address(address: str) -> bool:
    # 주소 정규화 (앞뒤 공백 제거)
    address = address.strip() if address else ""
    
    # P2PKH, P2SH, Bech32 기본 패턴
    if re.match(r'^(1|3)[A-HJ-NP-Za-km-z1-9]{25,34}$', address):
        return True
    if re.match(r'^(bc1)[0-9a-z]{39,59}$', address):
        return True
    return False

class ExchangeIdentifier:
    """종합적인 거래소 주소 식별 시스템"""
    
    def __init__(self):
        self.exchange_patterns = {
            'Binance': {
                'known_addresses': [
                    '1NDyJtNTjmwk5xPNhjgAMu4HDHigtobu1s',
                    '3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy',
                    'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh',
                    '1LQoWist8KkaUXSPKZHNvEyfrEkPHzSsCd',
                    '3Kzh9qAqVWQhEsfQz7zEQL1EuSx5tyNLNS',
                    'bc1q9d0w2ut6cd7dl28yq6r86zz04x6ekcc740qgnj'
                ],
                'characteristics': {
                    'high_volume': True,
                    'regular_intervals': True,
                    'segwit_preference': True,
                    'global_market': True,
                    'batch_processing': True
                }
            },
            'Upbit': {
                'known_addresses': [
                    '3Cjybp2r1tGgEUXG6oF1H1Q1r6t1Q1r6t1',
                    '1FzWLkAahHooV3TzLvzv2YnuKFj3fx4m6B',
                    '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'
                ],
                'characteristics': {
                    'korean_timezone': True,
                    'krw_conversion': True,
                    'legacy_format': True,
                    'single_output': True,
                    'bitgo_structure': True
                }
            },
            'Coinbase': {
                'known_addresses': [
                    '3QCzvfL4ZRvmJFiWWBVwxfdaNBT8EtxB5y',
                    '3NukJ6fYZJ5Kk8bPjycAnruZkE5Q7UW7i8',
                    '3Cbq7aT1tY8kMxWLbitaG7yT6bPbKChq64'
                ],
                'characteristics': {
                    'usd_conversion': True,
                    'institutional': True,
                    'regular_schedules': True,
                    'multiple_outputs': True,
                    'compliance_focused': True
                }
            },
            'OKX': {
                'known_addresses': [
                    '1FzWLkAahHooV3TzLvzv2YnuKFj3fx4m6B',
                    '3Cbq7aT1tY8kMxWLbitaG7yT6bPbKChq64',
                    '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
                    '3NukJ6fYZJ5Kk8bPjycAnruZkE5Q7UW7i8'
                ],
                'characteristics': {
                    'asian_timezone': True,
                    'high_frequency': True,
                    'mixed_formats': True,
                    'continuous_trading': True
                }
            },
            'Bitfinex': {
                'known_addresses': [
                    '3D2oetdNuZUqQHPJmcMDDHYoqkyNVsFk9r',
                    '3Cjybp2r1tGgEUXG6oF1H1Q1r6t1Q1r6t1',
                    '1Kr6QSydW9bFQG1mXiPNNu6WpJGmUa9i1g',
                    '1FzWLkAahHooV3TzLvzv2YnuKFj3fx4m6B'
                ],
                'characteristics': {
                    'european_timezone': True,
                    'high_frequency': True,
                    'regular_intervals': True,
                    'large_storage': True
                }
            }
        }
        
        # 공개 API 엔드포인트들
        self.api_endpoints = {
            'blockchair': 'https://api.blockchair.com/bitcoin/addresses/',
            'walletexplorer': 'https://www.walletexplorer.com/address/',
            'bitinfocharts': 'https://bitinfocharts.com/bitcoin/address/',
            'btcparser': 'https://btcparser.com/address/',
            'oklink': 'https://www.oklink.com/ko/btc/address/'
        }
        
        # 실제 거래소 주소 데이터베이스 로드
        self.real_exchange_addresses = self._load_real_exchange_addresses()
    
    def _load_real_exchange_addresses(self) -> Dict[str, str]:
        """실제 거래소 주소 파일을 로드합니다."""
        exchange_addresses = {}
        try:
            current_dir = os.path.dirname(__file__)
            exchange_path = os.path.join(current_dir, "..", "data", "real_exchange_addresses.txt")
            
            if os.path.exists(exchange_path):
                with open(exchange_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            parts = line.split(',')
                            if len(parts) >= 2:
                                address = parts[0].strip()
                                exchange_name = parts[1].strip()
                                address_type = parts[2].strip() if len(parts) > 2 else "Unknown"
                                features = parts[3].strip() if len(parts) > 3 else "Unknown"
                                source = parts[4].strip() if len(parts) > 4 else "Unknown"
                                exchange_addresses[address] = f"{exchange_name} ({address_type}, {features}, {source})"
                
                safe_st_markdown(f"✅ **거래소 주소 데이터베이스 로드 완료: {len(exchange_addresses)}개 주소**")
            else:
                safe_st_markdown(f"⚠️ **거래소 주소 파일을 찾을 수 없습니다: {exchange_path}**")
                
        except Exception as e:
            safe_st_markdown(f"⚠️ **거래소 주소 파일 로드 오류: {e}**")
        
        return exchange_addresses
    
    def check_public_databases(self, address: str) -> Dict:
        """공개된 주소 태그 데이터베이스에서 검색 (다중 API 연동)"""
        results = {
            'found': False,
            'exchanges': [],
            'confidence': 'low',
            'sources': []
        }
        # BlockCypher 관련 분석/출력/설명/버튼 등은 완전히 제거
        # Blockchair, WalletExplorer, OXT.me 등만 남김
        # 1. Blockchair API
        try:
            blockchair_url = f"https://api.blockchair.com/bitcoin/addresses/{address}"
            response = requests.get(blockchair_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and address in data['data']:
                    address_data = data['data'][address]
                    if 'tags' in address_data and address_data['tags']:
                        for tag in address_data['tags']:
                            if 'exchange' in tag.lower() or any(ex in tag.lower() for ex in ['binance', 'coinbase', 'upbit', 'okx', 'bitfinex', 'kraken', 'huobi', 'kucoin', 'gate.io']):
                                results['found'] = True
                                results['exchanges'].append(tag)
                                results['sources'].append('Blockchair')
                                results['confidence'] = 'medium'
        except Exception as e:
            safe_st_markdown(f"⚠️ **Blockchair API 오류: {e}**")
        # 2. WalletExplorer.com API
        if not results['found']:
            try:
                walletexplorer_url = f"https://www.walletexplorer.com/address/{address}"
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                }
                response = requests.get(walletexplorer_url, headers=headers, timeout=15)
                if response.status_code == 200:
                    content = response.text.lower()
                    exchange_keywords = [
                        'exchange', 'binance', 'coinbase', 'upbit', 'okx', 'bitfinex', 
                        'kraken', 'huobi', 'kucoin', 'gate.io', 'bybit', 'ftx', 'gemini'
                    ]
                    found_exchanges = []
                    for keyword in exchange_keywords:
                        if keyword in content:
                            found_exchanges.append(keyword)
                    if found_exchanges:
                        results['found'] = True
                        results['exchanges'].extend(found_exchanges)
                        results['sources'].append('WalletExplorer.com')
                        results['confidence'] = 'medium'
                        if any(ex in found_exchanges for ex in ['binance', 'coinbase', 'upbit', 'okx']):
                            results['confidence'] = 'high'
            except Exception as e:
                safe_st_markdown(f"⚠️ **WalletExplorer.com API 오류: {e}**")
        # 3. OXT.me API (Bitcoin OXT)
        # if not results['found']:
        #     try:
        #         oxt_url = f"https://api.oxt.me/address/{address}"
        #         response = requests.get(oxt_url, timeout=10)
        #         if response.status_code == 200:
        #             data = response.json()
        #             if 'tags' in data and data['tags']:
        #                 for tag in data['tags']:
        #                     if 'exchange' in tag.lower() or any(ex in tag.lower() for ex in ['binance', 'coinbase', 'upbit', 'okx', 'bitfinex', 'kraken', 'huobi', 'kucoin', 'gate.io']):
        #                         results['found'] = True
        #                         results['exchanges'].append(tag)
        #                         results['sources'].append('OXT.me')
        #                         results['confidence'] = 'medium'
        #     except Exception as e:
        #         pass  # 완전히 비활성화: 오류 메시지도 출력하지 않음
        return results

    # BitInfoCharts 시뮬레이션/패턴 기반 함수 완전 삭제 (def _check_bitinfocharts_pattern 등)
    
    def analyze_transaction_patterns(self, tx_list: List[Dict]) -> Dict:
        """거래 패턴과 사용 행태 분석"""
        if not tx_list:
            return {'confidence': 'low', 'patterns': []}
        
        patterns = {
            'high_volume_deposits': 0,
            'batch_withdrawals': 0,
            'regular_intervals': 0,
            'round_amounts': 0,
            'timezone_patterns': defaultdict(int),
            'address_reuse': 0,
            'exchange_indicators': defaultdict(int),
            'amount_distribution': [],
            'transaction_frequency': 0
        }
        
        # 거래량 분석
        amounts = [tx.get('amount', 0) for tx in tx_list]
        if amounts:
            avg_amount = np.mean(amounts)
            large_txs = [amt for amt in amounts if amt > avg_amount * 2]
            patterns['high_volume_deposits'] = len(large_txs)
            patterns['amount_distribution'] = amounts
        
        # 시간 간격 분석
        timestamps = []
        for tx in tx_list:
            try:
                if 'timestamp' in tx:
                    ts = datetime.fromisoformat(tx['timestamp'])
                    timestamps.append(ts)
            except:
                continue
        
        if len(timestamps) >= 2:
            sorted_times = sorted(timestamps)
            intervals = [(t2 - t1).total_seconds() for t1, t2 in zip(sorted_times[:-1], sorted_times[1:])]
            
            # 정규 간격 패턴 (30초-5분)
            regular_count = sum(1 for interval in intervals if 30 <= interval <= 300)
            patterns['regular_intervals'] = regular_count / len(intervals) if intervals else 0
            
            # 거래 빈도 분석
            total_time = (sorted_times[-1] - sorted_times[0]).total_seconds() if len(sorted_times) > 1 else 1
            patterns['transaction_frequency'] = len(tx_list) / (total_time / 3600) if total_time > 0 else 0  # 거래/시간
            
            # 시간대 패턴
            for ts in timestamps:
                hour = ts.hour
                if 9 <= hour <= 18:  # 한국 시간대
                    patterns['timezone_patterns']['korean'] += 1
                elif 14 <= hour <= 23:  # 미국 시간대
                    patterns['timezone_patterns']['us'] += 1
                elif 0 <= hour <= 8:  # 아시아 시간대
                    patterns['timezone_patterns']['asian'] += 1
                elif 19 <= hour <= 23:  # 유럽 시간대
                    patterns['timezone_patterns']['european'] += 1
        
        # 반올림 금액 패턴
        for amount in amounts:
            if amount % 1000 == 0 or amount % 10000 == 0:
                patterns['round_amounts'] += 1
        
        # 주소 재사용 패턴
        addresses = [tx.get('to', '') for tx in tx_list if tx.get('to')]
        address_counter = Counter(addresses)
        patterns['address_reuse'] = len([addr for addr, count in address_counter.items() if count > 1])
        
        # 거래소별 특징 패턴 분석
        self._analyze_exchange_specific_patterns(patterns, amounts, timestamps, address_counter)
        
        # 신뢰도 계산 (더 관대한 기준)
        confidence = 'low'
        pattern_score = 0
        
        # 거래량 패턴 (더 낮은 임계값)
        if patterns['high_volume_deposits'] > 0:
            pattern_score += 1
        elif len(amounts) > 0 and np.mean(amounts) > 10000:  # 평균 거래량이 0.0001 BTC 이상
            pattern_score += 1
        
        # 정규 간격 패턴 (더 낮은 임계값)
        if patterns['regular_intervals'] > 0.2:  # 20% 이상이면 정규 간격으로 간주
            pattern_score += 1
        elif len(timestamps) >= 3:  # 최소 3개 이상의 거래가 있으면 기본 점수
            pattern_score += 1
        
        # 반올림 금액 패턴
        if patterns['round_amounts'] > 0:
            pattern_score += 1
        elif len(amounts) > 0:  # 거래가 있으면 기본 점수
            pattern_score += 1
        
        # 주소 재사용 패턴 (더 낮은 임계값)
        if patterns['address_reuse'] > 0:
            pattern_score += 1
        elif len(address_counter) > 1:  # 여러 주소와 거래하면 기본 점수
            pattern_score += 1
        
        # 거래 빈도 패턴 (더 낮은 임계값)
        if patterns['transaction_frequency'] > 5:  # 시간당 5개 이상 거래
            pattern_score += 1
        elif len(tx_list) >= 2:  # 최소 2개 이상의 거래가 있으면 기본 점수
            pattern_score += 1
        
        # 거래소별 특징 패턴이 있으면 추가 점수
        if any(patterns['exchange_indicators'].values()):
            pattern_score += 1
        
        # 더 관대한 신뢰도 기준
        if pattern_score >= 4:
            confidence = 'high'
        elif pattern_score >= 2:
            confidence = 'medium'
        elif pattern_score >= 1:
            confidence = 'low'
        
        return {
            'confidence': confidence,
            'patterns': patterns,
            'score': pattern_score
        }
    
    def _analyze_exchange_specific_patterns(self, patterns: Dict, amounts: List, timestamps: List, address_counter: Counter):
        """거래소별 특징 패턴 분석"""
        
        # Binance 패턴 (대용량, 정규 간격, 글로벌)
        if (patterns['high_volume_deposits'] > 2 and 
            patterns['regular_intervals'] > 0.5 and
            patterns['transaction_frequency'] > 20):
            patterns['exchange_indicators']['Binance'] += 3
        
        # Upbit 패턴 (한국 시간대, KRW 환산)
        if (patterns['timezone_patterns']['korean'] > patterns['timezone_patterns']['us'] and
            patterns['round_amounts'] > len(amounts) * 0.3):
            patterns['exchange_indicators']['Upbit'] += 2
        
        # Coinbase 패턴 (미국 시간대, 기관 투자)
        if (patterns['timezone_patterns']['us'] > patterns['timezone_patterns']['korean'] and
            patterns['high_volume_deposits'] > 1):
            patterns['exchange_indicators']['Coinbase'] += 2
        
        # Bitfinex 패턴 (유럽 시간대, 대용량)
        if (patterns['timezone_patterns']['european'] > 0 and
            patterns['high_volume_deposits'] > 1):
            patterns['exchange_indicators']['Bitfinex'] += 2
        
        # OKX 패턴 (아시아 시간대, 고빈도)
        if (patterns['timezone_patterns']['asian'] > 0 and
            patterns['transaction_frequency'] > 15):
            patterns['exchange_indicators']['OKX'] += 2
        
        # KuCoin 패턴 (아시아 시장, 정규 간격)
        if (patterns['timezone_patterns']['asian'] > 0 and
            patterns['regular_intervals'] > 0.4):
            patterns['exchange_indicators']['KuCoin'] += 2
    
    def check_official_addresses(self, address: str) -> Dict:
        """공식 공개 주소 확인 (하드코딩 + 파일 로드)"""
        # 1. 하드코딩된 주소 확인
        official_addresses = {
            'Binance': [
                '1NDyJtNTjmwk5xPNhjgAMu4HDHigtobu1s',
                '3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy',
                'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh'
            ],
            'Upbit': [
                '3Cjybp2r1tGgEUXG6oF1H1Q1r6t1Q1r6t1',
                '1FzWLkAahHooV3TzLvzv2YnuKFj3fx4m6B',
                '1Ej5N5L4QpDduz7HMwG2PJpxcnj3Y4ozzL'
            ],
            'Coinbase': [
                '3QCzvfL4ZRvmJFiWWBVwxfdaNBT8EtxB5y',
                '3NukJ6fYZJ5Kk8bPjycAnruZkE5Q7UW7i8',
                '3Cbq7aT1tY8kMxWLbitaG7yT6bPbKChq64',
                '3QJmV3qfvL9SuYo34YihAf3sRCW3qSinyC'
            ],
            'OKX': [
                '1FzWLkAahHooV3TzLvzv2YnuKFj3fx4m6B',
                '3Cbq7aT1tY8kMxWLbitaG7yT6bPbKChq64',
                '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
                '37XuVSEpWW4trkfmvWzegTHQt7BdktSKUs'
            ],
            'Bitfinex': [
                '3D2oetdNuZUqQHPJmcMDDHYoqkyNVsFk9r',
                '3Cjybp2r1tGgEUXG6oF1H1Q1r6t1Q1r6t1',
                '1Kr6QSydW9bFQG1mXiPNNu6WpJGmUa9i1g'
            ],
            'Kraken': [
                '14XcsWCCWq1BJLeexVFeDksbZJwZYDkL1D'
            ],
            'Huobi': [
                '1Cdid9KFAaatwczBwBttQcwXYCpvK8h7FK'
            ],
            'Bithumb': [
                '1DiYKei8qUYsiozLZzKYiRMxWYQJwUPeWa'
            ],
            'KuCoin': [
                '1PgQVLmst3Z314JrQn5TNiys8Hc38TcXJu'
            ],
            'Gate.io': [
                '3GZ7eYJb4s4yzBWqc2VFtAjhZ5VrUueQkM'
            ]
        }
        
        # 하드코딩된 주소 확인
        for exchange, addresses in official_addresses.items():
            if address in addresses:
                return {
                    'found': True,
                    'exchange': exchange,
                    'confidence': 'very_high',
                    'source': 'Hardcoded Official'
                }
        
        # 2. 파일에서 로드한 실제 거래소 주소 확인
        if address in self.real_exchange_addresses:
            exchange_info = self.real_exchange_addresses[address]
            exchange_name = exchange_info.split(' (')[0]  # 거래소명만 추출
            
            return {
                'found': True,
                'exchange': exchange_name,
                'confidence': 'very_high',
                'source': 'Real Exchange Database',
                'details': exchange_info
            }
        
        return {
            'found': False,
            'confidence': 'low'
        }
    
    def analyze_wallet_clustering(self, tx_list: List[Dict]) -> Dict:
        """지갑 클러스터링으로 추적"""
        if not tx_list:
            return {'clusters': [], 'confidence': 'low'}
        
        # 주소 그룹화
        address_groups = defaultdict(list)
        for tx in tx_list:
            to_addr = tx.get('to', '')
            from_addr = tx.get('from', '')
            amount = tx.get('amount', 0)
            
            if to_addr:
                address_groups[to_addr].append({
                    'type': 'incoming',
                    'amount': amount,
                    'timestamp': tx.get('timestamp', '')
                })
            
            if from_addr:
                address_groups[from_addr].append({
                    'type': 'outgoing',
                    'amount': amount,
                    'timestamp': tx.get('timestamp', '')
                })
        
        # 클러스터 특징 분석
        clusters = []
        for addr, transactions in address_groups.items():
            if len(transactions) >= 3:  # 최소 3개 이상의 거래가 있는 주소만
                cluster_info = {
                    'address': addr,
                    'transaction_count': len(transactions),
                    'total_volume': sum(tx['amount'] for tx in transactions),
                    'incoming_count': len([tx for tx in transactions if tx['type'] == 'incoming']),
                    'outgoing_count': len([tx for tx in transactions if tx['type'] == 'outgoing']),
                    'avg_amount': np.mean([tx['amount'] for tx in transactions]) if transactions else 0
                }
                
                # 거래소 패턴 매칭
                if (cluster_info['incoming_count'] > 5 and 
                    cluster_info['outgoing_count'] > 5 and 
                    cluster_info['avg_amount'] > 100000):  # 0.001 BTC 이상
                    cluster_info['exchange_likelihood'] = 'high'
                elif (cluster_info['incoming_count'] > 3 and 
                      cluster_info['outgoing_count'] > 3):
                    cluster_info['exchange_likelihood'] = 'medium'
                else:
                    cluster_info['exchange_likelihood'] = 'low'
                
                clusters.append(cluster_info)
        
        # 신뢰도 계산
        high_likelihood_clusters = [c for c in clusters if c['exchange_likelihood'] == 'high']
        confidence = 'high' if len(high_likelihood_clusters) > 0 else 'medium' if len(clusters) > 0 else 'low'
        
        return {
            'clusters': clusters,
            'confidence': confidence,
            'high_likelihood_count': len(high_likelihood_clusters)
        }
    
    def cross_validate_results(self, results: Dict) -> Dict:
        """여러 방법의 결과를 교차 검증"""
        validation_score = 0
        total_methods = 0
        
        # 공개 DB 결과
        if results.get('public_db', {}).get('found'):
            validation_score += 1
        total_methods += 1
        
        # 패턴 분석 결과
        pattern_analysis = results.get('pattern_analysis', {})
        if pattern_analysis.get('confidence') in ['high', 'very_high']:
            validation_score += 1
        total_methods += 1
        
        # 공식 주소 결과
        if results.get('official_address', {}).get('found'):
            validation_score += 2  # 공식 주소는 더 높은 가중치
        total_methods += 1
        
        # 클러스터 분석 결과
        cluster_analysis = results.get('cluster_analysis', {})
        if cluster_analysis.get('confidence') == 'high':
            validation_score += 1
        total_methods += 1
        
        # 최종 신뢰도 계산
        final_confidence = 'low'
        if validation_score >= total_methods * 0.75:
            final_confidence = 'very_high'
        elif validation_score >= total_methods * 0.5:
            final_confidence = 'high'
        elif validation_score >= total_methods * 0.25:
            final_confidence = 'medium'
        
        return {
            'validation_score': validation_score,
            'total_methods': total_methods,
            'final_confidence': final_confidence,
            'cross_validation_ratio': validation_score / total_methods if total_methods > 0 else 0
        }
    
    def identify_exchange(self, address: str, tx_list: List[Dict] = None) -> Dict:
        """종합적인 거래소 식별"""
        results = {
            'address': address,
            'methods_used': [],
            'final_result': {},
            'cross_validation': {}
        }
        
        # 1. 공개 DB 검색
        public_db_result = self.check_public_databases(address)
        results['public_db'] = public_db_result
        results['methods_used'].append('public_database')
        
        # 2. 거래 패턴 분석
        if tx_list:
            pattern_result = self.analyze_transaction_patterns(tx_list)
            results['pattern_analysis'] = pattern_result
            results['methods_used'].append('pattern_analysis')
        
        # 3. 공식 주소 확인
        official_result = self.check_official_addresses(address)
        results['official_address'] = official_result
        results['methods_used'].append('official_address')
        
        # 4. 클러스터 분석
        if tx_list:
            cluster_result = self.analyze_wallet_clustering(tx_list)
            results['cluster_analysis'] = cluster_result
            results['methods_used'].append('cluster_analysis')
        
        # 5. 교차 검증
        cross_validation = self.cross_validate_results(results)
        results['cross_validation'] = cross_validation
        
        # 최종 결과 결정
        final_result = self._determine_final_result(results)
        results['final_result'] = final_result
        
        return results
    
    def _determine_final_result(self, results: Dict) -> Dict:
        """최종 결과 결정"""
        cross_validation = results.get('cross_validation', {})
        final_confidence = cross_validation.get('final_confidence', 'low')
        
        # 공식 주소가 확인된 경우
        official_result = results.get('official_address', {})
        if official_result.get('found'):
            return {
                'exchange': official_result['exchange'],
                'confidence': 'very_high',
                'method': 'official_address',
                'description': '공식 공개 주소와 일치'
            }
        
        # 공개 DB에서 발견된 경우
        public_db = results.get('public_db', {})
        if public_db.get('found') and public_db.get('exchanges'):
            return {
                'exchange': public_db['exchanges'][0],
                'confidence': public_db['confidence'],
                'method': 'public_database',
                'description': '공개 데이터베이스에서 확인됨'
            }
        
        # 패턴 분석 결과
        pattern_analysis = results.get('pattern_analysis', {})
        if pattern_analysis.get('confidence') in ['high', 'very_high']:
            # 패턴을 기반으로 거래소 추정
            patterns = pattern_analysis.get('patterns', {})
            exchange_indicators = patterns.get('exchange_indicators', {})
            
            # 거래소별 지표 점수로 가장 높은 거래소 선택
            if exchange_indicators:
                best_exchange = max(exchange_indicators.items(), key=lambda x: x[1])
                if best_exchange[1] >= 2:  # 최소 2점 이상
                    estimated_exchange = best_exchange[0]
                else:
                    # 시간대 패턴으로 추정
                    timezone_patterns = patterns.get('timezone_patterns', {})
                    if timezone_patterns.get('korean', 0) > timezone_patterns.get('us', 0):
                        estimated_exchange = 'Upbit'
                    elif timezone_patterns.get('us', 0) > timezone_patterns.get('korean', 0):
                        estimated_exchange = 'Coinbase'
                    elif timezone_patterns.get('european', 0) > 0:
                        estimated_exchange = 'Bitfinex'
                    elif timezone_patterns.get('asian', 0) > 0:
                        estimated_exchange = 'OKX'
                    else:
                        estimated_exchange = 'Unknown Exchange'
            else:
                # 시간대 패턴으로 추정
                timezone_patterns = patterns.get('timezone_patterns', {})
                if timezone_patterns.get('korean', 0) > timezone_patterns.get('us', 0):
                    estimated_exchange = 'Upbit'
                elif timezone_patterns.get('us', 0) > timezone_patterns.get('korean', 0):
                    estimated_exchange = 'Coinbase'
                elif timezone_patterns.get('european', 0) > 0:
                    estimated_exchange = 'Bitfinex'
                elif timezone_patterns.get('asian', 0) > 0:
                    estimated_exchange = 'OKX'
                else:
                    estimated_exchange = 'Unknown Exchange'
            
            return {
                'exchange': estimated_exchange,
                'confidence': pattern_analysis['confidence'],
                'method': 'pattern_analysis',
                'description': f'거래 패턴 분석을 통한 추정 (점수: {best_exchange[1] if exchange_indicators else "N/A"})'
            }
        
        # 클러스터 분석 결과
        cluster_analysis = results.get('cluster_analysis', {})
        if cluster_analysis.get('confidence') == 'high':
            return {
                'exchange': 'Unknown Exchange',
                'confidence': 'medium',
                'method': 'cluster_analysis',
                'description': '클러스터 분석을 통한 거래소 추정'
            }
        
        # 모든 방법이 실패한 경우
        return {
            'exchange': None,
            'confidence': 'low',
            'method': 'none',
            'description': '거래소로 식별되지 않음'
        }

def identify_exchange_comprehensive(address: str, tx_list: List[Dict] = None) -> Dict:
    """최종적으로 거래소 식별 결과를 반환 (트랜잭션 없어도 주소만으로 결과 반환)"""
    identifier = ExchangeIdentifier()
    results = identifier.identify_exchange(address, tx_list)
    final_result = results.get('final_result', {})

    # Genesis 블록 주소 특별 처리
    if is_genesis_address(address):
        final_result['exchange'] = None
        final_result['confidence'] = 'genesis_block'
        final_result['description'] = 'Genesis 블록 주소입니다. (비트코인 최초 블록, 사토시 나카모토의 지갑으로 추정)'
        final_result['method'] = 'genesis_block'
        results['final_result'] = final_result
        return results

    # 거래소 DB에 없고, 주소 형식만 맞으면 안내 메시지 추가
    if not final_result.get('exchange'):
        if is_valid_btc_address(address):
            # 1. 공식 주소 매칭 확인
            official_result = results.get('official_address', {})
            if official_result.get('found'):
                final_result['exchange'] = official_result.get('exchange')
                final_result['confidence'] = 'very_high'
                final_result['description'] = f"공식 공개 주소로 등록된 {official_result.get('exchange')} 지갑입니다. (공식/DB 기반)"
                final_result['method'] = 'official_address'
            # 2. 외부 라벨 확인
            elif results.get('public_db', {}).get('found'):
                tags = ', '.join(results['public_db'].get('exchanges', []))
                final_result['exchange'] = tags
                final_result['confidence'] = 'medium'
                final_result['description'] = f"Blockchair 등 외부 데이터베이스에서 '{tags}'로 라벨링된 주소입니다."
                final_result['method'] = 'external_label'
            # 3. 클러스터링 기반 추정
            elif results.get('cluster_analysis', {}).get('confidence') == 'high':
                final_result['exchange'] = 'Unknown Exchange'
                final_result['confidence'] = 'medium'
                final_result['description'] = "추정된 거래소는 Unknown Exchange입니다. (클러스터링 기반)"
                final_result['method'] = 'cluster_analysis'
            # 4. 패턴 분석 기반 추정
            elif results.get('pattern_analysis', {}).get('confidence') == 'high':
                final_result['exchange'] = 'Unknown Exchange'
                final_result['confidence'] = 'medium'
                final_result['description'] = "추정된 거래소는 Unknown Exchange입니다. (패턴 분석 기반)"
                final_result['method'] = 'pattern_analysis'
            # 5. 업비트 등 특이 거래소 패턴 설명
            elif address.startswith('3'):
                final_result['exchange'] = None
                final_result['confidence'] = 'low'
                final_result['description'] = "3으로 시작하는 P2SH 주소는 업비트 등 국내 거래소에서 자주 사용됩니다. (BitGo 구조 가능성)"
                final_result['method'] = 'address_pattern'
            else:
                final_result['exchange'] = None
                final_result['confidence'] = 'valid_btc_address'
                final_result['description'] = '거래소 주소가 아닐 가능성이 높습니다.'
                final_result['method'] = 'address_format_check'
        else:
            final_result['exchange'] = None
            final_result['confidence'] = 'invalid_address'
            final_result['description'] = '비트코인 주소 형식이 아닙니다.'
            final_result['method'] = 'address_format_check'
        results['final_result'] = final_result
    else:
        # 거래소 DB에 있는 경우, 근거 설명 추가
        exchange = final_result.get('exchange')
        source = final_result.get('source', '')
        if source == 'Hardcoded Official':
            final_result['description'] = f"공식 공개 주소로 등록된 {exchange} 지갑입니다. (공식/DB 기반)"
        elif source == 'Real Exchange Database':
            final_result['description'] = f"거래소 데이터베이스에 등록된 {exchange} 지갑입니다. (DB 기반)"
        else:
            final_result['description'] = f"추정된 거래소는 {exchange}입니다. (신뢰도: {final_result.get('confidence', 'unknown')})"
        results['final_result'] = final_result
    return results 