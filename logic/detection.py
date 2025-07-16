from datetime import datetime
from collections import Counter
import numpy as np
import pandas as pd  # ✅ 이거 반드시 추가
import os
import streamlit as st # 경고 메시지 출력용

# 1. 거래 간격 이상 탐지 (60초 미만)
def interval_anomaly_score(tx_list):
    if len(tx_list) < 2:
        return 0, []
    try:
        timestamps = [
            datetime.fromisoformat(tx['timestamp'])
            for tx in tx_list
            if isinstance(tx, dict) and 'timestamp' in tx
        ]
    except Exception:
        return 0, []
    
    if len(timestamps) < 2:
        return 0, []

    intervals = [
        (t2 - t1).total_seconds()
        for t1, t2 in zip(timestamps[:-1], timestamps[1:])
    ]
    short_intervals = [i for i in intervals if i < 60]
    score = min(25, len(short_intervals) * 5)
    return score, short_intervals


# 2. 이상 금액 탐지 (IQR 이상)
def amount_anomaly_score(tx_list):
    values = [tx['amount'] for tx in tx_list if isinstance(tx, dict) and 'amount' in tx]
    if not values:
        return 0, []

    df = pd.DataFrame(values, columns=['amount'])
    q1 = df['amount'].quantile(0.25)
    q3 = df['amount'].quantile(0.75)
    iqr = q3 - q1
    threshold = q3 + 1.5 * iqr
    outliers = df[df['amount'] > threshold]['amount'].tolist()

    score = min(len(outliers) * 5, 25)
    return score, outliers

# 3. 동일 수신 주소 반복 탐지
def repeated_address_score(tx_list):
    targets = [tx.get('to') for tx in tx_list if isinstance(tx, dict) and tx.get('to')]

    counter = Counter(targets)
    flagged = [addr for addr, count in counter.items() if count >= 3]
    score = min(25, len(flagged) * 5)
    return score, flagged

# 4. 시계열 상 이상 간격 탐지
def time_gap_anomaly_score(tx_list):
    if len(tx_list) < 2:
        return 0, []
    try:
        timestamps = [datetime.fromisoformat(tx['timestamp']) for tx in tx_list]
    except Exception:
        return 0, []
    gaps = [
        (t2 - t1).total_seconds()
        for t1, t2 in zip(timestamps[:-1], timestamps[1:])
    ]
    abnormal = [g for g in gaps if g < 10 or g > 3600]
    score = min(15, len(abnormal) * 5)
    return score, abnormal

# 5. 블랙리스트 로딩 및 탐지
def load_blacklist():
    try:
        current_dir = os.path.dirname(__file__)
        blacklist_path = os.path.join(current_dir, "..", "data", "blacklist.txt")

        if not os.path.exists(blacklist_path):
            st.error(f"❌ blacklist.txt not found at: {blacklist_path}")
            return set()

        with open(blacklist_path, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    except Exception as e:
        st.markdown(f"⚠️ **블랙리스트 파일 오류: {e}**")
        return set()

def load_mixer_addresses():
    """믹서 주소들을 여러 파일에서 로드합니다."""
    try:
        current_dir = os.path.dirname(__file__)
        data_dir = os.path.join(current_dir, "..", "data")
        
        mixer_files = [
            "mixer_addresses.txt",      # Wasabi
            "samourai_mixer.txt",       # Samourai
            "joinmarket_mixer.txt",     # JoinMarket
            "other_mixers.txt"          # 기타 믹서들
        ]
        
        mixer_addresses = {}
        
        for filename in mixer_files:
            file_path = os.path.join(data_dir, filename)
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            parts = line.split(',')
                            if len(parts) >= 3:
                                address = parts[0].strip()
                                mixer_type = parts[1].strip()
                                source = parts[3].strip() if len(parts) > 3 else "Unknown"
                                mixer_addresses[address] = f"{mixer_type} ({source})"
            else:
                st.markdown(f"⚠️ **{filename} not found at: {file_path}**")
        
        return mixer_addresses
    except Exception as e:
        st.markdown(f"⚠️ **믹서 주소 파일 오류: {e}**")
        return {}

def load_bridge_addresses():
    """브릿지 주소들을 여러 파일에서 로드합니다."""
    try:
        current_dir = os.path.dirname(__file__)
        data_dir = os.path.join(current_dir, "..", "data")
        
        bridge_files = [
            "wbtc_bridge.txt",          # WBTC
            "renvm_bridge.txt",         # RenVM
            "multichain_bridge.txt",    # Multichain
            "binance_bridge.txt",       # Binance
            "coinbase_bridge.txt",      # Coinbase
            "other_bridges.txt"         # 기타 브릿지들
        ]
        
        bridge_addresses = {}
        
        for filename in bridge_files:
            file_path = os.path.join(data_dir, filename)
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            parts = line.split(',')
                            if len(parts) >= 3:
                                address = parts[0].strip()
                                bridge_type = parts[1].strip()
                                source = parts[3].strip() if len(parts) > 3 else "Unknown"
                                bridge_addresses[address] = f"{bridge_type} ({source})"
            else:
                st.markdown(f"⚠️ **{filename} not found at: {file_path}**")
        
        return bridge_addresses
    except Exception as e:
        st.markdown(f"⚠️ **브릿지 주소 파일 오류: {e}**")
        return {}

def load_exchange_addresses():
    """거래소 주소들을 파일에서 로드합니다."""
    try:
        current_dir = os.path.dirname(__file__)
        # 실제 거래소 주소 파일 우선 사용
        exchange_path = os.path.join(current_dir, "..", "data", "real_exchange_addresses.txt")
        if not os.path.exists(exchange_path):
            # 기존 파일로 폴백
            exchange_path = os.path.join(current_dir, "..", "data", "exchange_addresses.txt")
            if not os.path.exists(exchange_path):
                st.markdown(f"⚠️ **거래소 주소 파일을 찾을 수 없습니다: {exchange_path}**")
                return {}
        
        exchange_addresses = {}
        with open(exchange_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split(',')
                    if len(parts) >= 3:
                        address = parts[0].strip()
                        exch_name = parts[1].strip()
                        address_type = parts[2].strip() if len(parts) > 2 else "Unknown"
                        features = parts[3].strip() if len(parts) > 3 else "Unknown"
                        source = parts[4].strip() if len(parts) > 4 else "Unknown"
                        exchange_addresses[address] = f"{exch_name} ({address_type}, {features}, {source})"
        return exchange_addresses
    except Exception as e:
        st.markdown(f"⚠️ **거래소 주소 파일 오류: {e}**")
        return {}

def exchange_detection_score(tx_list, address=None):
    """거래소 주소와 연결된 입출금 여부 탐지 + 패턴 분석"""
    exchange_addresses = load_exchange_addresses()
    exchange_hits = set()
    exchange_details = {}
    
    # 거래소 주소 로드 완료 (디버깅 메시지 제거)
    
    for tx in tx_list:
        to_address = tx.get('to', '')
        from_address = tx.get('from', '')
        amount = tx.get('amount', 0)
        
        # 입금 (거래소로의 전송)
        if to_address in exchange_addresses:
            exchange_name = exchange_addresses[to_address].split(' (')[0]  # 거래소명만 추출
            exchange_hits.add(exchange_name)
            if exchange_name not in exchange_details:
                exchange_details[exchange_name] = {'deposits': [], 'withdrawals': []}
            exchange_details[exchange_name]['deposits'].append({
                'address': to_address,
                'amount': amount,
                'type': exchange_addresses[to_address]
            })
        
        # 출금 (거래소에서의 전송)
        if from_address in exchange_addresses:
            exchange_name = exchange_addresses[from_address].split(' (')[0]  # 거래소명만 추출
            exchange_hits.add(exchange_name)
            if exchange_name not in exchange_details:
                exchange_details[exchange_name] = {'deposits': [], 'withdrawals': []}
            exchange_details[exchange_name]['withdrawals'].append({
                'address': from_address,
                'amount': amount,
                'type': exchange_addresses[from_address]
            })
    
    # 패턴 분석 - 트랜잭션 루프 밖으로 이동
    pattern_analysis = {}
    if tx_list:
        try:
            from logic.exchange_pattern_analyzer import analyze_exchange_patterns
            from logic.exchange_identifier import identify_exchange_comprehensive
            
            # 기존 패턴 분석
            pattern_analysis = analyze_exchange_patterns(tx_list)
            
            # 종합 거래소 식별 시스템
            comprehensive_result = identify_exchange_comprehensive(address, tx_list) if address else None
            final_result = comprehensive_result['final_result'] if comprehensive_result else {}
            final_exchange = final_result.get('exchange', None)
            final_confidence = final_result.get('confidence', 'low')
            final_method = final_result.get('method', '-')
            description = final_result.get('description', '')
            cross_validation = comprehensive_result.get('cross_validation', {}) if comprehensive_result else {}
            methods_used = comprehensive_result.get('methods_used', []) if comprehensive_result else []
            # 단계별 성공/실패
            public_db_result = comprehensive_result.get('public_db', {}) if comprehensive_result else {}
            pattern_result = comprehensive_result.get('pattern_analysis', {}) if comprehensive_result else {}
            official_result = comprehensive_result.get('official_address', {}) if comprehensive_result else {}
            cluster_result = comprehensive_result.get('cluster_analysis', {}) if comprehensive_result else {}
            
            # 거래소 인식 결과는 app.py에서 처리하므로 여기서는 제거
            
            # 2. 단계별 진행상황 스텝바 (가로 행)
            steps = [
                ("공개 DB", public_db_result.get('found', False), "🌐"),
                ("패턴 분석", pattern_result.get('confidence', 'low') != 'low', "📈"),
                ("공식 주소", official_result.get('found', False), "🏛️"),
                ("클러스터", cluster_result.get('confidence', 'low') == 'high', "🔗"),
            ]
            
            # 가로 행으로 표시
            cols = st.columns(len(steps))
            for i, (name, success, icon) in enumerate(steps):
                with cols[i]:
                    color = "#08BDBD" if success else "#ccc"
                    status = "✅ 성공" if success else "❌ 실패"
                    st.markdown(f"""
                    <div style='text-align: center; padding: 12px; border: 2px solid {color}; border-radius: 8px; background: {color}22;'>
                        <div style='font-size: 28px; color: {color}; margin-bottom: 8px;'>{icon}</div>
                        <div style='font-size: 16px; color: {color}; font-weight: bold; margin-bottom: 4px;'>{name}</div>
                        <div style='font-size: 14px; color: {color};'>{status}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # 3. 교차 검증/세부 정보는 토글(expander)로
            with st.expander("🔬 교차 검증 상세 보기", expanded=False):
                st.markdown(f"""
                <ul>
                    <li>검증 점수: <b>{cross_validation.get('validation_score', 0)}/{cross_validation.get('total_methods', 0)}</b></li>
                    <li>검증 비율: <b>{cross_validation.get('cross_validation_ratio', 0):.1%}</b></li>
                    <li>최종 신뢰도: <b>{cross_validation.get('final_confidence', 'low')}</b></li>
                </ul>
                """, unsafe_allow_html=True)
                if methods_used:
                    st.markdown(f"**📋 사용된 식별 방법:**")
                    for method in methods_used:
                        method_names = {
                            'public_database': '공개 데이터베이스 검색',
                            'pattern_analysis': '거래 패턴 분석',
                            'official_address': '공식 주소 확인',
                            'cluster_analysis': '지갑 클러스터 분석'
                        }
                        st.caption(f"• {method_names.get(method, method)}")
        
        except Exception as e:
            st.markdown(f"⚠️ **패턴 분석 오류: {e}**")
    
    # 상세 정보와 패턴 분석을 함께 반환
    return list(exchange_hits), exchange_details, pattern_analysis

def blacklist_score(tx_list):
    blacklist = load_blacklist()
    involved = [tx.get('to') for tx in tx_list if isinstance(tx, dict) and tx.get('to') in blacklist]
    if involved:
        return True, 100  # 블랙리스트 주소가 포함되면 100점
    return False, 0

# 6. Mixer 탐지 기능
def mixer_detection_score(tx_list):
    """
    믹서(Mixer) 사용 여부를 탐지합니다.
    - Wasabi, Samourai, JoinMarket 등의 특징적인 패턴 탐지
    - 다중 입력/출력, 동일 금액, 시간 간격 패턴 분석
    """
    mixer_indicators = []
    mixer_score = 0
    
    if not tx_list:
        return mixer_score, mixer_indicators
    
    # 1. 알려진 믹서 주소 매칭
    known_mixer_addresses = load_mixer_addresses()
    mixer_hits = set()
    for tx in tx_list:
        to_address = tx.get('to', '')
        if to_address in known_mixer_addresses:
            mixer_hits.add(known_mixer_addresses[to_address])
    
    if mixer_hits:
        mixer_score += min(25, len(mixer_hits) * 10)
        for mixer_type in mixer_hits:
            mixer_indicators.append(f"알려진 믹서 주소: {mixer_type}")
    
    # 2. 다중 입력/출력 패턴 탐지
    multi_io_count = 0
    for tx in tx_list:
        inputs = tx.get('inputs', [])
        outputs = tx.get('outputs', [])
        
        if len(inputs) > 3 and len(outputs) > 3:
            multi_io_count += 1
    
    if multi_io_count > 0:
        mixer_score += min(20, multi_io_count * 5)
        mixer_indicators.append(f"다중 I/O 패턴: {multi_io_count}개 트랜잭션")
    
    # 2. 동일 금액 패턴 탐지 (믹서의 특징)
    amounts = [tx.get('amount', 0) for tx in tx_list]
    amount_counter = Counter(amounts)
    repeated_amounts = [amt for amt, count in amount_counter.items() if count >= 2 and amt > 0]
    
    if repeated_amounts:
        mixer_score += min(15, len(repeated_amounts) * 3)
        mixer_indicators.append(f"동일 금액 패턴: {len(repeated_amounts)}개 중복 금액")
    
    # 3. 시간 간격 패턴 분석 (믹서는 보통 짧은 간격으로 연속 트랜잭션)
    try:
        timestamps = [datetime.fromisoformat(tx['timestamp']) for tx in tx_list if 'timestamp' in tx]
        if len(timestamps) >= 2:
            intervals = [(t2 - t1).total_seconds() for t1, t2 in zip(timestamps[:-1], timestamps[1:])]
            short_intervals = [i for i in intervals if i < 30]  # 30초 이내 간격
            
            if len(short_intervals) > len(intervals) * 0.5:  # 50% 이상이 짧은 간격
                mixer_score += 10
                mixer_indicators.append("빠른 연속 트랜잭션 패턴")
    except Exception:
        pass
    
    return mixer_score, mixer_indicators

# 7. Cross-chain Bridge 탐지 기능
def cross_chain_detection_score(tx_list):
    """
    크로스체인 브릿지 사용 여부를 탐지합니다.
    - 주요 브릿지 주소 패턴 탐지
    - 대용량 단일 트랜잭션 탐지
    - 특정 브릿지 서비스 주소 매칭
    """
    bridge_indicators = []
    bridge_score = 0
    
    if not tx_list:
        return bridge_score, bridge_indicators
    
    # 1. 브릿지 주소 매칭
    bridge_addresses = load_bridge_addresses()
    bridge_hits = set()  # 중복 제거를 위해 set 사용
    for tx in tx_list:
        to_address = tx.get('to', '')
        if to_address in bridge_addresses:
            bridge_hits.add(bridge_addresses[to_address])
    
    if bridge_hits:
        bridge_score += min(30, len(bridge_hits) * 10)
        for bridge_type in bridge_hits:
            bridge_indicators.append(f"브릿지 주소 감지: {bridge_type}")
    
    # 2. 대용량 단일 트랜잭션 탐지 (브릿지 특징)
    large_txs = [tx for tx in tx_list if tx.get('amount', 0) > 1000000]  # 1 BTC 이상
    if large_txs:
        bridge_score += min(20, len(large_txs) * 5)
        bridge_indicators.append(f"대용량 트랜잭션: {len(large_txs)}개")
    
    # 3. 특정 패턴 탐지 (브릿지 사용 시 특징적인 패턴)
    # - 큰 금액의 단일 트랜잭션 후 작은 금액의 분산
    amounts = [tx.get('amount', 0) for tx in tx_list]
    if amounts:
        max_amount = max(amounts)
        if max_amount > 500000:  # 0.5 BTC 이상
            small_txs = [amt for amt in amounts if 0 < amt < max_amount * 0.1]
            if len(small_txs) >= 2:
                bridge_score += 15
                bridge_indicators.append("브릿지 후 분산 패턴 감지")
    
    return bridge_score, bridge_indicators

# 8. 통합 세탁 의심도 분석
def money_laundering_risk_score(tx_list):
    """
    전체적인 세탁 의심도를 종합적으로 분석합니다.
    """
    risk_indicators = []
    total_risk_score = 0
    
    # 각 탐지 기능 실행
    mixer_score, mixer_indicators = mixer_detection_score(tx_list)
    bridge_score, bridge_indicators = cross_chain_detection_score(tx_list)
    
    total_risk_score = mixer_score + bridge_score
    
    # 지표들 통합
    risk_indicators.extend(mixer_indicators)
    risk_indicators.extend(bridge_indicators)
    
    # 추가 위험 지표
    if len(tx_list) > 10:
        risk_indicators.append("높은 트랜잭션 볼륨")
        total_risk_score += 10
    
    # 금액 분산 패턴
    amounts = [tx.get('amount', 0) for tx in tx_list]
    if amounts:
        amount_variance = np.var(amounts) if len(amounts) > 1 else 0
        if amount_variance > 1000000:  # 높은 분산
            risk_indicators.append("불규칙한 금액 분산 패턴")
            total_risk_score += 15
    
    return total_risk_score, risk_indicators
