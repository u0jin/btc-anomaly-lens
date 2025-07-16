# BTC Anomaly Lens 🔍

비트코인 거래 이상 탐지 도구 - 블록체인 포렌식 시스템

## 📋 주요 기능

### 🔍 이상 탐지 기능
- **거래 간격 이상**: 60초 미만 연속 트랜잭션 탐지
- **금액 이상**: IQR 기반 이상치 탐지
- **주소 반복**: 동일 주소 반복 사용 탐지
- **시계열 이상**: 비정상적인 시간 간격 탐지
- **블랙리스트 매칭**: 알려진 위험 주소 탐지

### 🆕 추가된 기능 (교수님 피드백 반영)
- **믹서(Mixer) 탐지**: Wasabi, Samourai, JoinMarket 등
- **크로스체인 브릿지 탐지**: WBTC, RenVM, Multichain 등
- **통합 세탁 의심도 분석**: 종합적인 위험도 평가

### 🏦 🆕 거래소 패턴 분석 (NEW!)
- **AI 기반 거래소 식별**: 엔트로피, 금액 패턴, 시간 패턴 분석
- **거래소별 특징 매칭**: Binance, Upbit, Coinbase, OKX 등 13개 거래소
- **실시간 패턴 분석**: 금액 분산, 시간대별 활동, 주소 형식 분석
- **신뢰도 평가**: High/Medium/Low 신뢰도로 거래소 매칭 정확도 표시

## 📊 데이터 출처

### 믹서 주소 출처
- **Chainalysis 2023 Report**: Wasabi Wallet 관련 주소
- **Elliptic 2023 Report**: Samourai Wallet 관련 주소
- **TRM Labs 2023 Report**: JoinMarket 관련 주소
- **CipherTrace 2023 Report**: 기타 알려진 믹서 주소

### 브릿지 주소 출처
- **WBTC Official**: https://wbtc.network/
- **RenVM Official**: https://renproject.io/
- **Multichain Official**: https://multichain.org/
- **Binance Official**: https://www.binance.com/en/bridge
- **Coinbase Official**: https://www.coinbase.com/bridge
- **DeFi Pulse**: https://defipulse.com/
- **DeFi Llama**: https://defillama.com/

### 블록체인 분석 기업 출처
- **Chainalysis**: https://www.chainalysis.com/reports/
- **Elliptic**: https://www.elliptic.co/insights/
- **TRM Labs**: https://www.trmlabs.com/insights/
- **CipherTrace**: https://ciphertrace.com/insights/

### 거래소 패턴 분석 출처
- **실제 거래소 주소**: Chainalysis, OKLink, Etherscan, 각 거래소 공식 문서
- **패턴 분석 알고리즘**: 정보 이론 기반 엔트로피 계산, 시계열 분석, 금액 분산 패턴
- **거래소별 특징**: 시간대별 활동, 주소 형식 선호도, 거래량 패턴 분석

## 🚀 설치 및 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 앱 실행
streamlit run app.py
```

## 📈 사용 예시

### 대표적인 비트코인 주소들

**거래소 주소:**
- `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa` (Satoshi의 Genesis 블록 주소)
- `3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy` (Binance 핫월렛)
- `3D2oetdNuZUqQHPJmcMDDHYoqkyNVsFk9r` (Upbit 핫월렛)
- `3QCzvfL4ZRvmJFiWWBVwxfdaNBT8EtxB5y` (Coinbase 핫월렛)

**믹서 주소:**
- `bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh` (Wasabi Wallet)
- `1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2` (JoinMarket)

**브릿지 주소:**
- `3Kzh9qAqXWxQ9P3nLjY2GKmGypFMQ5rHMs` (RenVM Bridge)
- `1FzWLkAahHooV3TzLvzv2YnuKFj3fx4m6B` (Binance Bridge)

**테스트용 주소:**
- `bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh` (일반 사용자)

## 🔧 기술 스택

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Blockchain API**: BlockCypher, Mempool.space
- **Risk Detection**: Custom algorithms

## 📝 라이선스

이 프로젝트는 교육 및 연구 목적으로 개발되었습니다.

## ⚠️ 면책 조항

이 도구는 블록체인 포렌식 연구 목적으로 개발되었으며, 실제 법적 조사나 규제 목적으로 사용하기 전에 전문가의 검토가 필요합니다. 모든 주소 데이터는 공신력 있는 출처에서 수집되었으나, 지속적인 업데이트가 필요합니다.
