def get_text(lang):
    if lang == "한국어":
        return {
            "title": "비트코인 이상 거래 탐지 시스템",
            "caption": "이 도구는 실시간으로 비정상 거래 패턴을 분석합니다.",
            "risk_score": "위험 점수",
            "risk_help": "이 점수는 사용자 정의 로직 기반으로 계산됩니다.",

            # 사이드바
            "premium_on": "프리미엄 모드 활성화됨 (기능 시뮬레이션 전용)",
            "premium_off": "프리미엄 모드 꺼짐. 무료 API 사용 중입니다.",
            "creator_section": "개발자 정보",

            # 결과 화면 - 공통
            "total_score": "🧠 총 위험 점수",
            "score": "점수",
            "view_logic": "📘 점수 산정 기준 보기",

            # 1. 거래 간격 이상 탐지
            "interval_title": " 거래 간격 이상 탐지",
            "interval_logic_md": """
            **함수명:** `interval_anomaly_score(tx_list)`  
            **정의:** 60초 미만으로 반복되는 거래 간격을 탐지합니다.  
            **점수 기준:** 60초 미만 간격 1건당 5점 부여, 최대 25점
            """,
            "interval_chart_title": "짧은 거래 간격 분포",
            "interval_chart_label": "간격 (초)",
            "interval_none": "60초 미만의 거래 간격이 감지되지 않았습니다.",

            # 2. 이상 거래 금액
            "amount_title": " 이상 거래 금액",
            "amount_logic_md": """
            **함수명:** `amount_anomaly_score(tx_list)`  
            **정의:** 중위값 기준 이상금액(IQR 기준 초과)을 탐지합니다.  
            **점수 기준:** 이상 거래 1건당 10점 부여, 최대 25점
            """,
            "amount_chart_title": "이상 거래 금액 박스 플롯",
            "amount_chart_label": "BTC 금액",
            "amount_none": "이상 거래 금액이 감지되지 않았습니다.",

            # 3. 동일 수신 주소 반복
            "address_title": " 동일 수신 주소 반복",
            "address_logic_md": """
            **함수명:** `repeated_address_score(tx_list)`  
            **정의:** 동일한 수신 주소가 3회 이상 반복될 경우,  
            의심 주소로 간주하여 점수를 부여합니다.  
            **점수 기준:** 반복 주소 1개당 5점, 최대 25점
            """,
            "address_chart_title": "수신 주소 반복 빈도",
            "address_chart_label": "수신 주소",
            "address_none": "반복된 수신 주소가 감지되지 않았습니다.",

            # 4. 시계열 간격 이상
            "timegap_title": " 시계열 상 이상 간격",
            "timegap_logic_md": """
            **함수명:** `time_gap_anomaly_score(tx_list)`  
            **정의:** 10초 이하 또는 1시간 이상인 비정상 시간 간격 탐지  
            **점수 기준:** 이상 간격 1건당 5점, 최대 15점
            """,
            "timegap_chart_title": "거래 간 시계열 간격",
            "timegap_chart_label": "간격 (초)",
            "timegap_none": "비정상 시간 간격이 감지되지 않았습니다.",

            # 5. 블랙리스트 탐지
            "blacklist_title": " 제재 주소 탐지",
            "blacklist_logic_md": """
            **함수명:** `blacklist_score(tx_list)`  
            **정의:** 국제 제재 목록 (OFAC 등)에 포함된 주소 발견 시,  
            위험 점수 최대 부여 (기본 10점, 직접 포함 시 100점)
            """,
            "blacklist_flagged": "❗ 제재 주소 탐지됨: 위험",
            "blacklist_safe": "✅ 제재 주소와의 연결 없음",

            # 6. 믹서 탐지
            "mixer_title": " 믹서 탐지",
            "mixer_logic_md": """
            **함수명:** `mixer_detection_score(tx_list)`  
            **정의:** Wasabi, Samourai, JoinMarket 등 믹서 서비스의 특징적 패턴 탐지  
            **탐지 방법:**
            - 다중 입력/출력 패턴: 3개 이상 입력/출력 시 +5점 (최대 20점)
            - 동일 금액 반복: 같은 금액 2회 이상 반복 시 +3점 (최대 15점)
            - 빠른 연속 트랜잭션: 30초 이내 연속이 50% 이상 시 +10점
            **점수 기준:** 최대 25점
            """,
            "mixer_flagged": "🔍 믹서 사용 의심 패턴 감지됨",
            "mixer_safe": "✅ 믹서 사용 의심 패턴 없음",

            # 7. 크로스체인 브릿지 탐지
            "bridge_title": " 크로스체인 브릿지 탐지",
            "bridge_logic_md": """
            **함수명:** `cross_chain_detection_score(tx_list)`  
            **정의:** 크로스체인 브릿지 서비스 사용 패턴 탐지  
            **탐지 방법:**
            - 브릿지 주소 매칭: 알려진 브릿지 주소와 매칭 시 +10점 (최대 30점)
            - 대용량 트랜잭션: 1 BTC 이상 단일 트랜잭션 시 +5점 (최대 20점)
            - 브릿지 후 분산: 큰 금액 후 작은 금액 분산 패턴 시 +15점
            **점수 기준:** 최대 30점
            """,
            "bridge_flagged": "🌉 크로스체인 브릿지 사용 의심",
            "bridge_safe": "✅ 크로스체인 브릿지 사용 의심 없음",

            # 8. 세탁 의심도 분석
            "laundering_title": " 세탁 의심도 분석",
            "laundering_logic_md": """
            **함수명:** `money_laundering_risk_score(tx_list)`  
            **정의:** 믹서와 브릿지 패턴을 통합한 종합 세탁 의심도 평가  
            **탐지 방법:**
            - 믹서 점수 + 브릿지 점수 합산
            - 높은 트랜잭션 볼륨: 10개 이상 시 +10점
            - 불규칙한 금액 분산: 높은 분산 패턴 시 +15점
            **점수 기준:** 최대 100점 (높음: 50점 이상, 중간: 30-50점, 낮음: 30점 미만)
            """,
            "laundering_high": "🚨 높은 세탁 의심도",
            "laundering_medium": "⚠️ 중간 세탁 의심도",
            "laundering_low": "✅ 낮은 세탁 의심도",

            # 차트 관련 텍스트
            "mixer_chart_title": "믹서 탐지 패턴 분석",
            "mixer_chart_none": "믹서 탐지 패턴이 없습니다.",
            "bridge_chart_title": "크로스체인 브릿지 탐지 패턴 분석",
            "bridge_chart_none": "크로스체인 브릿지 탐지 패턴이 없습니다.",
            "laundering_chart_title": "세탁 의심도 위험 요소 분포",
            "laundering_chart_none": "세탁 의심도 지표가 없습니다.",
            # 거래소 탐지
            "exchange_detected": "거래소 주소와 연결됨 (입출금):",
            "exchange_safe": "✅ 거래소와 직접 연결된 내역 없음.",
            
            # 거래소 패턴 분석
            "exchange_pattern_title": " 거래소 패턴 분석",
            "exchange_pattern_logic_md": """
            **함수명:** `analyze_exchange_patterns(tx_list)`  
            **정의:** AI 기반 거래소 패턴 분석으로 엔트로피, 금액 패턴, 시간 패턴을 종합 분석  
            **분석 방법:**
            - **엔트로피 분석**: 주소의 정보 이론적 복잡도 계산 (30% 가중치)
            - **금액 패턴**: 반올림 숫자, 환산 패턴, 대용량 거래 탐지 (20% 가중치)
            - **시간 패턴**: 시간대별 활동, 정규 간격, 배치 처리 패턴 (20% 가중치)
            - **주소 패턴**: bc1/SegWit vs 레거시 형식 선호도 (10% 가중치)
            **신뢰도 기준:** HIGH (70%+), MEDIUM (50-70%), LOW (<50%)
            """,
            "exchange_pattern_entropy_logic": """
            **엔트로피 계산 공식**
            - 각 주소의 문자 빈도 기반 정보 이론 엔트로피 계산
            - H = -Σ(p_i * log2(p_i)), p_i: 각 문자 출현 확률
            - 엔트로피가 높을수록 복잡한 주소 패턴 (SegWit 등)
            """,
            "exchange_pattern_amount_logic": """
            **금액 패턴 분석 기준**
            - 반올림 숫자: 1000, 10000, 100000 단위 거래
            - 대용량 거래: 1 BTC(=100,000,000 sat) 이상
            - KRW 환산: 45,000,000~55,000,000 sat (1 BTC ≈ 5천만원)
            - USD 환산: 35,000,000~45,000,000 sat (1 BTC ≈ 4만달러)
            """,
            "exchange_pattern_time_logic": """
            **시간 패턴 분석 기준**
            - 한국 시간대: 9~18시 (KST)
            - 미국 시간대: 14~23시 (UTC)
            - 정규 간격: 30~300초(0.5~5분) 간격 반복
            - 배치 처리: 60초 미만 연속 트랜잭션 비율
            """,
            "exchange_pattern_address_logic": """
            **주소 패턴 분석 기준**
            - bc1: SegWit 주소 (신규 거래소 선호)
            - 1/3: 레거시 주소 (구 거래소/한국 거래소 선호)
            - 다중 출력: 2개 이상 output
            - 단일 출력: 1개 output
            """,
            "exchange_pattern_chart_title": "거래소 유사도 분석",
            "exchange_pattern_chart_none": "거래소 패턴 분석 결과가 없습니다.",
            "exchange_pattern_best_match": "🎯 가장 유사한 거래소",
            "exchange_pattern_similarity": "유사도",
            "exchange_pattern_confidence": "신뢰도",
            "exchange_pattern_entropy": "엔트로피",
            "exchange_pattern_amount": "금액 패턴",
            "exchange_pattern_time": "시간 패턴",
            "exchange_pattern_address": "주소 패턴",
            
            # 네트워크 시각화 관련
            "network_visualization": "네트워크 시각화",
            "max_hops_setting": "최대 Hop 수 설정",
            "max_hops_help": "네트워크 시각화에서 표시할 최대 연결 단계 수 (1-10)",
            "max_nodes_setting": "표시할 최대 노드 수",
            "max_nodes_help": "네트워크에서 표시할 최대 노드 수",
            "network_stats": "네트워크 통계",
            "total_nodes": "총 노드 수",
            "total_edges": "총 연결 수",
            "unique_recipients": "고유 수신 주소",
            "total_volume": "총 거래량",
            "network_visualization_title": "트랜잭션 네트워크 시각화",
            "network_visualization_help": "네트워크 시각화는 최대 {max_hops} hop, 상위 {top_nodes}개 노드를 표시합니다.",
            "network_visualization_error": "네트워크 시각화를 생성할 수 없습니다.",
            "network_settings": "네트워크 시각화 설정",
            "save_settings": "설정 저장",
            "settings_saved": "네트워크 설정이 저장되었습니다!",
            "reset_settings": "기본값으로 초기화",
            "saved_settings": "저장된 설정",
            "current_settings": "현재 설정",
            "not_saved": "저장되지 않음",
            
            # 시나리오 매칭 설정
            "scenario_matching_settings": "시나리오 매칭 설정",
            "matching_threshold": "매칭 임계값 (%)",
            "matching_threshold_help": "알려진 시나리오와 매칭하기 위한 최소 유사도 (%)",
            "save_scenario_settings": "저장",
            "reset_scenario_settings": "초기화",
            "scenario_settings_saved": "시나리오 설정 저장됨!",
            "scenario_settings_reset": "시나리오 설정 초기화됨"
        }
    else:
        return {
            "title": "Bitcoin Anomaly Detection System",
            "caption": "This tool analyzes abnormal transaction patterns in real-time.",
            "risk_score": "Risk Score",
            "risk_help": "Score is calculated based on custom logic.",

            # Sidebar
            "premium_on": "Premium mode is ON. (Feature simulation only)",
            "premium_off": "Premium mode is OFF. Using free API.",
            "creator_section": "About the Creator",

            # Shared
            "total_score": " Total Risk Score",
            "score": "Score",
            "view_logic": " View Scoring Logic",

            # 1. Interval
            "interval_title": " Time Interval Anomaly",
            "interval_logic_md": """
            **Function:** `interval_anomaly_score(tx_list)`  
            **Definition:** Detects transactions spaced less than 60s apart.  
            **Scoring:** +5 pts per short interval, max 25 pts
            """,
            "interval_chart_title": "Short Interval Distribution",
            "interval_chart_label": "Interval (s)",
            "interval_none": "No short intervals detected.",

            # 2. Amount
            "amount_title": " Amount Outlier Detection",
            "amount_logic_md": """
            **Function:** `amount_anomaly_score(tx_list)`  
            **Definition:** Detects abnormal values beyond 1.5x IQR.  
            **Scoring:** +10 pts per outlier, max 25 pts
            """,
            "amount_chart_title": "Transaction Amount Box Plot",
            "amount_chart_label": "Amount (BTC)",
            "amount_none": "No outlier transactions detected.",

            # 3. Address
            "address_title": " Repeated Receiver Address",
            "address_logic_md": """
            **Function:** `repeated_address_score(tx_list)`  
            **Definition:** Detects repeated receiver addresses (≥3).  
            **Scoring:** +5 pts per address, max 25 pts
            """,
            "address_chart_title": "Receiver Address Frequency",
            "address_chart_label": "Address",
            "address_none": "No repeated addresses detected.",

            # 4. Time Gap
            "timegap_title": " Abnormal Time Gaps",
            "timegap_logic_md": """
            **Function:** `time_gap_anomaly_score(tx_list)`  
            **Definition:** Detects irregular time gaps (<10s or >1h).  
            **Scoring:** +5 pts per gap, max 15 pts
            """,
            "timegap_chart_title": "Transaction Time Gaps",
            "timegap_chart_label": "Interval (s)",
            "timegap_none": "No irregular gaps detected.",

            # 5. Blacklist
            "blacklist_title": " Blacklist Detection",
            "blacklist_logic_md": """
            **Function:** `blacklist_score(tx_list)`  
            **Definition:** Detects addresses matching OFAC or sanction lists.  
            **Scoring:** 10 pts if indirectly linked, 100 pts if directly used
            """,
            "blacklist_flagged": "❗ Blacklisted address detected",
            "blacklist_safe": "✅ No blacklist matches found",

            # 6. Mixer Detection
            "mixer_title": " Mixer Detection",
            "mixer_logic_md": """
            **Function:** `mixer_detection_score(tx_list)`  
            **Definition:** Detects characteristic patterns of mixer services like Wasabi, Samourai, JoinMarket  
            **Detection Methods:**
            - Multi I/O Pattern: +5 pts per transaction with >3 inputs/outputs (max 20 pts)
            - Repeated Amount Pattern: +3 pts per repeated amount ≥2 times (max 15 pts)
            - Fast Sequential Transactions: +10 pts if >50% intervals <30s
            **Scoring:** Maximum 25 points
            """,
            "mixer_flagged": "🔍 Mixer usage pattern detected",
            "mixer_safe": "✅ No mixer usage patterns detected",

            # 7. Cross-chain Bridge Detection
            "bridge_title": " Cross-chain Bridge Detection",
            "bridge_logic_md": """
            **Function:** `cross_chain_detection_score(tx_list)`  
            **Definition:** Detects cross-chain bridge service usage patterns  
            **Detection Methods:**
            - Bridge Address Matching: +10 pts per known bridge address (max 30 pts)
            - Large Transaction: +5 pts per transaction >1 BTC (max 20 pts)
            - Post-bridge Distribution: +15 pts for large-to-small amount distribution
            **Scoring:** Maximum 30 points
            """,
            "bridge_flagged": "🌉 Cross-chain bridge usage suspected",
            "bridge_safe": "✅ No cross-chain bridge usage detected",

            # 8. Money Laundering Risk Assessment
            "laundering_title": " Money Laundering Risk Assessment",
            "laundering_logic_md": """
            **Function:** `money_laundering_risk_score(tx_list)`  
            **Definition:** Comprehensive money laundering risk assessment combining mixer and bridge patterns  
            **Detection Methods:**
            - Mixer Score + Bridge Score summation
            - High Transaction Volume: +10 pts if >10 transactions
            - Irregular Amount Distribution: +15 pts for high variance patterns
            **Scoring:** Maximum 100 points (High: ≥50 pts, Medium: 30-50 pts, Low: <30 pts)
            """,
            "laundering_high": "🚨 High money laundering risk",
            "laundering_medium": "⚠️ Medium money laundering risk",
            "laundering_low": "✅ Low money laundering risk",

            # Chart related text
            "mixer_chart_title": "Mixer Detection Pattern Analysis",
            "mixer_chart_none": "No mixer detection patterns found.",
            "bridge_chart_title": "Cross-chain Bridge Detection Pattern Analysis",
            "bridge_chart_none": "No cross-chain bridge detection patterns found.",
            "laundering_chart_title": "Money Laundering Risk Factor Distribution",
            "laundering_chart_none": "No money laundering risk indicators found.",
            # 거래소 탐지
            "exchange_detected": "Linked to Exchange Address (Deposit/Withdrawal):",
            "exchange_safe": "✅ No direct exchange linkage detected.",
            
            # Exchange Pattern Analysis
            "exchange_pattern_title": " Exchange Pattern Analysis",
            "exchange_pattern_logic_md": """
            **Function:** `analyze_exchange_patterns(tx_list)`  
            **Definition:** AI-based exchange pattern analysis using entropy, amount patterns, and time patterns  
            **Analysis Methods:**
            - **Entropy Analysis**: Information theory-based address complexity calculation (30% weight)
            - **Amount Patterns**: Round numbers, conversion patterns, high-volume transactions (20% weight)
            - **Time Patterns**: Timezone activity, regular intervals, batch processing (20% weight)
            - **Address Patterns**: bc1/SegWit vs legacy format preferences (10% weight)
            **Confidence Levels:** HIGH (70%+), MEDIUM (50-70%), LOW (<50%)
            """,
            "exchange_pattern_entropy_logic": """
            **엔트로피 계산 공식**
            - 각 주소의 문자 빈도 기반 정보 이론 엔트로피 계산
            - H = -Σ(p_i * log2(p_i)), p_i: 각 문자 출현 확률
            - 엔트로피가 높을수록 복잡한 주소 패턴 (SegWit 등)
            """,
            "exchange_pattern_amount_logic": """
            **금액 패턴 분석 기준**
            - 반올림 숫자: 1000, 10000, 100000 단위 거래
            - 대용량 거래: 1 BTC(=100,000,000 sat) 이상
            - KRW 환산: 45,000,000~55,000,000 sat (1 BTC ≈ 5천만원)
            - USD 환산: 35,000,000~45,000,000 sat (1 BTC ≈ 4만달러)
            """,
            "exchange_pattern_time_logic": """
            **시간 패턴 분석 기준**
            - 한국 시간대: 9~18시 (KST)
            - 미국 시간대: 14~23시 (UTC)
            - 정규 간격: 30~300초(0.5~5분) 간격 반복
            - 배치 처리: 60초 미만 연속 트랜잭션 비율
            """,
            "exchange_pattern_address_logic": """
            **주소 패턴 분석 기준**
            - bc1: SegWit 주소 (신규 거래소 선호)
            - 1/3: 레거시 주소 (구 거래소/한국 거래소 선호)
            - 다중 출력: 2개 이상 output
            - 단일 출력: 1개 output
            """,
            "exchange_pattern_chart_title": "Exchange Similarity Analysis",
            "exchange_pattern_chart_none": "No exchange pattern analysis results.",
            "exchange_pattern_best_match": "🎯 Best Matching Exchange",
            "exchange_pattern_similarity": "Similarity",
            "exchange_pattern_confidence": "Confidence",
            "exchange_pattern_entropy": "Entropy",
            "exchange_pattern_amount": "Amount Patterns",
            "exchange_pattern_time": "Time Patterns",
            "exchange_pattern_address": "Address Patterns",
            
            # Network Visualization
            "network_visualization": "Network Visualization",
            "max_hops_setting": "Max Hops Setting",
            "max_hops_help": "Maximum connection steps to display in network visualization (1-10)",
            "max_nodes_setting": "Max Nodes to Display",
            "max_nodes_help": "Maximum number of nodes to display in network",
            "network_stats": "Network Statistics",
            "total_nodes": "Total Nodes",
            "total_edges": "Total Edges",
            "unique_recipients": "Unique Recipients",
            "total_volume": "Total Volume",
            "network_visualization_title": "Transaction Network Visualization",
            "network_visualization_help": "Network visualization shows max {max_hops} hops, top {top_nodes} nodes.",
            "network_visualization_error": "Unable to generate network visualization.",
            "network_settings": "Network Visualization Settings",
            "save_settings": "Save Settings",
            "settings_saved": "Network settings saved successfully!",
            "reset_settings": "Reset to Default",
            "saved_settings": "Saved Settings",
            "current_settings": "Current Settings",
            "not_saved": "Not Saved",
            
            # Scenario Matching Settings
            "scenario_matching_settings": "Scenario Matching Settings",
            "matching_threshold": "Matching Threshold (%)",
            "matching_threshold_help": "Minimum similarity (%) required to match with a known scenario",
            "save_scenario_settings": "Save",
            "reset_scenario_settings": "Reset",
            "scenario_settings_saved": "Scenario settings saved!",
            "scenario_settings_reset": "Scenario settings reset"
        }
