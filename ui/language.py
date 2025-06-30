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
            "blacklist_safe": "✅ 제재 주소와의 연결 없음"
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
            "blacklist_safe": "✅ No blacklist matches found"
        }
