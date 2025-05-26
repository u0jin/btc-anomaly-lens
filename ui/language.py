def get_text(lang):
    if lang == "한국어":
        return {
            "title": "비트코인 이상 거래 탐지 시스템",
            "caption": "이 도구는 실시간으로 비정상 거래 패턴을 분석합니다.",
            "risk_score": "위험 점수",
            "risk_help": "이 점수는 사용자 정의 로직 기반으로 계산됩니다.",
            "logic_title": "탐지 로직 설명 보기",
            "logic_description": "60초 이하 간격의 반복 거래를 감지하는 함수입니다. 점수는 개수에 따라 증가합니다."
        }
    else:
        return {
            "title": "Bitcoin Anomaly Detection System",
            "caption": "This tool analyzes abnormal transaction patterns in real-time.",
            "risk_score": "Risk Score",
            "risk_help": "Score is calculated based on custom logic.",
            "logic_title": "View Detection Logic",
            "logic_description": "This function detects repeated transactions with intervals under 60 seconds. The risk score increases by the count."
        }
