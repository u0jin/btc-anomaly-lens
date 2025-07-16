import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from ui.language import get_text

def apply_styles():
    """UI 스타일을 적용하는 함수"""
    # 💎 프리미엄 UI 스타일 적용
    st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #08BDBD;
        color: white;
        font-weight: 600;
        padding: 0.6em 1.2em;
        border-radius: 8px;
        transition: background-color 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #0a9a9a;
    }
    </style>
    """, unsafe_allow_html=True)

    # 사이드바에 툴 목적 명시
    st.sidebar.markdown("""
    <span style='font-size:13px; color:gray'>
    🔍 This tool is developed as part of a real-world blockchain forensic system, simulating TRM-style risk detection.
    </span>
    """, unsafe_allow_html=True)

def show_layout(
    lang, total_score,
    interval_score, short_intervals,
    amount_score, outliers,
    address_score, flagged_addresses,
    time_score, abnormal_gaps,
    blacklist_score_val, blacklist_flag,
    mixer_score=0, mixer_indicators=[],
    bridge_score=0, bridge_indicators=[],
    laundering_score=0, laundering_indicators=[],
    exchange_pattern_analysis=None
):
    # UI 스타일 적용
    apply_styles()
    
    t = get_text(lang)

    display_score = min(total_score, 100)

    with st.expander("📊 Risk Score Breakdown (Donut Chart)", expanded=False):
        score_parts = {
            "Interval": interval_score,
            "Amount": amount_score,
            "Address": address_score,
            "TimeGap": time_score,
            "Blacklist": blacklist_score_val,
            "Mixer": mixer_score,
            "Cross-chain": bridge_score
        }
        fig_donut = px.pie(
            names=list(score_parts.keys()),
            values=list(score_parts.values()),
            hole=0.5,
            title="Risk Score Composition"
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown(f"<h4>{t['total_score']}: <span style='color:#FF4B4B'>{display_score:.1f} / 100</span></h4>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-weight:500; color:#ccc;'>This score is calculated from multiple behavioral anomaly metrics designed to reflect forensic risk in live BTC traffic.</p>", unsafe_allow_html=True)
    if total_score > 100:
        st.caption("⚠️ One or more critical anomalies detected. Total score capped at 100.")

    with st.expander("📊 Radar Chart"):
        radar_data = {
            "항목": ["간격", "금액", "주소", "시계열", "블랙리스트", "믹서", "크로스체인"],
            "점수": [
                interval_score / 25 * 100,
                amount_score / 25 * 100,
                address_score / 25 * 100,
                time_score / 15 * 100,
                blacklist_score_val,
                mixer_score / 25 * 100,
                bridge_score / 30 * 100
            ]
        }
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=radar_data["점수"],
            theta=radar_data["항목"],
            fill='toself',
            name='Risk Profile'
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    def score_section(title, logic_md, score_val, max_score, none_msg, chart_fn=None):
        with st.container():
            st.markdown(f"### {title}")
            with st.popover(t['view_logic']):
                st.markdown(logic_md, unsafe_allow_html=True)
            st.markdown(f"**{t['score']}:** {score_val:.1f} / {max_score}")
            if chart_fn:
                chart_fn()
            else:
                st.info(none_msg)

    def interval_chart():
        if short_intervals:
            df = pd.DataFrame(short_intervals, columns=[t['interval_chart_label']])
            fig = px.histogram(df, x=t['interval_chart_label'], nbins=20, title=t['interval_chart_title'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(t['interval_none'])

    def amount_chart():
        if outliers:
            df = pd.DataFrame(outliers, columns=[t['amount_chart_label']])
            fig = px.box(df, y=t['amount_chart_label'], title=t['amount_chart_title'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(t['amount_none'])

    def address_chart():
        if flagged_addresses:
            df = pd.DataFrame(flagged_addresses, columns=[t['address_chart_label']])
            fig = px.histogram(df, x=t['address_chart_label'], title=t['address_chart_title'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(t['address_none'])

    def timegap_chart():
        if abnormal_gaps:
            df = pd.DataFrame(abnormal_gaps, columns=[t['timegap_chart_label']])
            fig = px.histogram(df, x=t['timegap_chart_label'], nbins=20, title=t['timegap_chart_title'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(t['timegap_none'])

    def mixer_chart():
        if mixer_indicators:
            # 믹서 지표들을 카테고리별로 분류
            categories = {
                "다중 I/O 패턴": 0,
                "동일 금액 패턴": 0,
                "빠른 연속 트랜잭션": 0
            }
            
            for indicator in mixer_indicators:
                if "다중 I/O 패턴" in indicator:
                    categories["다중 I/O 패턴"] += 1
                elif "동일 금액 패턴" in indicator:
                    categories["동일 금액 패턴"] += 1
                elif "빠른 연속 트랜잭션" in indicator:
                    categories["빠른 연속 트랜잭션"] += 1
            
            df = pd.DataFrame(list(categories.items()), columns=['Pattern Type', 'Count'])
            fig = px.bar(df, x='Pattern Type', y='Count', title=t['mixer_chart_title'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(t['mixer_chart_none'])

    def bridge_chart():
        if bridge_indicators:
            # 브릿지 지표들을 카테고리별로 분류
            categories = {
                "브릿지 주소 감지": 0,
                "대용량 트랜잭션": 0,
                "브릿지 후 분산 패턴": 0
            }
            
            for indicator in bridge_indicators:
                if "브릿지 주소 감지" in indicator:
                    categories["브릿지 주소 감지"] += 1
                elif "대용량 트랜잭션" in indicator:
                    categories["대용량 트랜잭션"] += 1
                elif "브릿지 후 분산 패턴" in indicator:
                    categories["브릿지 후 분산 패턴"] += 1
            
            df = pd.DataFrame(list(categories.items()), columns=['Pattern Type', 'Count'])
            fig = px.bar(df, x='Pattern Type', y='Count', title=t['bridge_chart_title'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(t['bridge_chart_none'])

    def laundering_chart():
        if laundering_indicators:
            # 세탁 의심도 지표들을 카테고리별로 분류
            categories = {
                "믹서 패턴": 0,
                "브릿지 패턴": 0,
                "높은 트랜잭션 볼륨": 0,
                "불규칙한 금액 분산": 0
            }
            
            for indicator in laundering_indicators:
                if any(keyword in indicator for keyword in ["다중 I/O", "동일 금액", "빠른 연속"]):
                    categories["믹서 패턴"] += 1
                elif any(keyword in indicator for keyword in ["브릿지", "대용량"]):
                    categories["브릿지 패턴"] += 1
                elif "높은 트랜잭션 볼륨" in indicator:
                    categories["높은 트랜잭션 볼륨"] += 1
                elif "불규칙한 금액 분산" in indicator:
                    categories["불규칙한 금액 분산"] += 1
            
            df = pd.DataFrame(list(categories.items()), columns=['Risk Factor', 'Count'])
            fig = px.pie(df, values='Count', names='Risk Factor', title=t['laundering_chart_title'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(t['laundering_chart_none'])

    def exchange_pattern_chart():
        if exchange_pattern_analysis and exchange_pattern_analysis.get('all_matches'):
            # 거래소별 유사도 데이터 준비
            exchanges = []
            similarities = []
            confidences = []
            
            for exchange, match_info in exchange_pattern_analysis['all_matches'].items():
                exchanges.append(exchange)
                similarities.append(match_info['similarity'])
                confidences.append(match_info['confidence'])
            
            # 색상 매핑
            color_map = {'high': '#FF6B6B', 'medium': '#FFA500', 'low': '#FFD700'}
            colors = [color_map.get(conf, '#FFD700') for conf in confidences]
            
            df = pd.DataFrame({
                'Exchange': exchanges,
                'Similarity': similarities,
                'Confidence': confidences
            })
            
            fig = px.bar(df, x='Exchange', y='Similarity', 
                        color='Confidence',
                        title=t['exchange_pattern_chart_title'],
                        color_discrete_map=color_map)
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(t['exchange_pattern_chart_none'])

    score_section("⏱️ " + t['interval_title'], t['interval_logic_md'], interval_score, 25, t['interval_none'], interval_chart)
    score_section("💰 " + t['amount_title'], t['amount_logic_md'], amount_score, 25, t['amount_none'], amount_chart)
    score_section("🔁 " + t['address_title'], t['address_logic_md'], address_score, 25, t['address_none'], address_chart)
    score_section("📉 " + t['timegap_title'], t['timegap_logic_md'], time_score, 15, t['timegap_none'], timegap_chart)

    # 🆕 Mixer 탐지 섹션 추가
    with st.container():
        st.markdown(f"### 🌀 {t['mixer_title']}")
        with st.popover(t['view_logic']):
            st.markdown(t['mixer_logic_md'], unsafe_allow_html=True)
        st.markdown(f"**{t['score']}:** {mixer_score:.1f} / 25")
        
        if mixer_indicators:
            st.markdown(f"⚠️ **{t['mixer_flagged']}**")
            for indicator in mixer_indicators:
                st.caption(f"• {indicator}")
        else:
            st.success(t['mixer_safe'])
            st.caption("일반적인 트랜잭션 패턴으로 보임")
        
        # 믹서 차트 추가
        mixer_chart()

    # 🆕 Cross-chain Bridge 탐지 섹션 추가
    with st.container():
        st.markdown(f"### 🌉 {t['bridge_title']}")
        with st.popover(t['view_logic']):
            st.markdown(t['bridge_logic_md'], unsafe_allow_html=True)
        st.markdown(f"**{t['score']}:** {bridge_score:.1f} / 30")
        
        if bridge_indicators:
            st.markdown(f"⚠️ **{t['bridge_flagged']}**")
            for indicator in bridge_indicators:
                st.caption(f"• {indicator}")
        else:
            st.success(t['bridge_safe'])
            st.caption("단일 체인 내 트랜잭션으로 보임")
        
        # 브릿지 차트 추가
        bridge_chart()

    # 🆕 통합 세탁 의심도 섹션 추가
    with st.container():
        st.markdown(f"### 🚨 {t['laundering_title']}")
        with st.popover(t['view_logic']):
            st.markdown(t['laundering_logic_md'], unsafe_allow_html=True)
        st.markdown(f"**Total Risk Score:** {laundering_score:.1f} / 100")
        
        if laundering_indicators:
            st.markdown(f"🚨 **{t['laundering_high']}**")
            for indicator in laundering_indicators:
                st.caption(f"• {indicator}")
        elif laundering_score > 30:
            st.markdown(f"⚠️ **{t['laundering_medium']}**")
            for indicator in laundering_indicators:
                st.caption(f"• {indicator}")
        else:
            st.success(t['laundering_low'])
            st.caption("정상적인 트랜잭션 패턴")
        
        # 세탁 의심도 차트 추가
        laundering_chart()

    # 🆕 거래소 패턴 분석 섹션 - 실제 데이터가 있을 때만 표시
    if exchange_pattern_analysis and exchange_pattern_analysis.get('analysis'):
        analysis = exchange_pattern_analysis['analysis']
        
        # 실제 데이터가 있는지 확인 (더 엄격한 조건)
        amount_patterns = analysis.get('amount_patterns', {})
        time_patterns = analysis.get('time_patterns', {})
        
        # 의미 있는 데이터가 있는지 확인
        meaningful_data = (
            amount_patterns.get('total_volume', 0) > 1000 or  # 최소 1000 sat 이상
            amount_patterns.get('avg_amount', 0) > 100 or      # 평균 100 sat 이상
            amount_patterns.get('round_numbers', 0) > 0 or     # 반올림 패턴이 있거나
            amount_patterns.get('high_volume', 0) > 0 or       # 대용량 거래가 있거나
            time_patterns.get('total_transactions', 0) > 5 or  # 최소 5개 이상 트랜잭션
            time_patterns.get('avg_interval', 0) > 10 or       # 평균 간격이 10초 이상이거나
            time_patterns.get('regular_intervals', 0) > 0.1 or # 정규 간격이 10% 이상이거나
            time_patterns.get('batch_processing', 0) > 0.1     # 배치 처리가 10% 이상
        )
        
        if meaningful_data:
            with st.container():
                st.markdown(f"### 🏦 {t['exchange_pattern_title']}")
                st.info("💡 거래소 인식 결과는 상단의 '🏦 거래소 인식 결과' 섹션에서 확인하세요.")
                st.caption("이 섹션은 거래소 패턴 분석의 상세 정보를 제공합니다.")
                
                # 기본 분석 정보만 표시 (중복 제거)
                with st.expander("📊 기본 패턴 분석 정보", expanded=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**💰 금액 패턴**")
                        st.caption(f"• 총 거래량: {amount_patterns.get('total_volume', 0):,.0f} sat")
                        st.caption(f"• 평균 거래량: {amount_patterns.get('avg_amount', 0):,.0f} sat")
                        st.caption(f"• 반올림 패턴: {amount_patterns.get('round_numbers', 0)}건")
                        st.caption(f"• 대용량 거래: {amount_patterns.get('high_volume', 0)}건")
                    
                    with col2:
                        st.markdown("**⏰ 시간 패턴**")
                        st.caption(f"• 총 트랜잭션: {time_patterns.get('total_transactions', 0)}건")
                        st.caption(f"• 평균 간격: {time_patterns.get('avg_interval', 0):.1f}초")
                        st.caption(f"• 정규 간격: {time_patterns.get('regular_intervals', 0):.1%}")
                        st.caption(f"• 배치 처리: {time_patterns.get('batch_processing', 0):.1%}")
                
                # 거래소 유사도 차트 (참고용)
                if exchange_pattern_analysis.get('all_matches'):
                    exchange_pattern_chart()

    with st.container():
        st.markdown(f"### 🚫 {t['blacklist_title']}")
        with st.popover(t['view_logic']):
            st.markdown(t['blacklist_logic_md'], unsafe_allow_html=True)
        st.markdown(f"**{t['score']}:** {blacklist_score_val:.1f} / 100")
        if blacklist_flag:
            st.markdown(f"🚨 **{t['blacklist_flagged']}**")
            st.caption("⚠️ This address is associated with known sanctioned or darknet entities.")
        else:
            st.success(t['blacklist_safe'])
            st.caption("✅ No critical blacklist match found. Address appears clean.")

        if total_score >= 75:
            st.markdown("⚠️ **🔍 This address exhibits highly suspicious behavior and matches several risk factors including timing, repetition, and potential sanctioning.**")
        elif total_score >= 50:
            st.info("⚠️ This address has moderate anomalies that may warrant further investigation.")
        else:
            st.success("🟢 No significant anomalies detected. Address shows normal transaction behavior.")

# 🔧 확장용 placeholder
def render_interval_chart(data):
    pass

# show_layout 함수가 외부에서 import될 수 있도록 명시적으로 선언
__all__ = ['show_layout', 'render_interval_chart']
